"""Modo offline: responde sem chamar a API.

Serve para testar o fluxo (CLI, web, gravacao de lead) sem credencial e sem
gastar credito. As respostas saem direto da base de conhecimento, por
correspondencia de palavras - nao ha geracao de texto nova, e por isso mesmo
nao ha risco de invencao. Nao substitui o agente de verdade.
"""

from __future__ import annotations

import re
import unicodedata

from .conhecimento import Conhecimento

PEDIDOS_DE_HUMANO = {"humano", "atendente", "pessoa", "vendedor", "responsavel", "gerente"}
TERMOS_NEGOCIACAO = {"desconto", "fechar", "contrato", "pagamento", "parcelar", "proposta"}


def _normalizar(texto: str) -> str:
    texto = unicodedata.normalize("NFKD", texto.lower())
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9\s]", " ", texto)


def _palavras(texto: str) -> set[str]:
    return set(_normalizar(texto).split())


def _casa(palavras: set[str], alvos: set[str], minimo: int = 4) -> bool:
    """Compara por radical: 'agendamentos' casa com 'agendamento', 'sites' com 'site'."""
    for palavra in palavras:
        if len(palavra) < minimo:
            continue
        for alvo in alvos:
            if len(alvo) >= minimo and (palavra.startswith(alvo) or alvo.startswith(palavra)):
                return True
    return False


def responder_offline(base: Conhecimento, mensagem: str):
    """Devolve um objeto Resposta montado a partir da base."""
    from .agente import Resposta  # import tardio: evita ciclo

    palavras = _palavras(mensagem)
    aviso = "\n\n[modo offline - resposta montada a partir da base, sem IA]"

    if palavras & PEDIDOS_DE_HUMANO:
        return Resposta(
            texto="Claro, vou chamar alguem da equipe da ELEV. Qual o melhor contato para te retornarem?" + aviso,
            handoff=True,
            motivo_handoff="pedido_explicito",
        )

    if palavras & TERMOS_NEGOCIACAO:
        return Resposta(
            texto="Valores e condicoes quem trata e a equipe. Vou encaminhar seu contato para eles." + aviso,
            handoff=True,
            motivo_handoff="negociacao",
        )

    for item in base.faq:
        if _casa(palavras, {_normalizar(t).strip() for t in item.get("tags", [])}):
            return Resposta(texto=str(item["resposta"]).strip() + aviso)

    for servico in base.servicos:
        alvo = _palavras(f"{servico['id']} {servico['nome']}")
        if _casa(palavras, alvo):
            perguntas = servico.get("perguntas_chave") or []
            texto = str(servico["resumo"]).strip()
            if perguntas:
                texto += f"\n\n{perguntas[0]}"
            return Resposta(texto=texto + aviso)

    nomes = ", ".join(s["nome"] for s in base.servicos)
    return Resposta(
        texto=(
            f"A {base.empresa['nome']} trabalha com: {nomes}.\n\n"
            "Me conta um pouco sobre o seu negocio e o que voce quer resolver?" + aviso
        )
    )
