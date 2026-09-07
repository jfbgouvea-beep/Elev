"""O agente de atendimento da ELEV.

Responsabilidade unica: dado o historico da conversa, produzir a proxima
mensagem e sinalizar se o atendimento deve ir para uma pessoa da equipe.
Nao sabe nada sobre terminal, web ou WhatsApp - quem chama e que decide isso.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

import anthropic

from .config import Config
from .conhecimento import Conhecimento
from .lead import Lead, RegistroConversa
from .offline import responder_offline
from .prompt import montar_system_prompt

# A unica ferramenta do agente: pedir socorro humano. Deliberadamente estreita -
# o agente decide QUANDO encaminhar; o que fazer com isso e do sistema.
FERRAMENTA_HANDOFF = {
    "name": "encaminhar_para_humano",
    "description": (
        "Registra que este atendimento precisa de uma pessoa da equipe da ELEV. "
        "Chame assim que um dos gatilhos de encaminhamento acontecer. Depois de "
        "chamar, escreva a mensagem que o cliente vai ler explicando o proximo passo."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "motivo": {
                "type": "string",
                "description": "id do gatilho de encaminhamento que se aplica",
            },
            "urgencia": {"type": "string", "enum": ["normal", "alta"]},
            "resumo_para_equipe": {
                "type": "string",
                "description": "Resumo objetivo do caso, em ate 3 frases, para quem vai assumir.",
            },
        },
        "required": ["motivo", "urgencia", "resumo_para_equipe"],
        "additionalProperties": False,
    },
}


@dataclass
class Resposta:
    """Uma resposta do agente, com os sinais que o sistema precisa."""

    texto: str
    handoff: bool = False
    motivo_handoff: str | None = None
    urgencia: str | None = None
    resumo_para_equipe: str | None = None
    tokens_entrada: int = 0
    tokens_saida: int = 0
    tokens_cache_lidos: int = 0


@dataclass
class AgenteElev:
    """Mantem o estado de UMA conversa."""

    config: Config
    base: Conhecimento
    canal: str = "terminal"
    mensagens: list[dict] = field(default_factory=list)
    id_conversa: str = field(default_factory=lambda: uuid4().hex[:12])
    iniciada_em: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    handoff: bool = False
    motivo_handoff: str | None = None
    _system: str = field(init=False, default="")
    _cliente: anthropic.Anthropic | None = field(init=False, default=None)

    def __post_init__(self) -> None:
        self._system = montar_system_prompt(self.base, self.config.dir_prompts)
        if not self.config.offline:
            self._cliente = anthropic.Anthropic()

    # ------------------------------------------------------------------ util
    @classmethod
    def novo(cls, config: Config, canal: str = "terminal") -> "AgenteElev":
        return cls(config=config, base=Conhecimento.carregar(config.dir_conhecimento), canal=canal)

    @property
    def system_blocks(self) -> list[dict]:
        # Bloco estavel + cache: o prompt nao muda entre turnos, entao a partir
        # da segunda mensagem ele e lido do cache em vez de recobrado inteiro.
        return [{"type": "text", "text": self._system, "cache_control": {"type": "ephemeral"}}]

    def saudacao(self) -> str:
        nome = self.base.empresa["nome"]
        return (
            f"Oi! Eu sou o assistente digital da {nome}. "
            "Posso te explicar o que a gente faz e entender o que voce precisa. "
            "Como voce se chama?"
        )

    # -------------------------------------------------------------- conversa
    def responder(self, mensagem_cliente: str) -> Resposta:
        """Recebe a mensagem do cliente e devolve a proxima fala do agente."""
        self.mensagens.append({"role": "user", "content": mensagem_cliente})

        if self.config.offline:
            resposta = responder_offline(self.base, mensagem_cliente)
        else:
            resposta = self._responder_via_api()

        self.mensagens.append({"role": "assistant", "content": resposta.texto})
        if resposta.handoff:
            self.handoff = True
            self.motivo_handoff = resposta.motivo_handoff
        return resposta

    def _responder_via_api(self) -> Resposta:
        assert self._cliente is not None
        resposta = Resposta(texto="")
        historico = [{"role": m["role"], "content": m["content"]} for m in self.mensagens]

        # Loop de ferramenta: no maximo 2 voltas (chamar handoff + responder).
        for _ in range(3):
            msg = self._cliente.messages.create(
                model=self.config.modelo,
                max_tokens=self.config.max_tokens_conversa,
                system=self.system_blocks,
                messages=historico,
                tools=[FERRAMENTA_HANDOFF],
                thinking={"type": "adaptive"},
                output_config={"effort": self.config.esforco_conversa},
            )
            resposta.tokens_entrada += msg.usage.input_tokens
            resposta.tokens_saida += msg.usage.output_tokens
            resposta.tokens_cache_lidos += getattr(msg.usage, "cache_read_input_tokens", 0) or 0

            texto = "".join(b.text for b in msg.content if b.type == "text").strip()
            chamadas = [b for b in msg.content if b.type == "tool_use"]

            if not chamadas:
                resposta.texto = texto
                return resposta

            # O modelo pediu encaminhamento: registramos e devolvemos o resultado
            # para ele fechar a conversa com o cliente.
            historico.append({"role": "assistant", "content": msg.content})
            resultados = []
            for chamada in chamadas:
                if chamada.name == "encaminhar_para_humano":
                    resposta.handoff = True
                    resposta.motivo_handoff = chamada.input.get("motivo")
                    resposta.urgencia = chamada.input.get("urgencia")
                    resposta.resumo_para_equipe = chamada.input.get("resumo_para_equipe")
                    conteudo = (
                        "Encaminhamento registrado para a equipe da ELEV. "
                        "Agora escreva a mensagem para o cliente confirmando o proximo passo, "
                        "sem prometer horario que nao esteja cadastrado."
                    )
                else:  # pragma: no cover - nao ha outras ferramentas hoje
                    conteudo = "Ferramenta desconhecida."
                resultados.append(
                    {"type": "tool_result", "tool_use_id": chamada.id, "content": conteudo}
                )
            historico.append({"role": "user", "content": resultados})

        resposta.texto = (
            "Deixa eu chamar alguem da equipe para te ajudar melhor com isso. "
            "Qual o melhor contato para te retornarem?"
        )
        resposta.handoff = True
        resposta.motivo_handoff = resposta.motivo_handoff or "informacao_ausente"
        return resposta

    # -------------------------------------------------------------- extracao
    def extrair_lead(self) -> Lead:
        """Le a conversa inteira e devolve os dados estruturados do interessado."""
        if self.config.offline or not self.mensagens:
            return Lead()

        assert self._cliente is not None
        transcricao = "\n".join(
            f"{'Cliente' if m['role'] == 'user' else 'Agente'}: {m['content']}"
            for m in self.mensagens
            if isinstance(m.get("content"), str)
        )
        instrucao = (
            "Extraia os dados do interessado a partir da conversa abaixo.\n"
            "Regras: preencha APENAS o que o cliente disse de fato. O que ele nao "
            "disse fica null - nao deduza, nao complete, nao invente contato.\n"
            f"O campo servico_de_interesse deve ser um destes ids ou null: "
            f"{', '.join(self.base.ids_servicos)}.\n\n"
            f"CONVERSA:\n{transcricao}"
        )
        msg = self._cliente.messages.parse(
            model=self.config.modelo,
            max_tokens=self.config.max_tokens_extracao,
            messages=[{"role": "user", "content": instrucao}],
            output_format=Lead,
            output_config={"effort": self.config.esforco_extracao},
        )
        return msg.parsed_output or Lead()

    # -------------------------------------------------------------- registro
    def registro(self, lead: Lead | None = None) -> RegistroConversa:
        lead = lead if lead is not None else Lead()
        pesos = self.base.qualificacao["pontuacao"]
        faixas = self.base.qualificacao["temperatura"]
        return RegistroConversa(
            id_conversa=self.id_conversa,
            iniciada_em=self.iniciada_em,
            canal=self.canal,
            mensagens=[m for m in self.mensagens if isinstance(m.get("content"), str)],
            lead=lead,
            pontuacao=lead.pontuacao(pesos),
            temperatura=lead.temperatura(pesos, faixas),
            handoff=self.handoff,
            motivo_handoff=self.motivo_handoff,
        )
