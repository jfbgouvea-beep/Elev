# Site da ELEV

Pagina unica, sem build: e um `index.html` com CSS e JS dentro. Publica em
qualquer lugar arrastando a pasta `site/`.

## Ver localmente

```bash
python3 -m http.server 8080 --directory site
# abre http://localhost:8080
```

## Onde esta publicado

Netlify, conectado a este repositorio (`netlify.toml` na raiz serve a pasta
`site/` direto). Todo push que altere `site/` republica sozinho.

## O que voce precisa preencher

### 1. A logo oficial

```
site/assets/logo-elev.png      (ou .svg - ajuste o src no index.html)
```

A logo aparece em quatro lugares: header, hero, faixa de diagnostico e rodape.
Enquanto o arquivo nao existir, esses pontos mostram o nome ELEV em tipografia,
e o JS troca sozinho assim que o arquivo aparecer. Fundo transparente funciona
melhor no tema escuro.

### 2. Dados institucionais do rodape

Procure `data-rodape-pendente` no `index.html` e troque por cidade e CNPJ.

### 3. Contatos (ja preenchidos)

No bloco `const CONTATO`, perto do fim do `index.html`. Se algum ficar vazio, os
botoes daquele canal aparecem marcados como pendentes em vez de virar link morto.

## Como o site esta organizado

| Secao | id | O que faz |
|---|---|---|
| Hero | `inicio` | Proposta principal e os dois botoes de entrada |
| ELEV Lab | `elev-lab` | Raio-X, Desafio e Forge - o coracao da proposta |
| Solucoes | `solucoes` | Trilhas por tipo de negocio (exemplos, nao clientes) |
| Servicos | `servicos` | Quatro frentes, cada uma expansivel |
| Precos | `precos` | Quatro familias em abas, tres niveis cada |
| Simulador | `simulador` | Monta a solucao e soma a estimativa inicial |
| Como funciona | `processo` | Cinco etapas |
| Por que a ELEV | `por-que` | Quatro diferenciais |
| Demonstracoes | `demos` | Wireframes marcados como demonstracao |
| Contato | `contato` | Formulario que monta a mensagem pronta |
| FAQ | `faq` | Seis perguntas |

## Precos: onde mexer

Os valores vivem em **um lugar so** dentro de cada card de preco
(`data-preco` no `.plano`). O botao de WhatsApp de cada plano e o texto da
mensagem sao montados a partir dai, entao nao existe risco de o card mostrar um
valor e a mensagem enviar outro.

O simulador tem a propria lista (`data-preco` em cada `.opcao`), porque inclui
itens que nao estao na tabela. Item com `data-preco="0"` aparece como **a orcar**
- e assim que o site evita inventar valor.

Os mesmos precos estao em `conhecimento/servicos.yaml` e `conhecimento/faq.yaml`,
que alimentam o agente ELEV AI. **Mudou preco: mude nos dois lugares**, senao o
agente e o site passam a dizer coisas diferentes.

## O que NAO tem no site (de proposito)

Nenhum cliente, depoimento, numero de resultado, estatistica ou case. Nada disso
existe de forma verificada. As quatro pecas da secao de demonstracoes estao
marcadas como demonstracao no card e no aviso acima delas.

## Formulario

Nao ha backend. Ao enviar, o site valida os dois campos essenciais, monta a
mensagem com tudo que foi escrito e oferece dois caminhos: abrir o WhatsApp da
ELEV com a mensagem pronta, ou abrir o e-mail. Nenhum dado sai do navegador do
visitante sem ele mandar.
