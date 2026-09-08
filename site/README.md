# Site da ELEV

Página única, sem dependência de build: e um arquivo `index.html` com CSS e JS
dentro. Da para publicar em qualquer lugar (Vercel, Netlify, GitHub Pages,
hospedagem comum) arrastando a pasta `site/`.

## Onde o site esta publicado

Netlify, conectado a este repositorio. Qualquer push que altere `site/` publica
sozinho - nao existe passo manual de deploy.

A configuracao esta em `netlify.toml`, na raiz: o Netlify serve a pasta `site/`
direto, sem build.

## Ver localmente

```bash
python3 -m http.server 8080 --directory site
# abre http://localhost:8080
```

## O que voce precisa preencher

### 1. A logo oficial (importante)

Salve o arquivo da logo em:

```
site/assets/logo-elev.png      (ou .svg - se for svg, ajuste o src no index.html)
```

Enquanto o arquivo nao existir, o site mostra o nome ELEV em tipografia. Assim
que o arquivo aparecer, a logo entra sozinha no topo, no menu e no rodape - nao
precisa mexer em codigo. Fundo transparente funciona melhor no tema escuro.

### 2. Contatos

No `index.html`, procure o bloco `const CONTATO` (perto do fim do arquivo):

```js
const CONTATO = {
  whatsapp:  "",   // so numeros com DDI+DDD. Ex.: "5511999999999"
  email:     ""    // Ex.: "contato@elev.com.br"
};
```

Enquanto estiverem vazios, os dois botoes aparecem marcados como "a configurar"
com borda tracejada - de proposito, para nao virar link morto. Preencheu, eles
viram link de verdade na hora.

### 3. Dados institucionais do rodape

Procure `data-rodape-pendente` no `index.html` e troque o texto por cidade,
CNPJ e o que mais for oficial.

## Precos

A tabela da secao "Investimento" vem dos valores iniciais definidos pela ELEV.
Todos aparecem como "a partir de" com a faixa ao lado, e a nota abaixo da tabela
explica que o ponto exato depende do escopo e e confirmado por escrito.

Os mesmos valores estao em `conhecimento/servicos.yaml` e `conhecimento/faq.yaml`,
que alimentam o agente ELEV AI. **Mudou o preco: mude nos dois lugares**, senao o
agente e o site passam a dizer coisas diferentes.

## O que NAO tem no site (de proposito)

Nao ha cliente, depoimento, numero de resultado nem prazo. Nada disso existe
ainda de forma verificada, e inventar seria o pior erro possivel numa vitrine
comercial.

A secao de projetos demonstrativos foi retirada por decisao do Bruno - as demos
serao feitas depois. Quando existirem, entram entre "Investimento" e "Por que a
ELEV".

## Identidade visual

Extraida da logo: ciano `#22D3FF` no vertice, azul eletrico `#1E5CF5` na base,
fundo azul-preto `#070A12`. O gradiente da logo aparece nos botoes, no destaque
do titulo e nos detalhes. O triangulo ascendente vira o marcador da lista de
servicos e o brilho no topo dos cards.

Tipografia: Archivo (titulos), Manrope (texto), IBM Plex Mono (etiquetas).
