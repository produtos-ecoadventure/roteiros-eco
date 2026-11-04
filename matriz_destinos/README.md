# Guia de roteiros: dados e geradores

Tudo sai da pasta `dados/`. Para mudar um roteiro, um texto ou um destino, edite só ali e rode
`python3 gerar.py` (valida e gera a página e a planilha).

## Arquivos de dados (separador `;`)

| Arquivo | Colunas | Observações |
|---|---|---|
| `familias.csv` | ordem; familia; descricao | A descrição é o texto que o consultor lê. A ordem define a ordem na página. |
| `destinos.csv` | ordem; destino; regiao; lat; lon | Nome no formato `Cidade/UF`. Coordenadas aproximadas para o mapa. |
| `roteiros_destinos.csv` | roteiro; familia; dias; noites; ordem; destino; noites_destino; obs | Uma linha por parada, na ordem do trajeto. |
| `roteiros_precos.csv` | roteiro; categoria; base; preco_vista_baixa; arquivo_id; obs | Usado para a categoria (Light/Stars) e o link do PDF. Os preços só aparecem na planilha. |
| `mapa_base.json` | costa, divisas, siglas | Contorno simplificado do mapa esquemático. |

## Convenções

- **Chegada, saída ou passagem sem pernoite** = 0 noites, com o motivo em `obs` (`saída`, `chegada`, `visita no trajeto`).
- **Bate-volta** = 0 noites e `obs` com a palavra `bate-volta`. A página mostra esses destinos entre parênteses.
- **Travessia dos Lençóis** = noites em redários do trekking (Baixa Grande, Queimada dos Britos, Betânia).
- **Bate e volta e Mini pacotes** têm versões de 1 a 3 dias; a base registra a mais longa.

## Validação (`validar.py`)

Para o processo e mostra o problema quando:

- a soma das noites do trajeto difere do total do roteiro, ou dias ≠ noites + 1;
- a ordem das paradas não é 1, 2, 3…;
- um destino não existe em `destinos.csv` (ou está sem coordenada válida);
- uma família não existe em `familias.csv`, ou uma família/destino ficou sem uso;
- um roteiro está sem categoria ou sem id do PDF.

## Fonte

PDFs 2026 da pasta `Roteiros` do Drive, um por roteiro (base 2 pessoas), lidos em 04/11/2026.
