import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))

from elev.config import Config  # noqa: E402
from elev.conhecimento import Conhecimento  # noqa: E402


@pytest.fixture
def base() -> Conhecimento:
    return Conhecimento.carregar(RAIZ / "conhecimento")


@pytest.fixture
def config(tmp_path) -> Config:
    cfg = Config(dir_dados=tmp_path)
    cfg.offline = True
    return cfg
