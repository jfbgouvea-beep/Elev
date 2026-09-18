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
| Social Media | `social` | Nove servicos + o Pacote de Conteudo de R$ 300 |
| Design | `design` | Oito servicos + mockups marcados como exemplo |
| ELEV Orcamento | `orcamento` | Conversa guiada que estima a partir da tabela |
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

O ELEV Orcamento **le os precos do proprio HTML dos cards** ao carregar a pagina
(`PRECOS` e montado a partir de `.plano[data-familia]`). Mudou o card, mudou a
estimativa - nao existe segunda copia dos valores para desatualizar. A unica
excecao e o Pacote de Conteudo (R$ 300), que fica em `PRECOS.pacoteConteudo`
porque nao tem card de preco proprio.

### Como o ELEV Orcamento decide

Nao e IA externa: e uma maquina de regras local e deterministica, em
`PERGUNTAS` + `estimar()`. O fluxo:

1. Pergunta segmento, problema e o que a pessoa acha que precisa.
2. Se marcou Social Media, abre as perguntas de redes, tempo e quantidade.
3. Se marcou algo com niveis, pergunta a complexidade.
4. `estimar()` cruza as escolhas com `PRECOS`: item com tabela soma o nivel
   escolhido; item sem tabela entra como **a orcar**; nada reconhecido vira
   **orcamento personalizado** com a lista de fatores que influenciam o valor.
5. A combinacao exata de 10 Reels + 2 semanas e reconhecida como o Pacote de
   Conteudo de R$ 300. Qualquer outro volume vira orcamento proprio, porque nao
   existe tabela para ele.

Tudo sai rotulado como **estimativa inicial**, com a ressalva de que o valor
final depende da complexidade. Para plugar uma IA de verdade depois, o ponto de
entrada e `estimar()`: mesma entrada, mesma saida.

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

## Demonstrações

Sete demos independentes em `site/demos/`, cada uma com identidade visual
propria e empresa ficticia. Todas carregam `assets/demo.css` e `assets/demo.js`,
que trazem a barra "Projeto demonstrativo ELEV", o modal e os utilitarios
comuns - o que evita repetir codigo em sete arquivos.

| Pasta | Empresa ficticia | O que demonstra |
|---|---|---|
| `social/` | Brisa Cafe | Perfil com feed, Reels, destaques, post ampliado e o pacote de R$ 300 |
| `design/` | Nomade Studio | Identidade visual, galeria de pecas com visualizacao ampliada |
| `ai/` | Mecanica Trilho | Agente que le texto livre, identifica intencao, qualifica e resume |
| `automacao/` | — | Fluxo do lead executando passo a passo, com classificacao |
| `agendamento/` | Studio Aurora | Fluxo do cliente em 5 passos + painel do salao |
| `institucional/` | Vertice Engenharia | Site completo: hero, servicos, sobre, formulario, CTA |
| `catalogo/` | Verde Vivo | 12 produtos, busca, filtros, pagina de produto e carrinho |

Para criar uma demo nova: copie a pasta mais parecida, troque os tokens `--d-*`
no `<style>` (e a fonte) e ajuste os dados no `<script>`. A barra ELEV entra
sozinha pelo `data-demo` da tag de script.

### Regra das demos

Empresas, numeros, avaliacoes e conteudos sao **ficticios**. Cada demo diz isso
no proprio corpo, alem da barra fixa no topo. Nenhuma pode ser apresentada como
cliente real da ELEV.
