"""Testes da fonte única de dados. Rode com:  python3 -m unittest discover matriz_destinos"""
import copy
import unittest

import base


class TestDados(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.b = base.carregar()

    def erros_com(self, mudar):
        b = copy.deepcopy(self.b)
        mudar(b)
        return base.validar(b)

    def test_dados_atuais_validos(self):
        self.assertEqual(base.validar(self.b), [])

    def test_contagens(self):
        self.assertEqual(len(self.b["roteiros"]), 46)
        self.assertEqual(len(self.b["ordem_familias"]), 14)

    def test_ordem_de_exibicao(self):
        pos = {f: i for i, f in enumerate(self.b["ordem_familias"])}
        chaves = [(pos[r["familia"]], r["dias"], n) for n, r in self.b["roteiros"].items()]
        self.assertEqual(chaves, sorted(chaves))

    def test_pega_soma_de_noites_errada(self):
        def mudar(b): b["roteiros"]["Essencial"]["trajeto"][1]["noites"] += 1
        self.assertTrue(any("soma das noites" in e for e in self.erros_com(mudar)))

    def test_pega_destino_inexistente(self):
        def mudar(b): b["roteiros"]["Rota das Dunas"]["trajeto"][0]["destino"] = "Cidade X/MA"
        self.assertTrue(any("Cidade X/MA" in e for e in self.erros_com(mudar)))

    def test_pega_familia_inexistente(self):
        def mudar(b): b["roteiros"]["Essencial"]["familia"] = "Inexistente"
        self.assertTrue(any("Inexistente" in e for e in self.erros_com(mudar)))

    def test_pega_ordem_quebrada(self):
        def mudar(b): b["roteiros"]["Essencial"]["trajeto"][2]["ordem"] = 9
        self.assertTrue(any("ordem do trajeto" in e for e in self.erros_com(mudar)))

    def test_pega_pasta_ausente(self):
        def mudar(b): b["roteiros"]["Essencial"]["pasta"] = ""
        self.assertTrue(any("pasta" in e for e in self.erros_com(mudar)))

    def test_pega_pasta_repetida(self):
        def mudar(b): b["roteiros"]["Essencial Plus"]["pasta"] = b["roteiros"]["Essencial"]["pasta"]
        self.assertTrue(any("mais de um roteiro" in e for e in self.erros_com(mudar)))

    def test_pega_parada_de_roteiro_inexistente(self):
        def mudar(b): b["paradas_orfas"].append("Roteiro Fantasma")
        self.assertTrue(any("Roteiro Fantasma" in e for e in self.erros_com(mudar)))

    def test_todo_destino_tem_coordenada(self):
        for r in self.b["roteiros"].values():
            for p in r["trajeto"]:
                self.assertIn(p["destino"], self.b["geo"])


if __name__ == "__main__":
    unittest.main()
