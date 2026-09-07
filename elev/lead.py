"""Modelo do lead: o que o agente descobre na conversa e como priorizamos."""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field


class Lead(BaseModel):
    """Informacoes extraidas de uma conversa. Campo nao descoberto fica None."""

    nome: str | None = Field(None, description="Nome do interessado, se ele disse")
    negocio: str | None = Field(None, description="O que o negocio dele faz")
    necessidade: str | None = Field(None, description="O problema ou objetivo, nas palavras dele")
    servico_de_interesse: str | None = Field(
        None, description="id do servico da ELEV mais aderente, ou None se ainda nao esta claro"
    )
    situacao_atual: str | None = Field(None, description="Como ele resolve isso hoje")
    prazo_desejado: str | None = Field(None, description="Quando ele quer isso funcionando")
    decisor: bool | None = Field(None, description="True se a decisao e dele")
    contato: str | None = Field(None, description="Telefone, e-mail ou WhatsApp informado")
    resumo: str | None = Field(None, description="Resumo da conversa em ate 3 frases")
    pendencias: list[str] = Field(
        default_factory=list,
        description="Perguntas do cliente que ficaram sem resposta e a equipe precisa responder",
    )

    # ------------------------------------------------------------ priorizacao
    def pontuacao(self, pesos: dict[str, int]) -> int:
        total = 0
        if self.necessidade:
            total += pesos.get("necessidade_clara", 0)
        if self.servico_de_interesse:
            total += pesos.get("servico_identificado", 0)
        if self.contato:
            total += pesos.get("contato_informado", 0)
        if self.prazo_desejado:
            total += pesos.get("prazo_definido", 0)
        if self.decisor:
            total += pesos.get("e_o_decisor", 0)
        return min(total, 100)

    def temperatura(self, pesos: dict[str, int], faixas: dict[str, int]) -> Literal["quente", "morno", "frio"]:
        p = self.pontuacao(pesos)
        if p >= faixas.get("quente", 70):
            return "quente"
        if p >= faixas.get("morno", 40):
            return "morno"
        return "frio"

    def campos_faltando(self, obrigatorios: list[str]) -> list[str]:
        return [c for c in obrigatorios if getattr(self, c, None) in (None, "", [])]


class RegistroConversa(BaseModel):
    """O que fica gravado ao final de um atendimento."""

    id_conversa: str
    iniciada_em: str
    encerrada_em: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    canal: str = "terminal"
    mensagens: list[dict] = Field(default_factory=list)
    lead: Lead = Field(default_factory=Lead)
    pontuacao: int = 0
    temperatura: str = "frio"
    handoff: bool = False
    motivo_handoff: str | None = None
