"""O prompt e montado a partir da base - nada de fato escrito a mao nele."""

from pathlib import Path

from elev.prompt import montar_system_prompt

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"


def test_prompt_nao_deixa_marcador(base):
    prompt = montar_system_prompt(base, PROMPTS)
    assert "{{" not in prompt


def test_prompt_traz_todos_os_servicos(base):
    prompt = montar_system_prompt(base, PROMPTS)
    for servico in base.servicos:
        assert servico["nome"] in prompt


def test_prompt_traz_regra_anti_invencao(base):
    prompt = montar_system_prompt(base, PROMPTS).lower()
    assert "verificar com a equipe" in prompt
    assert "nunca" in prompt


def test_prompt_traz_gatilhos_de_handoff(base):
    prompt = montar_system_prompt(base, PROMPTS)
    for gatilho in base.ids_gatilhos:
        assert gatilho in prompt


def test_prompt_e_deterministico(base):
    """Prompt identico entre chamadas = cache de prompt funciona = menos custo."""
    assert montar_system_prompt(base, PROMPTS) == montar_system_prompt(base, PROMPTS)
