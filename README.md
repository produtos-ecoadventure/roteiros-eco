# Tabela de Prioritários — Tarifário Receptivo 2026

Projeto para gerar, numa sessão em nuvem do Claude Code, uma planilha automatizada
no modelo da Tabela de Prioritários 2026, só com os serviços do Tarifário Receptivo.

As instruções completas para o Claude estão em `CLAUDE.md`.

## Como começar a sessão em nuvem

1. **Crie um repositório privado no GitHub** (ex.: `tabela-prioritarios-tarifario`).
   Ele precisa ser privado, porque contém valores de fornecedores.
2. **Envie esta pasta** para o repositório. Pelo site do GitHub: "Add file" → "Upload files",
   arraste o conteúdo da pasta (mantendo as subpastas) e faça o commit.
3. **Abra uma sessão em nuvem**: acesse claude.ai/code (ou a aba Code no app),
   conecte o GitHub se ainda não estiver conectado, escolha o repositório e inicie.
4. **Cole o pedido inicial**:

   > Leia o CLAUDE.md e execute o projeto: gere a planilha automatizada em `saida/`,
   > o relatório de casamento, valide as fórmulas e faça o commit numa branch.

5. Quando terminar, baixe `saida/TABELA_PRIORITARIOS_TARIFARIO_RECEPTIVO_2026.xlsx`
   pela branch no GitHub.

## Estrutura

```
CLAUDE.md                         instruções do projeto para o Claude
dados/
  originais/                      planilha-modelo e PDF (não editar)
  servicos_tarifario_2026.csv     71 serviços / 182 faixas extraídos do PDF
scripts/                          scripts que a sessão criar
saida/                            planilha final e relatório
```
