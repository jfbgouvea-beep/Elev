"""Fluxo completo sem chamar a API: conversa, handoff e gravacao."""

import re

from elev.agente import AgenteElev
from elev.armazenamento import listar_leads, registrar_lead, salvar_registro


def test_saudacao_cita_a_empresa(config):
    agente = AgenteElev.novo(config)
    assert "ELEV" in agente.saudacao()


def test_pedido_de_humano_dispara_handoff(config):
    agente = AgenteElev.novo(config)
    resposta = agente.responder("quero falar com um atendente")
    assert resposta.handoff is True
    assert resposta.motivo_handoff == "pedido_explicito"
    assert agente.handoff is True


def test_pergunta_de_preco_usa_a_tabela_cadastrada(config):
    """Preco agora existe na base: o agente pode citar, mas so o que esta cadastrado."""
    agente = AgenteElev.novo(config)
    texto = agente.responder("quanto custa um site?").texto

    assert "R$ 150" in texto, "deve citar o valor inicial cadastrado do site basico"
    assert "escopo" in texto.lower(), "deve deixar claro que a faixa depende do escopo"

    # todo valor citado precisa existir na tabela - nada de numero novo
    cadastrados = {100, 150, 180, 250, 300, 400, 500, 600}
    citados = {int(v) for v in re.findall(r"R\$\s*(\d+)", texto)}
    assert citados <= cadastrados, f"valores fora da tabela: {citados - cadastrados}"


def test_negociacao_dispara_handoff(config):
    agente = AgenteElev.novo(config)
    assert agente.responder("quero fechar, me da um desconto?").motivo_handoff == "negociacao"


def test_historico_guarda_os_dois_lados(config):
    agente = AgenteElev.novo(config)
    agente.responder("oi")
    assert [m["role"] for m in agente.mensagens] == ["user", "assistant"]


def test_registro_grava_conversa_e_lead(config):
    agente = AgenteElev.novo(config)
    agente.responder("tenho uma barbearia e quero agendamento online")
    registro = agente.registro(agente.extrair_lead())

    caminho = salvar_registro(registro, config.dir_dados)
    registrar_lead(registro, config.dir_dados)

    assert caminho.exists()
    leads = listar_leads(config.dir_dados)
    assert len(leads) == 1 and leads[0]["id_conversa"] == agente.id_conversa
