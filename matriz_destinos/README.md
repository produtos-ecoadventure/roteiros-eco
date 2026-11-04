# Matriz de destinos por roteiro (2026)

Versão otimizada da "Tabela de destinos por pacotes": em vez de ✅/❌ com os roteiros nas
colunas, cada **roteiro é uma linha** e cada **destino é uma coluna** (ordem geográfica), e a
célula mostra **quantas noites** o roteiro passa ali (● = visita sem pernoite).

## Arquivos

| Arquivo | O que é |
|---|---|
| `dados/roteiros_destinos.csv` | Base: uma linha por roteiro × destino, na ordem do trajeto, com noites e observações |
| `dados/roteiros_precos.csv` | Preço "a partir de" (2 pessoas, baixa temporada) e id do PDF no Drive |
| `gerar_planilha.py` | Gera `saida/MATRIZ_DESTINOS_POR_ROTEIRO_2026.xlsx` (Matriz, Busca, Base, Destinos, Como usar) |
| `gerar_pagina.py` + `modelo_pagina.html` | Geram `saida/matriz_destinos.html` (página interativa) |

```bash
python3 gerar_planilha.py && python3 gerar_pagina.py
```

## Fonte

46 roteiros da pasta `Roteiros` do Drive (inclusive as subpastas Econômicas, Eco Culturais,
Alhurez e Invertidas). De cada pasta foi lido um PDF (base 2 pessoas), porque o trajeto é o
mesmo para todas as bases. As noites foram contadas pelas linhas "Pernoite em …" e conferidas
com o total "X dias e Y noites" de cada roteiro (46/46 batem).

## Convenções

- Chegada ou saída sem pernoite (ex.: aeroporto de Fortaleza no último dia) = 0 noites (●).
- Bate-volta (Santo Amaro, Atins, Canoa Quebrada) = 0 noites (●), com a observação na Base.
- Travessia dos Lençóis = noites em redários do trekking (Baixa Grande, Queimada dos Britos, Betânia).
- Bate e volta / Mini pacotes têm versões de 1 a 3 dias; a Base registra a versão mais longa.
