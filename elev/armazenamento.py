"""Gravacao das conversas e dos leads em disco.

Formato deliberadamente simples (JSON e JSONL): da para abrir no editor, no
Excel e para migrar para banco depois sem reescrever o agente.
"""

from __future__ import annotations

import json
from pathlib import Path

from .lead import RegistroConversa


def salvar_registro(registro: RegistroConversa, dir_dados: Path) -> Path:
    """Grava a conversa completa em data/conversas/<id>.json."""
    destino = dir_dados / "conversas"
    destino.mkdir(parents=True, exist_ok=True)
    caminho = destino / f"{registro.id_conversa}.json"
    caminho.write_text(
        json.dumps(registro.model_dump(), ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return caminho


def registrar_lead(registro: RegistroConversa, dir_dados: Path) -> Path:
    """Acrescenta uma linha em data/leads.jsonl - a fila de trabalho da equipe."""
    caminho = dir_dados / "leads.jsonl"
    linha = {
        "id_conversa": registro.id_conversa,
        "quando": registro.encerrada_em,
        "canal": registro.canal,
        "temperatura": registro.temperatura,
        "pontuacao": registro.pontuacao,
        "handoff": registro.handoff,
        "motivo_handoff": registro.motivo_handoff,
        **registro.lead.model_dump(),
    }
    with caminho.open("a", encoding="utf-8") as arquivo:
        arquivo.write(json.dumps(linha, ensure_ascii=False) + "\n")
    return caminho


def listar_leads(dir_dados: Path) -> list[dict]:
    caminho = dir_dados / "leads.jsonl"
    if not caminho.exists():
        return []
    return [json.loads(l) for l in caminho.read_text(encoding="utf-8").splitlines() if l.strip()]
