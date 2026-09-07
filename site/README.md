# Site da ELEV

Página única, sem dependência de build: e um arquivo `index.html` com CSS e JS
dentro. Da para publicar em qualquer lugar (Vercel, Netlify, GitHub Pages,
hospedagem comum) arrastando a pasta `site/`.

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
  instagram: "",   // so o usuario, sem @. Ex.: "elev.digital"
  email:     ""    // Ex.: "contato@elev.com.br"
};
```

Enquanto estiverem vazios, os tres botoes aparecem marcados como "a configurar"
com borda tracejada - de proposito, para nao virar link morto. Preencheu, eles
viram link de verdade na hora.

### 3. Dados institucionais do rodape

Procure `data-rodape-pendente` no `index.html` e troque o texto por cidade,
CNPJ e o que mais for oficial.

## O que NAO tem no site (de proposito)

Nao ha cliente, depoimento, numero de resultado, preco nem prazo. Nada disso
existe ainda de forma verificada, e inventar seria o pior erro possivel numa
vitrine comercial. Os quatro projetos da secao "Projetos demonstrativos" estao
marcados como demonstracao no proprio card e no aviso acima deles.

Quando houver cliente real com autorizacao, o lugar de entrar e a mesma secao -
trocando o aviso e o selo "Demonstracao" pelo nome do cliente.

## Identidade visual

Extraida da logo: ciano `#22D3FF` no vertice, azul eletrico `#1E5CF5` na base,
fundo azul-preto `#070A12`. O gradiente da logo aparece nos botoes, no destaque
do titulo e nos detalhes. O triangulo ascendente vira o marcador da lista de
servicos e o brilho no topo dos cards.

Tipografia: Archivo (titulos), Manrope (texto), IBM Plex Mono (etiquetas).
