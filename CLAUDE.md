# Projeto: Guia de Roteiros Eco Adventure Tour 2026

Eco Adventure Tour. Responda sempre em português do Brasil.

## Objetivo

Manter um **guia de roteiros para consultores novos**: por onde cada roteiro passa,
quantas noites fica em cada destino e o que diferencia uma família de outra.
O projeto **não** trata de tarifários nem de preços de fornecedores.

## Fonte dos dados

Os roteiros vêm do Google Drive, pasta `Roteiros` (id `1ny4Q1bqaReKJG2nBRmYq6XseLSU3VgXt`),
uma subpasta por roteiro (as pastas `1 - Econômicas`, `2 - Eco Culturais`, `3 - Alhurez`
e `4 - Invertidas` têm subpastas). Em cada pasta basta ler **um** PDF (de preferência
`2 PESSOAS`): o trajeto é igual para todas as bases de pessoas e categorias de hotel.
As noites saem das linhas "Pernoite em …" e devem bater com o "X dias e Y noites" do PDF.

## Estrutura

```
matriz_destinos/
  dados/                  FONTE ÚNICA — edite só aqui
    familias.csv          ordem; familia; descricao (texto que o consultor lê)
    destinos.csv          ordem; destino; regiao; lat; lon
    roteiros.csv          uma linha por roteiro: família, dias, noites, categoria, id do PDF (e preço, só p/ planilha)
    paradas.csv           uma linha por parada: roteiro; ordem; destino; noites; obs
    mapa_base.json        costa, divisas estaduais e siglas do mapa esquemático
  base.py                 leitura + regras de validação
  validar.py              confere os dados (sai com erro se algo não bate)
  test_dados.py           testes (python3 -m unittest discover -s matriz_destinos -t matriz_destinos)
  gerar.py                valida e gera tudo
  gerar_planilha.py       saida/MATRIZ_DESTINOS_POR_ROTEIRO_2026.xlsx
  gerar_pagina.py         saida/matriz_destinos.html (a partir de modelo_pagina.html)
saida/                    arquivos gerados (não editar à mão)
```

## Regras

1. Toda mudança de conteúdo é feita nos arquivos de `matriz_destinos/dados/`, nunca no HTML ou na planilha.
2. Depois de editar: `python3 matriz_destinos/gerar.py` e confira que a validação passou.
3. Convenções da base: chegada/saída sem pernoite e bate-volta = 0 noites, com o motivo em `obs`
   (o texto "bate-volta" faz a página mostrar o destino entre parênteses).
   Destino novo precisa de linha em `destinos.csv` com coordenadas.
4. A página publicada é o artifact "Guia de Roteiros Eco 2026"; republique o mesmo arquivo
   (`saida/matriz_destinos.html`) para manter o link.
5. Identidade visual: verde `#53AF02` e azul `#2A3767` (manual da marca); fundo branco,
   modo escuro opcional. Visual limpo: uma coisa por tela (famílias → roteiros → detalhe).
6. As lâminas (deck "Lâminas de Destinos 2026") são editadas à parte; ao mudar roteiros, atualize-as também.

## Arquivos legados

`dados/originais/` e `dados/servicos_tarifario_2026.csv` são do projeto de tarifários,
que foi descontinuado. Não são usados pelo guia.
