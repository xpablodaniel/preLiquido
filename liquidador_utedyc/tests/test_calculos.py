import unittest

from data.feriados import obtener_feriados_periodo_20_20
from logic.calculos import comparar_liquidaciones, liquidar
from logic.modelos import Asistencia, Empleado


class CalculosTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.empleado = Empleado(
            categoria="D",
            antiguedad_anios=10,
            titulo_secundario=True,
            maquina_contable=True,
            permanencia_categoria=True,
            cuota_sindical=True,
        )
        self.asistencia = Asistencia(
            feriados_trabajados=2,
            nocturnos=6,
            horas_extras=0,
        )

    def test_liquidacion_retorna_neto_positivo(self) -> None:
        resultado = liquidar(self.empleado, self.asistencia, "2026-03")
        self.assertGreater(resultado["neto_estimado"], 0)
        self.assertIn("feriados_periodo_20_20", resultado)
        self.assertGreater(len(resultado["alertas"]), 0)
        self.assertIn("items_cod", resultado)
        self.assertIn("adicionales_fijos", resultado)
        self.assertAlmostEqual(resultado["adicionales_variables"]["feriado_unitario"], 92041.60, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["nocturnos"], 444110.46, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["feriados_nacionales_0229"], 184083.20, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["adicional_feriado_0281"], 32352.96, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["feriados_trabajados"], 216436.16, places=2)

    def test_comparacion_fin_temporada(self) -> None:
        comparacion = comparar_liquidaciones(
            self.empleado,
            self.asistencia,
            mes_base="2026-03",
            mes_objetivo="2026-04",
        )
        delta_neto = comparacion["diferencias"]["delta_neto"]
        self.assertLess(delta_neto, 0)

    def test_feriados_periodo_20_20_abril_2026(self) -> None:
        feriados = obtener_feriados_periodo_20_20("2026-04")
        self.assertEqual(feriados, ["2026-03-24", "2026-04-02", "2026-04-03"])

    def test_feriado_manual_sobrescribe_formula(self) -> None:
        resultado = liquidar(
            self.empleado,
            self.asistencia,
            "2026-01",
            valor_feriado_manual=80000.0,
            coef_adicional_feriado=0.0,
        )
        self.assertAlmostEqual(resultado["adicionales_variables"]["feriado_unitario"], 80000.0, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["feriados_trabajados"], 160000.0, places=2)

    def test_0281_sale_de_basico_b(self) -> None:
        resultado = liquidar(self.empleado, self.asistencia, "2026-03")
        self.assertAlmostEqual(resultado["adicionales_variables"]["monto_base_281"], 15000.0, places=2)
        self.assertEqual(resultado["adicionales_variables"]["mes_base_281"], "2025-11")
        self.assertAlmostEqual(resultado["adicionales_variables"]["factor_arrastre_281"], 1.07843, places=4)
        self.assertAlmostEqual(resultado["adicionales_variables"]["adicional_feriado_base_0281"], 16176.48, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["factor_adicional_0281"], 2.0, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["adicional_feriado_0281"], 32352.96, places=2)

    def test_0281_se_paga_sin_feriados(self) -> None:
        asistencia = Asistencia(feriados_trabajados=0, nocturnos=0, horas_extras=0)
        resultado = liquidar(self.empleado, asistencia, "2026-03")
        self.assertAlmostEqual(resultado["adicionales_variables"]["factor_adicional_0281"], 1.0, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["adicional_feriado_0281"], 16176.48, places=2)

    def test_cod_0719_refrigerio_sumado(self) -> None:
        empleado = Empleado(
            categoria="D",
            antiguedad_anios=10,
            refrigerio=True,
        )
        asistencia = Asistencia(feriados_trabajados=0, nocturnos=0, horas_extras=0)
        resultado = liquidar(
            empleado,
            asistencia,
            "2026-03",
        )
        self.assertAlmostEqual(resultado["adicionales_fijos"]["refrigerio_0719"], 566078.40, places=2)
        cod_0719 = next(item for item in resultado["items_cod"]["remunerativos"] if item["cod"] == "0719")
        self.assertAlmostEqual(cod_0719["importe"], 566078.40, places=2)


if __name__ == "__main__":
    unittest.main()
