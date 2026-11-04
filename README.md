# Guia de Roteiros — Eco Adventure Tour 2026

Guia para consultores novos conhecerem os 46 roteiros da Eco: famílias, trajeto de cada
roteiro no mapa e quantas noites ele passa em cada destino.

## O que é gerado

| Arquivo | Para quê |
|---|---|
| `saida/matriz_destinos.html` | O guia (página publicada como artifact "Guia de Roteiros Eco 2026") |
| `saida/MATRIZ_DESTINOS_POR_ROTEIRO_2026.xlsx` | Planilha de apoio: matriz roteiros × destinos, busca por destinos e base editável |

## Como atualizar

1. Edite os arquivos em `matriz_destinos/dados/` (detalhes em `matriz_destinos/README.md`).
2. Rode:

   ```bash
   pip install -r requirements.txt
   python3 matriz_destinos/gerar.py
   ```

   O comando valida os dados primeiro (soma de noites, destinos com coordenadas, família
   existente, PDF informado) e só gera se estiver tudo certo.
3. Faça o commit. No GitHub, a ação **Guia de roteiros** repete a validação e avisa se a
   página ficou desatualizada em relação aos dados.

Instruções para o Claude: `CLAUDE.md`.
