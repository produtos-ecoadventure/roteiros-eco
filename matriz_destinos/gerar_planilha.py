"""Gera a Matriz de Destinos por Roteiro (2026) em .xlsx.

Entrada: a fonte única em dados/ (ver base.py).

Saída:
  ../saida/MATRIZ_DESTINOS_POR_ROTEIRO_2026.xlsx

A matriz é calculada por fórmula (SUMIFS/COUNTIFS sobre a aba "Base"), então
incluir ou corrigir linhas na Base atualiza a matriz e a aba de Busca.
Fórmulas compatíveis com Excel e Google Sheets (sem FILTER/HSTACK).
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import CellIsRule, FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.worksheet.datavalidation import DataValidation

AQUI = Path(__file__).parent
SAIDA = AQUI.parent / "saida" / "MATRIZ_DESTINOS_POR_ROTEIRO_2026.xlsx"

import base

COR_REGIAO = ["F4CCCC", "FCE5CD", "FFF2CC", "D9EAD3", "CFE2F3", "EAD1DC", "D0E0E3"]

PRETO, BRANCO = "000000", "FFFFFF"
VERDE_ECO = "38761D"
AZUL_CLARO = "EEF4FB"
fino = Side(style="thin", color="BFBFBF")
BORDA = Border(left=fino, right=fino, top=fino, bottom=fino)
L = get_column_letter
COL_DEST0 = 6  # coluna F: primeiro destino na Matriz
PRIM = 7       # primeira linha de roteiro na Matriz


def nome_curto(destino):
    return destino.rsplit("/", 1)[0]


def main():
    b = base.carregar()
    DESTINOS, FAMILIAS = b["regioes"], b["ordem_familias"]
    roteiros = b["roteiros"]          # já em ordem de exibição
    ordem = list(roteiros)
    todos_dest = [d for ds in DESTINOS.values() for d in ds]
    n_paradas = sum(len(r["trajeto"]) for r in roteiros.values())
    ULT = PRIM + len(ordem) - 1
    col_traj = COL_DEST0 + len(todos_dest)
    faixa_dest = f"Matriz!${L(COL_DEST0)}${PRIM}:${L(col_traj - 1)}${ULT}"
    cab_dest = f"Matriz!${L(COL_DEST0)}$6:${L(col_traj - 1)}$6"

    wb = Workbook()

    # ------------------------------------------------------------------ Base
    wsb = wb.active
    wsb.title = "Base"
    cab_base = ["ROTEIRO", "FAMÍLIA", "DIAS", "NOITES", "ORDEM", "DESTINO", "NOITES NO DESTINO", "OBS"]
    wsb.append(cab_base)
    for nome, r in roteiros.items():
        for p in r["trajeto"]:
            wsb.append([nome, r["familia"], r["dias"], r["noites"],
                        p["ordem"], p["destino"], p["noites"], p["obs"] or None])
    for c in wsb[1]:
        c.font = Font(bold=True, color=BRANCO)
        c.fill = PatternFill("solid", fgColor=PRETO)
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for col, w in zip("ABCDEFGH", [32, 18, 7, 8, 7, 34, 10, 44]):
        wsb.column_dimensions[col].width = w
    wsb.freeze_panes = "A2"
    wsb.auto_filter.ref = f"A1:H{wsb.max_row}"
    dv_dest = DataValidation(type="list", formula1="=Destinos!$A$2:$A$%d" % (len(todos_dest) + 1),
                             allow_blank=False)
    wsb.add_data_validation(dv_dest)
    dv_dest.add(f"F2:F{wsb.max_row + 300}")
    n_base = wsb.max_row + 300  # folga para novos roteiros
    rngA = f"Base!$A$2:$A${n_base}"
    rngF = f"Base!$F$2:$F${n_base}"
    rngG = f"Base!$G$2:$G${n_base}"

    # -------------------------------------------------------------- Destinos
    wsd = wb.create_sheet("Destinos")
    wsd.append(["DESTINO", "REGIÃO", "Nº DE ROTEIROS", "SOMA DE NOITES NOS ROTEIROS"])
    for reg, ds in DESTINOS.items():
        for d in ds:
            i = wsd.max_row + 1
            wsd.append([d, reg, None, None])
            col_m = f'INDEX({faixa_dest},0,MATCH(A{i},{cab_dest},0))'
            wsd[f"C{i}"] = f'=COUNT({col_m})+COUNTIF({col_m},"●")'
            wsd[f"D{i}"] = f"=SUMIFS({rngG},{rngF},A{i})"
    for c in wsd[1]:
        c.font = Font(bold=True, color=BRANCO)
        c.fill = PatternFill("solid", fgColor=PRETO)
        c.alignment = Alignment(horizontal="center", wrap_text=True)
    for col, w in zip("ABCD", [36, 24, 14, 22]):
        wsd.column_dimensions[col].width = w
    wsd.freeze_panes = "A2"

    # ---------------------------------------------------------------- Matriz
    ws = wb.create_sheet("Matriz", 0)
    col_dest0 = COL_DEST0
    col_pdf = col_traj + 1
    col_aux = col_pdf + 1
    ws["A1"] = "MATRIZ DE DESTINOS POR ROTEIRO – 2026"
    ws["A1"].font = Font(bold=True, size=16, color=VERDE_ECO)
    ws["A2"] = ("Número = noites no destino   •   ● = visita sem pernoite (bate-volta, passagem, "
                "chegada ou saída)   •   célula vazia = não passa")
    ws["A2"].font = Font(italic=True, color="595959")
    ws["A3"] = ("Preço: a partir de, por pessoa, base 2 pessoas, baixa temporada, Jeri-For pela estrada "
                "(categoria Light, salvo indicação). Use os filtros da linha 6 e a aba Busca.")
    ws["A3"].font = Font(italic=True, color="595959", size=9)

    cab = ["FAMÍLIA", "ROTEIRO", "DIAS", "NOITES", "A PARTIR DE"]
    for i, t in enumerate(cab, start=1):
        ws.cell(row=6, column=i, value=t)
    ws.merge_cells(start_row=5, start_column=1, end_row=5, end_column=5)
    ws.cell(row=5, column=1, value="ROTEIRO")
    c = col_dest0
    for k, (reg, ds) in enumerate(DESTINOS.items()):
        ws.merge_cells(start_row=5, start_column=c, end_row=5, end_column=c + len(ds) - 1)
        cel = ws.cell(row=5, column=c, value=reg.upper())
        for j in range(c, c + len(ds)):
            ws.cell(row=5, column=j).fill = PatternFill("solid", fgColor=COR_REGIAO[k % len(COR_REGIAO)])
            ws.cell(row=5, column=j).border = BORDA
        cel.font = Font(bold=True, size=9)
        cel.alignment = Alignment(horizontal="center", vertical="center")
        for d in ds:
            ws.cell(row=6, column=c, value=d)
            c += 1
    ws.cell(row=6, column=col_traj, value="TRAJETO (noites)")
    ws.cell(row=6, column=col_pdf, value="PDF")
    ws.cell(row=6, column=col_aux, value="AUX BUSCA")
    ws.merge_cells(start_row=5, start_column=col_traj, end_row=5, end_column=col_pdf)
    ws.cell(row=5, column=col_traj, value="DETALHES")

    for j in range(1, col_aux + 1):
        cel = ws.cell(row=6, column=j)
        cel.font = Font(bold=True, color=BRANCO, size=9)
        cel.fill = PatternFill("solid", fgColor=VERDE_ECO if j == 2 else PRETO)
        cel.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True,
                                  text_rotation=90 if col_dest0 <= j < col_traj else 0)
        cel.border = BORDA
    ws.row_dimensions[6].height = 150
    for j in (1, col_traj):
        ws.cell(row=5, column=j).font = Font(bold=True, size=9)
        ws.cell(row=5, column=j).alignment = Alignment(horizontal="center")

    familia_ant = None
    faixa = False
    for i, nome in enumerate(ordem):
        r = PRIM + i
        info = roteiros[nome]
        if info["familia"] != familia_ant:
            faixa = not faixa
            familia_ant = info["familia"]
        fundo = PatternFill("solid", fgColor=AZUL_CLARO if faixa else BRANCO)
        ws.cell(row=r, column=1, value=info["familia"])
        ws.cell(row=r, column=2, value=nome)
        ws.cell(row=r, column=3, value=f"=INDEX(Base!$C$2:$C${n_base},MATCH($B{r},{rngA},0))")
        ws.cell(row=r, column=4, value=f"=SUMIFS({rngG},{rngA},$B{r})")
        if info["preco"]:
            cel = ws.cell(row=r, column=5, value=float(info["preco"]))
            cel.number_format = '"R$" #,##0'
        else:
            ws.cell(row=r, column=5, value=info["obs_preco"] or None)
        cat = info["categoria"]
        if cat != "LIGHT":
            ws.cell(row=r, column=5).number_format = f'"R$" #,##0" ({cat.title()})"'
        for j, d in enumerate(todos_dest):
            col = col_dest0 + j
            ref = f"{L(col)}$6"
            ws.cell(row=r, column=col,
                    value=(f'=IF(COUNTIFS({rngA},$B{r},{rngF},{ref})=0,"",'
                           f'IF(SUMIFS({rngG},{rngA},$B{r},{rngF},{ref})=0,"●",'
                           f'SUMIFS({rngG},{rngA},$B{r},{rngF},{ref})))'))
        traj = " → ".join(
            f"{nome_curto(p['destino'])} ({p['noites']})" if p["noites"]
            else f"{nome_curto(p['destino'])} (●)"
            for p in info["trajeto"])
        ws.cell(row=r, column=col_traj, value=traj)
        ws.cell(row=r, column=col_pdf,
                value=f'=HYPERLINK("https://drive.google.com/file/d/{info["pdf"]}/view","abrir")')
        cond = []
        for k in (3, 4, 5):
            cond.append(f'OR(Busca!$C${k}="",COUNTIFS({rngA},$B{r},{rngF},Busca!$C${k})>0)')
        cond.append(f'OR(Busca!$C$6="",$C{r}<=Busca!$C$6)')
        cond.append(f'OR(Busca!$C$7="",$A{r}=Busca!$C$7)')
        ws.cell(row=r, column=col_aux, value=f'=IF(AND({",".join(cond)}),ROW(),"")')
        for j in range(1, col_aux + 1):
            cel = ws.cell(row=r, column=j)
            cel.fill = fundo
            cel.border = BORDA
            cel.font = Font(size=10, bold=(j == 2), color="7F7F7F" if j == col_aux else "000000")
            if col_dest0 <= j < col_traj or j in (3, 4):
                cel.alignment = Alignment(horizontal="center", vertical="center")
            else:
                cel.alignment = Alignment(vertical="center", wrap_text=(j == col_traj))
        ws.cell(row=r, column=col_pdf).font = Font(size=10, color="1155CC", underline="single")

    # Totais por destino
    rt = ULT + 2
    ws.cell(row=rt, column=2, value="Nº de roteiros que passam").font = Font(bold=True)
    for j in range(len(todos_dest)):
        col = col_dest0 + j
        cel = ws.cell(row=rt, column=col,
                      value=f'=COUNT({L(col)}{PRIM}:{L(col)}{ULT})+COUNTIF({L(col)}{PRIM}:{L(col)}{ULT},"●")')
        cel.font = Font(bold=True)
        cel.alignment = Alignment(horizontal="center")
        cel.border = BORDA

    # Formatação condicional: intensidade por nº de noites
    area = f"{L(col_dest0)}{PRIM}:{L(col_traj - 1)}{ULT}"
    ini = f"{L(col_dest0)}{PRIM}"
    escala = [(1, "D9EAD3", "000000"), (2, "B6D7A8", "000000"), (3, "93C47D", "000000"),
              (4, "6AA84F", BRANCO), (5, "38761D", BRANCO)]
    for n, cor, fonte in escala:
        op = "greaterThanOrEqual" if n == 5 else "equal"
        ws.conditional_formatting.add(area, CellIsRule(operator=op, formula=[str(n)],
                                                       fill=PatternFill("solid", fgColor=cor),
                                                       font=Font(bold=True, color=fonte)))
    ws.conditional_formatting.add(area, FormulaRule(formula=[f'{ini}="●"'],
                                                    font=Font(color="999999")))
    # Destaque da linha que atende a busca
    ws.conditional_formatting.add(f"B{PRIM}:B{ULT}", FormulaRule(
        formula=[f'AND(OR(Busca!$C$3<>"",Busca!$C$4<>"",Busca!$C$5<>"",Busca!$C$6<>"",Busca!$C$7<>""),${L(col_aux)}{PRIM}<>"")'],
        fill=PatternFill("solid", fgColor="FFE599")))

    ws.column_dimensions["A"].width = 15
    ws.column_dimensions["B"].width = 30
    ws.column_dimensions["C"].width = 6
    ws.column_dimensions["D"].width = 7
    ws.column_dimensions["E"].width = 16
    for j in range(col_dest0, col_traj):
        ws.column_dimensions[L(j)].width = 4.6
    ws.column_dimensions[L(col_traj)].width = 70
    ws.column_dimensions[L(col_pdf)].width = 7
    ws.column_dimensions[L(col_aux)].width = 6
    ws.column_dimensions[L(col_aux)].hidden = True
    ws.freeze_panes = f"{L(col_dest0)}{PRIM}"
    ws.auto_filter.ref = f"A6:{L(col_pdf)}{ULT}"
    ws.sheet_view.zoomScale = 90

    # ----------------------------------------------------------------- Busca
    wq = wb.create_sheet("Busca", 1)
    wq["B1"] = "BUSCA DE ROTEIROS"
    wq["B1"].font = Font(bold=True, size=14, color=VERDE_ECO)
    labels = ["Passa por (destino 1)", "E também por (destino 2)", "E também por (destino 3)",
              "Duração máxima (dias)", "Família"]
    for k, t in enumerate(labels, start=3):
        wq[f"B{k}"] = t
        wq[f"B{k}"].font = Font(bold=True)
        wq[f"C{k}"].fill = PatternFill("solid", fgColor="FFF2CC")
        wq[f"C{k}"].border = BORDA
    wq["D3"] = "← escolha na lista; deixe em branco para ignorar o filtro"
    wq["D3"].font = Font(italic=True, color="7F7F7F")
    dvq = DataValidation(type="list", formula1=f"=Destinos!$A$2:$A${len(todos_dest) + 1}", allow_blank=True)
    wq.add_data_validation(dvq)
    dvq.add("C3:C5")
    wsf = wb.create_sheet("Listas")
    for k, f in enumerate(FAMILIAS, start=1):
        wsf.cell(row=k, column=1, value=f)
    wsf.sheet_state = "hidden"
    dvf = DataValidation(type="list", formula1=f"=Listas!$A$1:$A${len(FAMILIAS)}", allow_blank=True)
    wq.add_data_validation(dvf)
    dvf.add("C7")
    dvd = DataValidation(type="whole", operator="between", formula1="1", formula2="30", allow_blank=True)
    wq.add_data_validation(dvd)
    dvd.add("C6")

    wq["B9"] = "=COUNT(Matriz!$%s$%d:$%s$%d)&\" roteiro(s) encontrado(s)\"" % (L(col_aux), PRIM, L(col_aux), ULT)
    wq["B9"].font = Font(bold=True, color=VERDE_ECO)
    cab_q = ["#", "ROTEIRO", "FAMÍLIA", "DIAS", "NOITES", "A PARTIR DE", "TRAJETO (noites)"]
    for j, t in enumerate(cab_q, start=1):
        cel = wq.cell(row=10, column=j, value=t)
        cel.font = Font(bold=True, color=BRANCO)
        cel.fill = PatternFill("solid", fgColor=PRETO)
        cel.alignment = Alignment(horizontal="center")
    aux = f"Matriz!${L(col_aux)}${PRIM}:${L(col_aux)}${ULT}"
    fontes = {2: "B", 3: "A", 4: "C", 5: "D", 6: "E", 7: L(col_traj)}
    for n in range(1, len(ordem) + 1):
        r = 10 + n
        wq.cell(row=r, column=1, value=f'=IF(COUNT({aux})>={n},{n},"")')
        for j, colm in fontes.items():
            cel = wq.cell(row=r, column=j,
                          value=f'=IF($A{r}="","",INDEX(Matriz!${colm}:${colm},SMALL({aux},$A{r})))')
            cel.alignment = Alignment(vertical="center", wrap_text=(j == 7),
                                      horizontal="center" if j in (4, 5) else None)
        wq.cell(row=r, column=6).number_format = '"R$" #,##0'
        wq.cell(row=r, column=2).font = Font(bold=True)
    for col, w in zip("ABCDEFG", [4, 30, 16, 6, 7, 14, 90]):
        wq.column_dimensions[col].width = w
    wq.column_dimensions["B"].width = 30
    wq.freeze_panes = "A11"

    # ------------------------------------------------------------ Como usar
    wh = wb.create_sheet("Como usar")
    textos = [
        ("COMO USAR E MANTER", True),
        ("", False),
        ("Matriz: uma linha por roteiro, uma coluna por destino (ordem geográfica). O número é a "
         "quantidade de noites; ● indica visita sem pernoite; vazio indica que o roteiro não passa ali.", False),
        ("Filtros: use as setas da linha 6 para filtrar por família, duração, ou por um destino "
         "(ex.: filtre a coluna Atins por 'não vazio').", False),
        ("Busca: escolha até 3 destinos, duração máxima e família. A lista e o destaque amarelo "
         "na Matriz se atualizam sozinhos.", False),
        ("", False),
        ("PARA INCLUIR OU CORRIGIR UM ROTEIRO", True),
        ("Esta planilha é gerada automaticamente. Mudanças feitas aqui não voltam para o guia: edite os "
         "arquivos roteiros.csv e paradas.csv (pasta matriz_destinos/dados do repositório) e rode "
         "'python3 matriz_destinos/gerar.py', que valida os dados e gera de novo a planilha e a página.", False),
        ("", False),
        ("Fonte: PDFs de 2026 (versão 2 pessoas) de cada pasta em Roteiros/Drive, lidos em 04/11/2026. "
         "O trajeto é o mesmo para todas as bases de pessoas.", False),
        ("Observações: Preá Experience e Alhurez/Alhurez Sense são cotados em categoria Stars. "
         "Econômicas e Mini pacotes só informam parcela em 12x no PDF.", False),
    ]
    for k, (t, b) in enumerate(textos, start=1):
        cel = wh.cell(row=k, column=1, value=t)
        cel.font = Font(bold=b, size=12 if b else 11, color=VERDE_ECO if b else "000000")
        cel.alignment = Alignment(wrap_text=True, vertical="top")
    wh.column_dimensions["A"].width = 120

    wb._sheets = [wb["Matriz"], wb["Busca"], wb["Base"], wb["Destinos"], wb["Como usar"], wb["Listas"]]
    wb.active = 0
    SAIDA.parent.mkdir(exist_ok=True)
    wb.save(SAIDA)
    print(f"OK: {SAIDA}  ({len(ordem)} roteiros, {len(todos_dest)} destinos, {n_paradas} linhas na Base)")


if __name__ == "__main__":
    main()
