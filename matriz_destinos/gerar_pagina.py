"""Gera a página interativa (saida/matriz_destinos.html) a partir dos mesmos CSVs da planilha."""
import csv
import json
from collections import OrderedDict
from pathlib import Path

from gerar_planilha import DESTINOS, FAMILIAS

AQUI = Path(__file__).parent
SAIDA = AQUI.parent / "saida" / "matriz_destinos.html"
MODELO = AQUI / "modelo_pagina.html"


def ler(nome):
    with open(AQUI / "dados" / nome, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def main():
    precos = {p["roteiro"]: p for p in ler("roteiros_precos.csv")}
    rot = OrderedDict()
    for l in ler("roteiros_destinos.csv"):
        r = rot.setdefault(l["roteiro"], {
            "n": l["roteiro"], "f": l["familia"], "d": int(l["dias"]), "nt": int(l["noites"]), "t": []})
        r["t"].append([l["destino"], int(l["noites_destino"]), l["obs"]])
    for nome, r in rot.items():
        p = precos[nome]
        r["p"] = int(p["preco_vista_baixa"]) if p["preco_vista_baixa"] else None
        r["px"] = p["obs"] if not p["preco_vista_baixa"] else ""
        r["cat"] = p["categoria"].title()
        r["pdf"] = p["arquivo_id"]
    dados = {
        "regioes": [{"nome": k, "destinos": v} for k, v in DESTINOS.items()],
        "familias": FAMILIAS,
        "roteiros": list(rot.values()),
    }
    html = MODELO.read_text(encoding="utf-8").replace(
        "/*__DADOS__*/null", json.dumps(dados, ensure_ascii=False, separators=(",", ":")))
    SAIDA.write_text(html, encoding="utf-8")
    print(f"OK: {SAIDA} ({len(rot)} roteiros)")


if __name__ == "__main__":
    main()
