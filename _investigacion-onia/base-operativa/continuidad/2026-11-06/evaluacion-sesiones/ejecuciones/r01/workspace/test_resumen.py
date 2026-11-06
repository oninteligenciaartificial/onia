import copy
import unittest

from resumen import subtotal


def fila(unidades=1, precio="1.00", estado="activo"):
    return dict(unidades=unidades, precio=precio, estado=estado)


class SubtotalTests(unittest.TestCase):
    def test_normales_y_entrada_intacta(self):
        pedido = [fila(2, "1.25"), fila(3, "0.10"), fila(8, "10", "anulado")]
        original = copy.deepcopy(pedido)
        self.assertEqual(subtotal(pedido), "2.80")
        self.assertEqual(pedido, original)

    def test_vacios_y_ceros(self):
        for pedido in ([], [fila(0, "15")], [fila(2, "10", "anulado")]):
            with self.subTest(pedido=pedido):
                self.assertEqual(subtotal(pedido), "0.00")

    def test_half_up(self):
        self.assertEqual(subtotal([fila(precio="1.005")]), "1.01")
        self.assertEqual(subtotal([fila(precio="2.675")]), "2.68")

    def test_redondea_al_final(self):
        self.assertEqual(subtotal([fila(precio="0.004"), fila(precio="0.004")]), "0.01")

    def test_precision_decimal(self):
        self.assertEqual(subtotal([fila(precio="123456789012345678901234567890.005")]),
                         "123456789012345678901234567890.01")

    def test_fallos_incluso_en_anulados(self):
        for estado in ("activo", "anulado"):
            for invalida in (fila(-1, estado=estado), fila(precio="-0.01", estado=estado),
                             fila(precio="NaN", estado=estado), fila(precio="Infinity", estado=estado),
                             fila(precio="texto", estado=estado), fila(1.5, estado=estado)):
                with self.subTest(fila=invalida):
                    with self.assertRaises(ValueError):
                        subtotal([invalida])
        with self.assertRaises(ValueError):
            subtotal([fila(estado="desconocido")])


if __name__ == "__main__":
    unittest.main()
