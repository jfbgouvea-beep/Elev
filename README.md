# ELEV AI

Agente de atendimento da ELEV. Esta versao roda **localmente**, no terminal ou
no navegador. WhatsApp e etapa posterior - o objetivo agora e ter certeza de que
o cerebro responde certo antes de conectar qualquer canal.

## Instalar e rodar

```bash
pip install -r requirements.txt
cp .env.example .env          # coloque sua ANTHROPIC_API_KEY

python chat.py                # conversa no terminal
python web.py                 # http://localhost:8000
python chat.py --checar       # valida a base e lista o que falta cadastrar
python chat.py --offline      # testa o fluxo sem chamar a API (sem custo)
python -m pytest tests -q     # 23 testes
```

Sem `ANTHROPIC_API_KEY` o sistema entra em modo offline sozinho: responde a
partir da base por correspondencia de palavras, sem IA. Serve para testar o
fluxo, nao para avaliar a qualidade das respostas.

## Estrutura

```
conhecimento/          A VERDADE. Editar aqui muda o que o agente sabe.
  empresa.yaml           dados institucionais
  servicos.yaml          catalogo, com preco e prazo em null de proposito
  faq.yaml               perguntas com resposta oficial
  qualificacao.yaml      o que perguntar, como pontuar, quando chamar humano
prompts/
  agente_elev.md       O COMPORTAMENTO. Tom, regras, o que nunca fazer.
elev/
  config.py              modelo, chaves, caminhos
  conhecimento.py        carrega, valida e marca o que nao esta cadastrado
  prompt.py              junta instrucoes + base num system prompt
  agente.py              a conversa e a ferramenta de encaminhamento
  offline.py             motor sem IA, para teste
  lead.py                dados do interessado, pontuacao, temperatura
  armazenamento.py       gravacao em data/
chat.py                Interface de terminal
web.py                 Interface local no navegador
docs/roteiro_de_teste.md  Casos para conferir antes de confiar no agente
data/                  Conversas e leads gravados (fora do git)
```

A separacao importante: **fato fica em YAML, comportamento fica no Markdown,
codigo nao contem nem um nem outro.** Atualizar preco nao exige mexer em Python.

## Como o sistema evita inventar informacao

Tres camadas, porque prompt sozinho nao segura:

1. **Base fechada.** O prompt e montado a partir dos YAMLs. Campo `null` vira
   literalmente `NAO CADASTRADO - responder que precisa verificar com a equipe`
   dentro do prompt. O agente le a ausencia, nao a adivinha.
2. **Regra explicita.** `prompts/agente_elev.md` proibe estimar preco, prazo e
   funcionalidade, com exemplo de resposta correta.
3. **Saida de emergencia.** A ferramenta `encaminhar_para_humano` da ao agente
   uma alternativa melhor do que chutar quando ele nao sabe.

Nenhuma das tres e infalivel sozinha. Por isso existe
`docs/roteiro_de_teste.md`: os casos que voce deve rodar antes de confiar.

## Cadastrar informacao nova

1. Achou uma lacuna: `python chat.py --checar` lista tudo que esta `null`.
2. Preencha no YAML correspondente.
3. `python -m pytest tests -q` para garantir que a base continua valida.
4. Rode o roteiro de teste na parte afetada.

Nunca preencha um campo com estimativa. Campo vazio faz o agente encaminhar;
campo errado faz o agente mentir com confianca.

## O que ainda nao existe

- Integracao com WhatsApp (proposital - proxima etapa)
- Banco de dados (hoje e JSON em `data/`)
- Painel para a equipe ver os leads
- Memoria entre conversas do mesmo cliente
- Avaliacao automatica das respostas contra casos esperados
