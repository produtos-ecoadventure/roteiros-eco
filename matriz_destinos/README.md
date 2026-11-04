# Guia de roteiros: dados e geradores

Tudo sai da pasta `dados/`. Para mudar um roteiro, um texto ou um destino, edite só ali e rode
`python3 gerar.py` (valida e gera a página e a planilha).

## Arquivos de dados (separador `;`)

| Arquivo | Colunas | Observações |
|---|---|---|
| `familias.csv` | ordem; familia; descricao | A descrição é o texto que o consultor lê. A ordem define a ordem na página. |
| `destinos.csv` | ordem; destino; regiao; lat; lon | Nome no formato `Cidade/UF`. Coordenadas aproximadas para o mapa. |
| `roteiros.csv` | roteiro; familia; dias; noites; categoria; pasta_drive; arquivo_pdf; preco_vista_baixa; obs_preco | Uma linha por roteiro. `pasta_drive` é o id da pasta do roteiro no Drive (o botão do guia abre essa pasta); `arquivo_pdf` é o PDF de 2 pessoas usado na extração. Preço (base 2 pessoas, baixa temporada) só aparece na planilha. |
| `paradas.csv` | roteiro; ordem; destino; noites; obs | Uma linha por parada, na ordem do trajeto. |
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
- um roteiro está sem categoria válida (Light, Comfort, Stars) ou sem pasta do Drive, ou duas linhas apontam para a mesma pasta;
- há parada de um roteiro que não existe em `roteiros.csv`.

Os testes (`test_dados.py`) garantem que essas regras continuam funcionando:
`python3 -m unittest discover -s matriz_destinos -t matriz_destinos`.

## Como incluir um roteiro novo

1. Uma linha em `roteiros.csv` (família, dias, noites, categoria, id da pasta no Drive — o trecho final do link da pasta, depois de `/folders/`).
2. Uma linha por parada em `paradas.csv`, na ordem do trajeto.
3. Destino novo? Uma linha em `destinos.csv` com região e coordenadas.
4. `python3 gerar.py` e, se a validação passar, commit.

## Fonte

PDFs 2026 da pasta `Roteiros` do Drive, um por roteiro (base 2 pessoas), lidos em 04/11/2026.
