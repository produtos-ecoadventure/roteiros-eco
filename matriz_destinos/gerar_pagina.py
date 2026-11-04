"""Gera a página do guia (saida/matriz_destinos.html) a partir da fonte única em dados/."""
import json
from pathlib import Path

import base

AQUI = Path(__file__).parent
SAIDA = AQUI.parent / "saida" / "matriz_destinos.html"
SITE = AQUI.parent / "saida" / "site" / "index.html"   # versão completa para o GitHub Pages

CABECALHO_SITE = """<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="robots" content="noindex, nofollow">
<meta name="description" content="Guia interno dos roteiros 2026 da Eco Adventure Tour para consultores.">
<style>html,body{margin:0}</style>
"""
MODELO = AQUI / "modelo_pagina.html"


def main():
    b = base.carregar()
    roteiros = []
    for nome, r in b["roteiros"].items():
        roteiros.append({
            "n": nome, "f": r["familia"], "d": r["dias"], "nt": r["noites"],
            "t": [[p["destino"], p["noites"], p["obs"]] for p in r["trajeto"]],
            "cat": r["categoria"].title(), "pdf": r["pdf"],
        })
    dados = {
        "regioes": [{"nome": k, "destinos": v} for k, v in b["regioes"].items()],
        "familias": b["ordem_familias"],
        "sobre": b["descricao"],
        "geo": {k: list(v) for k, v in b["geo"].items()},
        "mapa": {k: v for k, v in b["mapa"].items() if not k.startswith("_")},
        "roteiros": roteiros,
    }
    html = MODELO.read_text(encoding="utf-8").replace(
        "/*__DADOS__*/null", json.dumps(dados, ensure_ascii=False, separators=(",", ":")))
    SAIDA.write_text(html, encoding="utf-8")
    SITE.parent.mkdir(parents=True, exist_ok=True)
    corpo = html.index('<header class="hero')          # tudo antes disso (título, fontes, estilos) vai no <head>
    SITE.write_text(CABECALHO_SITE + html[:corpo].replace('<meta name="claude:viewport-fit-sides" content="cover">\n', "")
                    + "</head>\n<body>\n" + html[corpo:] + "\n</body>\n</html>\n", encoding="utf-8")
    print(f"OK: {SAIDA} e {SITE.relative_to(AQUI.parent)} ({len(roteiros)} roteiros)")


if __name__ == "__main__":
    main()
