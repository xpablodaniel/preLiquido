"""Test de liquidación real abril 2026 — Herrera Pablo Daniel.

Valores de referencia tomados del recibo oficial emitido por RRHH / SUTEBa.
El test verifica que la app replica exactamente los conceptos remunerativos
y los descuentos base (sin el ajuste de ganancias de período anterior,
que es un movimiento contable único y no reproducible).
"""

import unittest

from logic.calculos import liquidar
from logic.modelos import Asistencia, Empleado


EMPLEADO_HERRERA = Empleado(
    categoria="D",
    antiguedad_anios=10,
    titulo_secundario=True,
    maquina_contable=True,
    permanencia_categoria=True,
    quebranto_caja=True,
    exigencia_operativa=True,
    refrigerio=True,
    cuota_sindical=True,
)

ASISTENCIA_ABRIL_2026 = Asistencia(
    feriados_trabajados=3,
    nocturnos=6,
    horas_extras=0,
)

MES = "2026-04"


class LiquidacionAbril2026TestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.resultado = liquidar(EMPLEADO_HERRERA, ASISTENCIA_ABRIL_2026, MES)
        self.vars = self.resultado["adicionales_variables"]
        self.fijos = self.resultado["adicionales_fijos"]
        self.porcent = self.resultado["adicionales_porcentuales"]
        self.descuentos = self.resultado["descuentos"]

    # ── Básico ───────────────────────────────────────────────────────────────
    def test_basico(self) -> None:
        self.assertAlmostEqual(self.resultado["basico"], 1_150_520.00, places=2)

    # ── Adicionales porcentuales ─────────────────────────────────────────────
    def test_puntualidad_0214(self) -> None:
        self.assertAlmostEqual(self.porcent["puntualidad"], 176_899.50, places=2)

    def test_antiguedad_0216(self) -> None:
        self.assertAlmostEqual(self.porcent["antiguedad"], 235_866.00, places=2)

    def test_titulo_secundario_0273(self) -> None:
        self.assertAlmostEqual(self.porcent["titulo_secundario"], 117_933.00, places=2)

    def test_maquina_contable_0274(self) -> None:
        self.assertAlmostEqual(self.porcent["maquina_contable"], 117_933.00, places=2)

    def test_permanencia_categoria_0720(self) -> None:
        self.assertAlmostEqual(self.porcent["permanencia_categoria"], 70_759.80, places=2)

    def test_plus_temporada_0227(self) -> None:
        # Abril = mes 4 → cierre de temporada al 12 %.
        self.assertAlmostEqual(self.porcent["plus_temporada"], 141_519.60, places=2)

    # ── Adicionales fijos ────────────────────────────────────────────────────
    def test_quebranto_caja_0218(self) -> None:
        self.assertAlmostEqual(self.fijos["quebranto_caja_0218"], 117_933.00, places=2)

    def test_refrigerio_0719(self) -> None:
        self.assertAlmostEqual(self.fijos["refrigerio_0719"], 566_078.40, places=2)

    # ── Adicionales variables (coeficientes mensuales reales) ─────────────────
    def test_feriados_nacionales_0229(self) -> None:
        # 3 feriados × 84.046,706 = 252.140,12
        self.assertAlmostEqual(self.vars["feriados_nacionales_0229"], 252_140.12, places=1)

    def test_feriado_unitario_0229(self) -> None:
        self.assertAlmostEqual(self.vars["feriado_unitario"], 84_046.706, places=2)

    def test_adicional_feriado_0281(self) -> None:
        # 3 feriados × 9.338,52 = 28.015,56 ≈ 28.015,57
        self.assertAlmostEqual(self.vars["adicional_feriado_0281"], 28_015.56, places=1)

    def test_nocturnos_0283(self) -> None:
        # 6 turnos × 71.630,716 = 429.784,30
        self.assertAlmostEqual(self.vars["nocturnos"], 429_784.30, places=1)

    # ── Total remunerativo ───────────────────────────────────────────────────
    def test_total_remunerativo(self) -> None:
        # Verificado contra recibo RRHH: 3.589.465,49
        self.assertAlmostEqual(self.resultado["total_remunerativo"], 3_589_465.49, delta=5.0)

    # ── Descuentos base (sin ajuste ganancias período anterior) ─────────────
    def test_jubilacion_0401(self) -> None:
        self.assertAlmostEqual(self.descuentos["jubilacion"], 394_841.20, delta=2.0)

    def test_ley_19032_0402(self) -> None:
        self.assertAlmostEqual(self.descuentos["ley_19032"], 107_683.96, delta=2.0)

    def test_ley_23660_0405(self) -> None:
        self.assertAlmostEqual(self.descuentos["ley_23660"], 107_683.96, delta=2.0)

    def test_cuota_sindical_0426(self) -> None:
        self.assertAlmostEqual(self.descuentos["cuota_sindical"], 107_683.96, delta=2.0)

    # ── Feriados del período ─────────────────────────────────────────────────
    def test_feriados_periodo_20_20(self) -> None:
        self.assertEqual(self.resultado["feriados_periodo_20_20"]["cantidad"], 3)
        self.assertEqual(
            self.resultado["feriados_periodo_20_20"]["fechas"],
            ["2026-03-24", "2026-04-02", "2026-04-03"],
        )


if __name__ == "__main__":
    unittest.main()
