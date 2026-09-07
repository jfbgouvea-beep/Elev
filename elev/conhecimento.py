"""Carrega e valida a base de conhecimento da ELEV.

Este modulo e a fronteira entre "fato cadastrado" e "invencao". Ele tambem
renderiza os blocos de texto que entram no prompt do agente, marcando de forma
explicita o que NAO esta cadastrado - e isso que ensina o agente a dizer
"preciso verificar com a equipe" em vez de chutar.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

NAO_CADASTRADO = "NAO CADASTRADO - responder que precisa verificar com a equipe"


class BaseInvalida(Exception):
    """A base de conhecimento esta faltando algo obrigatorio."""


def _ler_yaml(caminho: Path) -> Any:
    if not caminho.exists():
        raise BaseInvalida(f"Arquivo obrigatorio nao encontrado: {caminho}")
    dados = yaml.safe_load(caminho.read_text(encoding="utf-8"))
    if dados is None:
        raise BaseInvalida(f"Arquivo vazio: {caminho}")
    return dados


def _valor(v: Any) -> str:
    """Formata um valor para o prompt, sinalizando ausencia com clareza."""
    if v is None or v == "" or v == []:
        return NAO_CADASTRADO
    if isinstance(v, list):
        return "\n" + "\n".join(f"  - {item}" for item in v)
    return str(v).strip()


@dataclass
class Conhecimento:
    """Toda a informacao oficial da ELEV, ja carregada e validada."""

    empresa: dict
    servicos: list[dict]
    faq: list[dict]
    qualificacao: dict

    # ---------------------------------------------------------------- carga
    @classmethod
    def carregar(cls, dir_conhecimento: Path) -> "Conhecimento":
        base = cls(
            empresa=_ler_yaml(dir_conhecimento / "empresa.yaml"),
            servicos=_ler_yaml(dir_conhecimento / "servicos.yaml"),
            faq=_ler_yaml(dir_conhecimento / "faq.yaml"),
            qualificacao=_ler_yaml(dir_conhecimento / "qualificacao.yaml"),
        )
        base.validar()
        return base

    def validar(self) -> None:
        """Falha cedo se a base estiver quebrada - antes de falar com cliente."""
        if not self.empresa.get("nome"):
            raise BaseInvalida("empresa.yaml precisa ter 'nome'.")
        if not self.servicos:
            raise BaseInvalida("servicos.yaml esta sem servicos.")
        for s in self.servicos:
            faltando = {"id", "nome", "resumo"} - set(s)
            if faltando:
                raise BaseInvalida(f"Servico {s.get('id', '?')} sem campos: {faltando}")
        if not self.qualificacao.get("campos"):
            raise BaseInvalida("qualificacao.yaml precisa da lista 'campos'.")
        if not self.qualificacao.get("gatilhos_handoff"):
            raise BaseInvalida("qualificacao.yaml precisa de 'gatilhos_handoff'.")

    # ------------------------------------------------------------- consultas
    def servico(self, id_servico: str) -> dict | None:
        return next((s for s in self.servicos if s["id"] == id_servico), None)

    @property
    def ids_servicos(self) -> list[str]:
        return [s["id"] for s in self.servicos]

    @property
    def ids_gatilhos(self) -> list[str]:
        return [g["id"] for g in self.qualificacao["gatilhos_handoff"]]

    def lacunas(self) -> list[str]:
        """Campos ainda nao cadastrados. Serve de checklist para a equipe."""
        pendentes = [f"empresa.{k}" for k, v in self.empresa.items() if v in (None, "", [])]
        for s in self.servicos:
            pendentes += [
                f"servicos.{s['id']}.{k}"
                for k in ("prazo", "preco")
                if s.get(k) in (None, "", [])
            ]
        return pendentes

    # ------------------------------------------------- renderizacao p/ prompt
    def texto_empresa(self) -> str:
        ordem = [
            ("Nome", "nome"),
            ("Tipo", "tipo"),
            ("Descricao", "descricao_curta"),
            ("Cidade", "cidade"),
            ("Regiao de atendimento", "regiao_atendimento"),
            ("Site", "site"),
            ("E-mail de contato", "email_contato"),
            ("WhatsApp oficial", "whatsapp_oficial"),
            ("Horario de atendimento", "horario_atendimento"),
            ("Prazo medio de resposta", "prazo_medio_resposta"),
            ("Como trabalhamos", "como_trabalhamos"),
            ("Diferenciais", "diferenciais"),
            ("Assuntos fora do escopo do agente", "fora_do_escopo"),
        ]
        return "\n".join(f"- {rotulo}: {_valor(self.empresa.get(chave))}" for rotulo, chave in ordem)

    def texto_servicos(self) -> str:
        blocos = []
        for s in self.servicos:
            blocos.append(
                "\n".join(
                    [
                        f"### {s['nome']} (id: {s['id']})",
                        f"- O que e: {_valor(s.get('resumo'))}",
                        f"- Para quem: {_valor(s.get('para_quem'))}",
                        f"- Inclui: {_valor(s.get('inclui'))}",
                        f"- Nao inclui: {_valor(s.get('nao_inclui'))}",
                        f"- Prazo: {_valor(s.get('prazo'))}",
                        f"- Preco: {_valor(s.get('preco'))}",
                    ]
                )
            )
        return "\n\n".join(blocos)

    def texto_faq(self) -> str:
        return "\n\n".join(
            f"P: {item['pergunta']}\nR: {str(item['resposta']).strip()}" for item in self.faq
        )

    def texto_campos_qualificacao(self) -> str:
        linhas = []
        for campo in self.qualificacao["campos"]:
            marca = "obrigatorio" if campo.get("obrigatorio") else "opcional"
            pergunta = campo.get("pergunta") or "(deduzir da conversa, nao perguntar direto)"
            linhas.append(f"- {campo['id']} ({marca}): {pergunta}")
        return "\n".join(linhas)

    def texto_perguntas_por_servico(self) -> str:
        blocos = []
        for s in self.servicos:
            perguntas = s.get("perguntas_chave") or []
            if perguntas:
                itens = "\n".join(f"  - {p}" for p in perguntas)
                blocos.append(f"- {s['nome']}:\n{itens}")
        return "\n".join(blocos)

    def texto_gatilhos_handoff(self) -> str:
        return "\n".join(
            f"- **{g['id']}**: {g['descricao']}" for g in self.qualificacao["gatilhos_handoff"]
        )
