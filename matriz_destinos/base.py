"""Fonte única dos dados do guia de roteiros: leitura e validação.

Arquivos em dados/ (separador ;):
  familias.csv   ordem; familia; descricao
  destinos.csv   ordem; destino; regiao; lat; lon
  roteiros.csv   roteiro; familia; dias; noites; categoria; arquivo_pdf; preco_vista_baixa; obs_preco
                 (preços: base 2 pessoas, baixa temporada; usados só na planilha)
  paradas.csv    roteiro; ordem; destino; noites; obs   (uma linha por parada, na ordem do trajeto)
  mapa_base.json costa, divisas estaduais e siglas do mapa esquemático
"""
import csv
import json
from collections import OrderedDict
from pathlib import Path

DADOS = Path(__file__).parent / "dados"


def _csv(nome):
    with open(DADOS / nome, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def carregar():
    familias = sorted(_csv("familias.csv"), key=lambda x: int(x["ordem"]))
    destinos = sorted(_csv("destinos.csv"), key=lambda x: int(x["ordem"]))
    regioes = OrderedDict()
    for d in destinos:
        regioes.setdefault(d["regiao"], []).append(d["destino"])
    ordem_fam = [f["familia"] for f in familias]

    roteiros = OrderedDict()
    for l in _csv("roteiros.csv"):
        roteiros[l["roteiro"]] = {
            "roteiro": l["roteiro"], "familia": l["familia"], "dias": int(l["dias"]),
            "noites": int(l["noites"]), "categoria": l["categoria"].strip().upper(),
            "pdf": l["arquivo_pdf"].strip(), "preco": l["preco_vista_baixa"].strip(),
            "obs_preco": l["obs_preco"].strip(), "trajeto": []}
    orfas = []
    for l in _csv("paradas.csv"):
        parada = {"ordem": int(l["ordem"]), "destino": l["destino"], "noites": int(l["noites"]), "obs": l["obs"]}
        if l["roteiro"] in roteiros:
            roteiros[l["roteiro"]]["trajeto"].append(parada)
        else:
            orfas.append(l["roteiro"])
    for r in roteiros.values():
        r["trajeto"].sort(key=lambda x: x["ordem"])

    # Ordem de exibição: família (ordem de familias.csv), depois duração e nome
    pos = {f: i for i, f in enumerate(ordem_fam)}
    ordenados = OrderedDict(sorted(roteiros.items(),
                                   key=lambda kv: (pos.get(kv[1]["familia"], 99), kv[1]["dias"], kv[0])))
    return {
        "familias": familias,
        "ordem_familias": ordem_fam,
        "descricao": {f["familia"]: f["descricao"] for f in familias},
        "destinos": destinos,
        "regioes": regioes,
        "geo": {d["destino"]: (float(d["lat"]), float(d["lon"])) for d in destinos},
        "roteiros": ordenados,
        "paradas_orfas": orfas,
        "mapa": json.loads((DADOS / "mapa_base.json").read_text(encoding="utf-8")),
    }


def validar(b):
    """Devolve a lista de problemas encontrados (vazia = tudo certo)."""
    erros = []
    fams, dests = set(b["ordem_familias"]), set(b["geo"])
    if len(fams) != len(b["familias"]):
        erros.append("familias.csv: nome de família repetido")
    if len(dests) != len(b["destinos"]):
        erros.append("destinos.csv: destino repetido")
    for nome in sorted(set(b["paradas_orfas"])):
        erros.append(f"paradas.csv: roteiro '{nome}' não existe em roteiros.csv")
    for nome, (lat, lon) in b["geo"].items():
        if not (-12 < lat < 0 and -48 < lon < -33):
            erros.append(f"destinos.csv: coordenada fora da região para {nome} ({lat}, {lon})")
    for nome, r in b["roteiros"].items():
        if r["familia"] not in fams:
            erros.append(f"{nome}: família '{r['familia']}' não existe em familias.csv")
        if r["categoria"] not in {"LIGHT", "COMFORT", "STARS"}:
            erros.append(f"{nome}: categoria '{r['categoria']}' (use Light, Comfort ou Stars)")
        if not r["pdf"]:
            erros.append(f"{nome}: sem id do PDF no Drive")
        if not r["trajeto"]:
            erros.append(f"{nome}: nenhuma parada em paradas.csv")
            continue
        soma = sum(p["noites"] for p in r["trajeto"])
        if soma != r["noites"]:
            erros.append(f"{nome}: soma das noites no trajeto = {soma}, mas o roteiro diz {r['noites']} noites")
        if r["dias"] != r["noites"] + 1:
            erros.append(f"{nome}: {r['dias']} dias e {r['noites']} noites (esperado dias = noites + 1)")
        ordens = [p["ordem"] for p in r["trajeto"]]
        if ordens != list(range(1, len(ordens) + 1)):
            erros.append(f"{nome}: ordem do trajeto não é 1, 2, 3… ({ordens})")
        for p in r["trajeto"]:
            if p["destino"] not in dests:
                erros.append(f"{nome}: destino '{p['destino']}' não existe em destinos.csv")
            if p["noites"] < 0:
                erros.append(f"{nome}: noites negativas em {p['destino']}")
    usados = {p["destino"] for r in b["roteiros"].values() for p in r["trajeto"]}
    for d in sorted(dests - usados):
        erros.append(f"destinos.csv: '{d}' não aparece em nenhum roteiro")
    for f in sorted(fams - {r["familia"] for r in b["roteiros"].values()}):
        erros.append(f"familias.csv: '{f}' não tem nenhum roteiro")
    return erros
