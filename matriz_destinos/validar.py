"""Confere a fonte única de dados antes de gerar qualquer coisa. Sai com código 1 se houver problema."""
import sys

import base


def main():
    b = base.carregar()
    erros = base.validar(b)
    n_rot, n_lin = len(b["roteiros"]), sum(len(r["trajeto"]) for r in b["roteiros"].values())
    if erros:
        print(f"{len(erros)} problema(s) nos dados:")
        for e in erros:
            print(" -", e)
        return 1
    print(f"Dados OK: {n_rot} roteiros, {n_lin} paradas, {len(b['geo'])} destinos, {len(b['familias'])} famílias.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
