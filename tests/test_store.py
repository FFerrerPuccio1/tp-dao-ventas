import unittest
from datetime import datetime

from ui.render import pagina
from ui.store import Store, clave_ok, hash_clave


class FlujoTest(unittest.TestCase):
    def test_cuit_duplicado(self):
        store = Store()
        error = store.guardar_proveedor({
            "cuit": "30-71234567-8", "razon": "Otro", "tel": "1", "email": "a@b.c",
            "rubros": [], "activo": True, "cuit_original": "",
        }, True)
        self.assertIn("TecnoSur", error)

    def test_precinto_y_despacho(self):
        store = Store()
        self.assertIn("precintar", store.despachar("BUL-2026-0101").lower())
        self.assertIsNotNone(store.precintar("BUL-2026-0101", "PREC-774102"))
        self.assertIsNone(store.precintar("BUL-2026-0101", "PREC-100001"))
        antes = store.st("CD-01", "PROD-0014")["disp"]
        self.assertIsNone(store.despachar("BUL-2026-0101"))
        self.assertEqual(store.bulto("BUL-2026-0101")["estado"], "EN_TRANSITO")
        self.assertEqual(store.st("CD-01", "PROD-0014")["disp"], antes - 20)
        self.assertEqual(store.st("LOC-01", "PROD-0014")["transito"], 40 + 20)

    def test_verificar_libera_stock_y_rechazo_no(self):
        store = Store()
        antes = store.st("LOC-01", "PROD-0014")["disp"]
        self.assertIsNone(store.verificar("BUL-2026-0099"))
        self.assertEqual(store.st("LOC-01", "PROD-0014")["disp"], antes + 30)
        self.assertEqual(store.st("LOC-01", "PROD-0014")["cuarentena"], 0)

        store = Store()
        antes = store.st("LOC-01", "PROD-0014")["disp"]
        self.assertIsNone(store.rechazar("BUL-2026-0099", "Precinto cortado"))
        self.assertEqual(store.st("LOC-01", "PROD-0014")["disp"], antes)
        self.assertEqual(store.bulto("BUL-2026-0099")["estado"], "RECHAZADO")

    def test_venta_no_supera_stock_y_devolucion(self):
        store = Store()
        self.assertIn("12", store.agregar_carrito("PROD-0014", 13))
        self.assertIsNone(store.agregar_carrito("PROD-0014", 2))
        error, nro = store.cobrar("efectivo", {"paga_con": "1"})
        self.assertIsNone(nro)
        self.assertIsNotNone(error)
        error, nro = store.cobrar("efectivo", {"paga_con": "50000"})
        self.assertIsNone(error)
        self.assertEqual(store.st("LOC-01", "PROD-0014")["disp"], 10)
        self.assertIn("2 u", store.confirmar_devolucion("TCK-LOC01-000451", {"PROD-0014": 3}, "cambio"))
        self.assertIsNone(store.confirmar_devolucion("TCK-LOC01-000451", {"PROD-0014": 1}, "cambio"))
        self.assertEqual(store.st("LOC-01", "PROD-0014")["disp"], 11)
        self.assertIn("no encontrado", store.confirmar_devolucion("TCK-NO", {}, "x").lower())
        store.ventas.append({
            "nro": "TCK-VIEJO", "local": "LOC-01", "fecha": datetime(2026, 1, 1),
            "medio": "efectivo", "ref": "", "total": 100, "items": [
                {"sku": "PROD-0063", "qty": 1, "devuelta": 0, "precio": 100, "costo": 50},
            ],
        })
        self.assertIn("30", store.confirmar_devolucion("TCK-VIEJO", {"PROD-0063": 1}, "tarde"))

    def test_pagina_y_clave(self):
        corte, n, pages, total, ini = pagina(list(range(25)), {"p": "2"})
        self.assertEqual(corte, list(range(10, 20)))
        self.assertEqual((n, pages, total, ini), (2, 3, 25, 10))
        corte, n, pages, total, ini = pagina(list(range(3)), {"p": "9"})
        self.assertEqual(n, 1)
        self.assertEqual(corte, [0, 1, 2])
        guardada = hash_clave("cd")
        self.assertTrue(clave_ok(guardada, "cd"))
        self.assertFalse(clave_ok(guardada, "no"))

    def test_margen_descuenta_cmv_y_merma(self):
        store = Store()
        rep = store.reporte_comercial(datetime(2026, 10, 1), datetime(2026, 10, 23, 23, 59, 59), "", "")
        self.assertEqual(rep["margen"], rep["ingresos"] - rep["cmv"] - rep["merma"])
        self.assertEqual(rep["ingresos"], 54700)
        self.assertGreater(rep["merma"], 0)


if __name__ == "__main__":
    unittest.main()
