"""Pontuacao e temperatura decidem a ordem da fila da equipe."""

from elev.lead import Lead


def test_lead_vazio_e_frio(base):
    pesos, faixas = base.qualificacao["pontuacao"], base.qualificacao["temperatura"]
    assert Lead().temperatura(pesos, faixas) == "frio"


def test_lead_completo_e_quente(base):
    pesos, faixas = base.qualificacao["pontuacao"], base.qualificacao["temperatura"]
    lead = Lead(
        nome="Bruno", negocio="pizzaria", necessidade="cardapio online",
        servico_de_interesse="cardapio_digital", prazo_desejado="mes que vem",
        decisor=True, contato="11 90000-0000",
    )
    assert lead.pontuacao(pesos) == 100
    assert lead.temperatura(pesos, faixas) == "quente"


def test_pontuacao_nunca_passa_de_cem(base):
    pesos = {k: 90 for k in base.qualificacao["pontuacao"]}
    lead = Lead(necessidade="x", servico_de_interesse="sites", contato="y", prazo_desejado="z", decisor=True)
    assert lead.pontuacao(pesos) == 100


def test_campos_faltando(base):
    obrigatorios = [c["id"] for c in base.qualificacao["campos"] if c["obrigatorio"]]
    lead = Lead(nome="Bruno")
    faltando = lead.campos_faltando(obrigatorios)
    assert "contato" in faltando and "nome" not in faltando
