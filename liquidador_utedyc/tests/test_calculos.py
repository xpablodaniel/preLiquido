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


    def test_simulacion_camarero_mar26(self) -> None:
        """Simulacion perfil camarero: cat B, 8 anios, horario discontinuo,
        comida incluida, 10 hs extras, 1 franco trabajado, 1 feriado."""
        empleado = Empleado(
            categoria="B",
            antiguedad_anios=8,
            titulo_secundario=True,
            horario_discontinuo=True,
            diario_comida=True,
        )
        asistencia = Asistencia(
            feriados_trabajados=1,
            nocturnos=8,
            horas_extras=10,
            franco_trabajado=1,
            dias_trabajados=30,
        )
        resultado = liquidar(empleado, asistencia, "2026-03")

        # Basico y adicionales porcentuales.
        self.assertAlmostEqual(resultado["basico"], 1179330.0, places=2)
        self.assertAlmostEqual(resultado["adicionales_porcentuales"]["horario_discontinuo"], 117933.0, places=2)
        self.assertAlmostEqual(resultado["adicionales_porcentuales"]["plus_temporada"], 235866.0, places=2)

        # Franco: debe ser 2 x feriado_unitario.
        feriado_u = resultado["adicionales_variables"]["feriado_unitario"]
        franco_u = resultado["adicionales_variables"]["franco_unitario"]
        self.assertAlmostEqual(franco_u, feriado_u * 2, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["franco_trabajado"], 188692.80, places=2)

        # Hora extra dinamica.
        self.assertAlmostEqual(resultado["adicionales_variables"]["hora_extra_unitaria"], 11793.30, places=2)
        self.assertAlmostEqual(resultado["adicionales_variables"]["horas_extras"], 117933.0, places=2)

        # Diario comida sobre 30 dias.
        self.assertAlmostEqual(resultado["adicionales_fijos"]["diario_comida_0280"], 707598.0, places=2)

        # Totales generales.
        self.assertAlmostEqual(resultado["total_remunerativo"], 3733548.26, places=2)
        self.assertAlmostEqual(resultado["neto_estimado"], 2986838.61, places=2)

        # Todos los CODs presentes en items_cod.
        cods = {item["cod"] for item in resultado["items_cod"]["remunerativos"]}
        for cod in ("0201", "0214", "0216", "0227", "0229", "0231", "0232",
                    "0273", "0280", "0281", "0283"):
            self.assertIn(cod, cods, msg=f"COD {cod} ausente en items_cod")


if __name__ == "__main__":
    unittest.main()
