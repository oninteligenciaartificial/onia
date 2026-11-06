import copy
import unittest

from resumen import subtotal


def fila(unidades=1, precio="1.00", estado="activo"):
    return {"unidades": unidades, "precio": precio, "estado": estado}


class SubtotalTests(unittest.TestCase):
    def test_normales(self):
        casos = [
            ([], "0.00"),
            ([fila(2, "3.10"), fila(1, "0.20")], "6.40"),
            ([fila(2, "3.10"), fila(99, "9.99", "anulado")], "6.20"),
            ([fila(1, "10.00", "anulado")], "0.00"),
            ([fila(0, "99.99")], "0.00"),
            ([fila(1, "1.005")], "1.01"),
            ([fila(1, "0.004"), fila(1, "0.004")], "0.01"),
            ([fila(3, "0.10")], "0.30"),
            ([fila(1, "9999999999999999999999999999.995")],
             "10000000000000000000000000000.00"),
        ]
        for pedido, esperado in casos:
            with self.subTest(pedido=pedido):
                original = copy.deepcopy(pedido)
                self.assertEqual(subtotal(pedido), esperado)
                self.assertEqual(pedido, original)

    def test_fallos(self):
        for estado in ("activo", "anulado"):
            for invalida in (fila(-1, estado=estado), fila(precio="-0.01", estado=estado)):
                with self.subTest(invalida=invalida):
                    original = copy.deepcopy(invalida)
                    with self.assertRaises(ValueError):
                        subtotal([invalida])
                    self.assertEqual(invalida, original)
        with self.assertRaises(ValueError):
            subtotal([fila(estado="pendiente")])


if __name__ == "__main__":
    unittest.main()
