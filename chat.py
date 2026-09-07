#!/usr/bin/env python3
"""Conversa com o ELEV AI pelo terminal.

    python chat.py              # usa a API (precisa de ANTHROPIC_API_KEY)
    python chat.py --offline    # testa o fluxo sem chamar a API
    python chat.py --checar     # so valida a base de conhecimento e sai

Comandos dentro da conversa: /lead  /base  /salvar  /sair
"""

from __future__ import annotations

import argparse
import sys

from elev.agente import AgenteElev
from elev.armazenamento import registrar_lead, salvar_registro
from elev.config import carregar_config
from elev.conhecimento import BaseInvalida, Conhecimento
from elev.lead import Lead

VERDE, CINZA, AMARELO, RESET = "\033[92m", "\033[90m", "\033[93m", "\033[0m"


def checar_base(cfg) -> int:
    try:
        base = Conhecimento.carregar(cfg.dir_conhecimento)
    except BaseInvalida as erro:
        print(f"Base invalida: {erro}")
        return 1
    print(f"Base OK - {len(base.servicos)} servicos, {len(base.faq)} perguntas no FAQ.")
    lacunas = base.lacunas()
    if lacunas:
        print(f"\n{AMARELO}{len(lacunas)} campos ainda nao cadastrados{RESET} "
              "(o agente vai dizer que verifica com a equipe):")
        for item in lacunas:
            print(f"  - {item}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="ELEV AI - atendimento pelo terminal")
    parser.add_argument("--offline", action="store_true", help="nao chama a API")
    parser.add_argument("--checar", action="store_true", help="valida a base e sai")
    args = parser.parse_args()

    cfg = carregar_config(offline=True if args.offline else None)
    if args.checar:
        return checar_base(cfg)

    try:
        agente = AgenteElev.novo(cfg, canal="terminal")
    except BaseInvalida as erro:
        print(f"Base invalida: {erro}")
        return 1

    modo = "offline (sem IA)" if cfg.offline else f"modelo {cfg.modelo}"
    print(f"{CINZA}ELEV AI - {modo} - conversa {agente.id_conversa}{RESET}")
    if cfg.offline and not args.offline:
        print(f"{AMARELO}Sem ANTHROPIC_API_KEY: rodando offline. "
              f"Configure a chave no .env para usar o agente de verdade.{RESET}")
    print(f"{CINZA}Comandos: /lead /base /salvar /sair{RESET}\n")
    print(f"{VERDE}Agente:{RESET} {agente.saudacao()}\n")

    lead = Lead()
    while True:
        try:
            entrada = input("Voce: ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if not entrada:
            continue

        if entrada in {"/sair", "/quit", "/exit"}:
            break
        if entrada == "/base":
            checar_base(cfg)
            continue
        if entrada == "/lead":
            lead = agente.extrair_lead()
            reg = agente.registro(lead)
            print(f"{CINZA}{reg.model_dump_json(indent=2, include={'lead','pontuacao','temperatura'})}{RESET}\n")
            continue
        if entrada == "/salvar":
            lead = agente.extrair_lead()
            reg = agente.registro(lead)
            print(f"{CINZA}Conversa: {salvar_registro(reg, cfg.dir_dados)}{RESET}")
            print(f"{CINZA}Lead: {registrar_lead(reg, cfg.dir_dados)}{RESET}\n")
            continue

        try:
            resposta = agente.responder(entrada)
        except Exception as erro:  # rede, credencial, limite - nao derruba a conversa
            print(f"{AMARELO}[erro ao falar com a API: {type(erro).__name__}: {erro}]{RESET}\n")
            continue

        print(f"\n{VERDE}Agente:{RESET} {resposta.texto}")
        if resposta.handoff:
            print(f"{AMARELO}[encaminhar para a equipe - motivo: {resposta.motivo_handoff}]{RESET}")
            if resposta.resumo_para_equipe:
                print(f"{CINZA}[resumo: {resposta.resumo_para_equipe}]{RESET}")
        if not cfg.offline:
            print(f"{CINZA}[tokens entrada {resposta.tokens_entrada} / saida "
                  f"{resposta.tokens_saida} / cache {resposta.tokens_cache_lidos}]{RESET}")
        print()

    if agente.mensagens:
        lead = agente.extrair_lead()
        reg = agente.registro(lead)
        salvar_registro(reg, cfg.dir_dados)
        registrar_lead(reg, cfg.dir_dados)
        print(f"{CINZA}Conversa salva em {cfg.dir_dados} "
              f"(lead {reg.temperatura}, pontuacao {reg.pontuacao}).{RESET}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
