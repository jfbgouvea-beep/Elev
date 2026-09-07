"""Configuracao central do ELEV AI.

Tudo que muda entre ambientes (modelo, chave, caminhos) passa por aqui.
Nada de valor magico espalhado pelo codigo.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent


def _carregar_dotenv(caminho: Path) -> None:
    """Le um .env simples (CHAVE=valor) sem depender de biblioteca externa."""
    if not caminho.exists():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, _, valor = linha.partition("=")
        os.environ.setdefault(chave.strip(), valor.strip().strip('"').strip("'"))


@dataclass
class Config:
    """Parametros de execucao do agente."""

    # Modelo. Opus 5 e o padrao; para reduzir custo em producao troque por
    # claude-sonnet-5 em ELEV_MODEL e meca a diferenca de qualidade antes.
    modelo: str = field(default_factory=lambda: os.getenv("ELEV_MODEL", "claude-opus-5"))

    # Esforco de raciocinio: atendimento e conversa, nao precisa de esforco alto.
    esforco_conversa: str = field(default_factory=lambda: os.getenv("ELEV_ESFORCO", "low"))
    esforco_extracao: str = "medium"

    # Respostas de atendimento sao curtas de proposito.
    max_tokens_conversa: int = 2000
    max_tokens_extracao: int = 4000

    dir_conhecimento: Path = RAIZ / "conhecimento"
    dir_prompts: Path = RAIZ / "prompts"
    dir_dados: Path = field(
        default_factory=lambda: Path(os.getenv("ELEV_DIR_DADOS", str(RAIZ / "data")))
    )

    # Sem chave de API o agente roda em modo offline (respostas montadas a
    # partir da base de conhecimento, sem chamar a API). Serve para testar o
    # fluxo sem gastar credito.
    offline: bool = False

    def __post_init__(self) -> None:
        self.dir_dados.mkdir(parents=True, exist_ok=True)

    @property
    def tem_credencial(self) -> bool:
        return bool(os.getenv("ANTHROPIC_API_KEY") or os.getenv("ANTHROPIC_AUTH_TOKEN"))


def carregar_config(offline: bool | None = None) -> Config:
    """Monta a configuracao lendo .env e variaveis de ambiente."""
    _carregar_dotenv(RAIZ / ".env")
    cfg = Config()
    cfg.offline = (not cfg.tem_credencial) if offline is None else offline
    return cfg
