"""Monta o system prompt do agente a partir do arquivo de instrucoes + base."""

from __future__ import annotations

from pathlib import Path

from .conhecimento import Conhecimento

ARQUIVO_INSTRUCOES = "agente_elev.md"


def montar_system_prompt(base: Conhecimento, dir_prompts: Path) -> str:
    """Substitui os marcadores {{...}} do arquivo de instrucoes pelos dados reais.

    O resultado e deterministico: mesmo conhecimento -> mesmo prompt, byte a byte.
    Isso e o que permite o cache de prompt funcionar entre chamadas.
    """
    caminho = dir_prompts / ARQUIVO_INSTRUCOES
    template = caminho.read_text(encoding="utf-8")

    substituicoes = {
        "{{EMPRESA}}": base.texto_empresa(),
        "{{SERVICOS}}": base.texto_servicos(),
        "{{FAQ}}": base.texto_faq(),
        "{{CAMPOS_QUALIFICACAO}}": base.texto_campos_qualificacao(),
        "{{PERGUNTAS_POR_SERVICO}}": base.texto_perguntas_por_servico(),
        "{{GATILHOS_HANDOFF}}": base.texto_gatilhos_handoff(),
    }

    prompt = template
    for marcador, valor in substituicoes.items():
        prompt = prompt.replace(marcador, valor)

    restantes = [m for m in substituicoes if m in prompt]
    if restantes:  # pragma: no cover - so acontece se o .md for editado errado
        raise ValueError(f"Marcadores nao substituidos: {restantes}")
    if "{{" in prompt:
        sobra = prompt[prompt.index("{{") : prompt.index("{{") + 40]
        raise ValueError(f"Marcador desconhecido no arquivo de instrucoes: {sobra}")

    return prompt
