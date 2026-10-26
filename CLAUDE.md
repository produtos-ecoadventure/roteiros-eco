# Projeto: Tabela de Prioritários — Tarifário Receptivo 2026

Eco Adventure Tour. Responda sempre em português do Brasil.

## Objetivo

Gerar **uma nova planilha .xlsx automatizada**, no mesmo modelo da
`TABELA DE PRIORITÁRIOS 2026`, contendo **apenas os serviços do Tarifário
Receptivo – Mais Vendidos 2026** (71 serviços / 182 linhas de capacidade).

Saída esperada: `saida/TABELA_PRIORITARIOS_TARIFARIO_RECEPTIVO_2026.xlsx`

## Arquivos de entrada

| Arquivo | O que é |
|---|---|
| `dados/originais/TABELA_DE_PRIORITARIOS_2026.xlsx` | Planilha-modelo (5 abas). **Somente leitura.** |
| `dados/originais/TARIFARIO_RECEPTIVO_2026.pdf` | Tarifário de 30 páginas (fonte da lista de serviços) |
| `dados/servicos_tarifario_2026.csv` | Serviços do PDF já extraídos (separador `;`), conferidos: todas as parcelas batem com a fórmula |

Colunas do CSV: `id; tipo (TRANS/PASSE); carater (COMP/PVT); servico; horarios; duracao; operacao; valor_vista; parcela_6x; pagina_pdf`.
Linhas com o mesmo `id` são faixas de capacidade do mesmo serviço.

## Estrutura da planilha-modelo (aba "Fornecedores com NF" é a versão completa)

- Linhas 1–7: legenda de cores (A1 "Legenda", F1 título, AA1 "LEGENDA CORES").
- Linha 8: cabeçalho. Repetido antes de cada seção (TRANSFERS na linha 8, PASSEIOS na 94).
- Colunas:
  - A nº · B TIPO · C CARÁTER · D SERVIÇO · E ORIENTAÇÃO · F QUANT.
  - G–R FORNE. 1 a 12 (texto livre: "FORNECEDOR R$ valor (ano) : ±x% do budget")
  - S PROJETADO (15%) "SIM/NÃO" · T BUDGET 2025 COM DETALHES · U QUANT.
  - **V BUDGET 2026** (valor de entrada, R$)
  - **W VALOR CLIENTE 2026** `=ROUNDUP(V/0.7,0)`
  - **X PARCELA 6X** `=ROUNDUP(W*0.1912,0)`
  - **Y VALOR OPERADORA** `=ROUNDUP(V/0.8,0)`
  - Z VALOR CLIENTE ANTIGO (2025) · **AA AUMENTO %** `=(W-Z)/Z` (formato 0%)
  - **AB status do bloco**: `=IF(COUNTIF(S9:S12,"não")=COUNTA(S9:S12),"Budget fechado",IF(COUNTIF(S9:S12,"sim")=COUNTA(S9:S12),"Budget aberto","Budget parcialmente fechado"))` na 1ª linha de cada serviço, cobrindo todas as linhas do bloco.
- Cada serviço ocupa um bloco de linhas (uma por capacidade), com A–E mesclados verticalmente.
- Estilos: cabeçalho fundo preto/fonte branca negrito (D e V em verde `38761D`); linhas de serviço alternando azul claro `CFE2F3` e branco; V com fundo `D9EAD3`; S com fundo `B7B7B7`; moeda `[$R$ -416]#,##0.00`.
- Abas auxiliares (fórmulas dinâmicas, HSTACK):
  - "Budgets 2026": `=HSTACK('Fornecedores 2026'!A8:E8,'Fornecedores 2026'!S8:Y8)` linha a linha.
  - "Parcial de Budgets": coluna A serviço (D), B status (AB) e um resumo com COUNTIF de "Budget fechado / parcialmente fechado / aberto", total e %.
  - "Emite NF": mesma grade, com legenda "Quem emite / Quem emite com acréscimo / Quem não emite".

## Regra-chave descoberta

O preço do tarifário **é o VALOR CLIENTE (coluna W)** da planilha. Portanto:
- Budget implícito = valor_vista × 0,7 (validar: `ROUNDUP(V/0.7)` deve reproduzir o valor do PDF).
- Para cada serviço, **buscar a linha correspondente na planilha-modelo** e trazer
  fornecedores (G–R), S, T, V, Z. Se o V do modelo não reproduzir o preço do PDF,
  manter o V do modelo e **sinalizar a divergência** numa coluna "CONFERÊNCIA TARIFÁRIO"
  (ex.: `=IF(W9=<valor PDF>,"OK","Diverge do tarifário")`).
- Serviço do PDF sem correspondente no modelo: criar o bloco com V = valor_vista×0,7
  (arredondado), fornecedores vazios, e destacar em amarelo para revisão.
- Os nomes dos serviços diferem entre PDF e planilha (maiúsculas, "VICE-VERSA",
  "Via Estrada" etc.). Fazer o casamento por rota + caráter + capacidade e
  **gerar um relatório de casamento** (`saida/relatorio_casamento.md`) listando cada
  serviço do PDF, a linha do modelo usada e as divergências.

## Requisitos da planilha nova

1. Abas: "Prioritários Tarifário" (principal), "Budgets", "Parcial de Budgets",
   "Conferência" (PDF × planilha) e, se fizer sentido, "Emite NF".
2. Tudo calculado por **fórmula** (W, X, Y, AA, AB, resumos). Alterar V deve
   atualizar o resto. Não colar valores calculados.
3. Preferir fórmulas compatíveis com Excel e Google Sheets; evitar HSTACK nas abas
   auxiliares (usar referências diretas `='Prioritários Tarifário'!D9`).
4. Manter a ordem do tarifário: Transfers (ids 1–31) e Passeios (ids 32–71).
5. Congelar painéis no cabeçalho, filtros, larguras de coluna legíveis.
6. Recalcular com LibreOffice (`soffice --headless`) e verificar que não há
   erros (`#REF!`, `#VALUE!`, `#DIV/0!`); AA deve tratar Z vazio com IFERROR.

## Ao terminar

- Commit em uma branch, com a planilha em `saida/` e o relatório de casamento.
- Resumo curto: quantos serviços casaram, quantos divergem do PDF, quantos novos.

## Cuidados

- Os dados de fornecedores e budgets são internos/confidenciais. O repositório deve ser **privado**.
- Não alterar os arquivos em `dados/originais/`.
