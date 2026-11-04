"""Um comando só: valida os dados e gera a planilha e a página.

    python3 gerar.py
"""
import sys

import gerar_pagina
import gerar_planilha
import validar

if __name__ == "__main__":
    if validar.main() != 0:
        sys.exit("Corrija os dados acima antes de gerar.")
    gerar_planilha.main()
    gerar_pagina.main()
