"""Gera a página do guia (saida/matriz_destinos.html) a partir da fonte única em dados/."""
import json
from pathlib import Path

import base

AQUI = Path(__file__).parent
SAIDA = AQUI.parent / "saida" / "matriz_destinos.html"
MODELO = AQUI / "modelo_pagina.html"


def main():
    b = base.carregar()
    roteiros = []
    for nome, r in b["roteiros"].items():
        x = b["extras"][nome]
        roteiros.append({
            "n": nome, "f": r["familia"], "d": r["dias"], "nt": r["noites"],
            "t": [[p["destino"], p["noites"], p["obs"]] for p in r["trajeto"]],
            "cat": x["categoria"].title(), "pdf": x["arquivo_id"],
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
    print(f"OK: {SAIDA} ({len(roteiros)} roteiros)")


if __name__ == "__main__":
    main()
