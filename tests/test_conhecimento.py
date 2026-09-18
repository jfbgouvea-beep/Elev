"""A base de conhecimento e a fonte da verdade - se ela quebra, o agente mente."""

import pytest
import yaml

from elev.conhecimento import NAO_CADASTRADO, BaseInvalida, Conhecimento


def test_base_real_carrega(base):
    assert base.empresa["nome"] == "ELEV"
    assert len(base.servicos) >= 5
    assert set(base.ids_servicos) >= {"sites", "cardapio_digital", "agendamento", "whatsapp", "ia"}


def test_todo_servico_tem_politica_de_preco(base):
    """Ou o servico tem tabela, ou diz explicitamente que e sob medida.
    O que nao pode existir e servico sem nenhuma orientacao de preco."""
    for servico in base.servicos:
        preco = (servico.get("preco") or "").lower()
        assert preco, f"{servico['id']} sem campo preco"
        assert "r$" in preco or "sob medida" in preco or "nao tem preco" in preco, \
            f"{servico['id']} com preco que nao orienta o agente"


def test_campo_vazio_vira_aviso_explicito(base):
    texto = base.texto_empresa()
    assert NAO_CADASTRADO in texto, "campo nao cadastrado precisa aparecer marcado no prompt"


def test_lacunas_listam_o_que_falta(base):
    """Prazo ainda nao foi definido pela ELEV: precisa aparecer como lacuna."""
    lacunas = base.lacunas()
    assert any(l.startswith("servicos.") and l.endswith(".prazo") for l in lacunas)
    assert "empresa.cidade" in lacunas


def test_base_sem_servicos_falha(tmp_path):
    (tmp_path / "empresa.yaml").write_text("nome: ELEV\n", encoding="utf-8")
    (tmp_path / "servicos.yaml").write_text("[]\n", encoding="utf-8")
    (tmp_path / "faq.yaml").write_text("[]\n", encoding="utf-8")
    (tmp_path / "qualificacao.yaml").write_text("campos: []\n", encoding="utf-8")
    with pytest.raises(BaseInvalida):
        Conhecimento.carregar(tmp_path)


def test_arquivo_faltando_falha(tmp_path):
    with pytest.raises(BaseInvalida):
        Conhecimento.carregar(tmp_path)


def test_todo_servico_tem_perguntas_de_qualificacao(base):
    for servico in base.servicos:
        assert servico.get("perguntas_chave"), f"{servico['id']} sem perguntas_chave"


def test_yaml_sem_erro_de_sintaxe():
    for nome in ("empresa", "servicos", "faq", "qualificacao"):
        with open(f"conhecimento/{nome}.yaml", encoding="utf-8") as f:
            assert yaml.safe_load(f) is not None
