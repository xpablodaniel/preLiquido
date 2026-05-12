"""Coeficientes mensuales publicados por UTEDYC para conceptos variables.

UTEDYC publica cada mes los valores unitarios reales para los conceptos
que no se derivan algebraicamente del básico (feriado, nocturno, adicional
feriado). Cuando el mes está cargado aquí, la app usa estos valores
en lugar de la fórmula de aproximación.

Fuente: circulares mensuales de UTEDYC / recibos de referencia.

NOTA: Meses sin coeficientes explícitos usarán fórmula de aproximación:
  - feriado_unitario_0229 = basico_categoria / 25
  - adicional_feriado_unitario_0281 = (monto_base_281 * factor_arrastre) * multiplicador
  - valor_nocturno_0283 = 74.018,41 (default desde VARIABLES_DEFAULT)
  
Agregá coeficientes reales cuando recibas recibos de RRHH.
"""

COEFICIENTES_MENSUALES: dict[str, dict[str, float]] = {
    "2026-02": {
        # COD 0229 – Feriado nacional trabajado (valor unitario por feriado).
        # Verificado contra recibo RRHH: 82.818,55 × 2 = 165.637,10
        "feriado_unitario_0229": 82_818.55,

        # COD 0281 – Adicional por feriado (unitario publicado por UTEDYC).
        # Verificado contra recibo RRHH: 8.831,275 × 2 = 17.662,55
        "adicional_feriado_unitario_0281": 8_831.275,

        # COD 0283 – Turno nocturno (valor hora nocturna mensual UTEDYC).
        # Verificado contra recibo RRHH: 75.306,42 × 6 = 451.838,52 (≈ 451.838,53)
        "valor_nocturno_0283": 75_306.42,

        # COD 6982 – Retención de ganancias 4ª categoría (importe fijo mensual).
        "retenciones_ganancias_6982": 2_092.34,
    },
    "2026-03": {
        # COD 0283 – Turno nocturno (valor hora nocturna mensual UTEDYC).
        # Verificado contra recibo RRHH: 74.018,408 × 6 = 444.110,45
        "valor_nocturno_0283": 74_018.408,

        # COD 0281 – Adicional por feriado (unitario publicado por UTEDYC).
        # Marzo no tiene feriados en período 20-20, pero se liquida base.
        # Verificado contra recibo RRHH: 32.534,21 (1 unidad)
        "adicional_feriado_unitario_0281": 32_534.21,

        # COD 6982 – Retención de ganancias 4ª categoría (importe negativo = reintegro).
        "retenciones_ganancias_6982": -818.22,
    },
    "2026-04": {
        # COD 0229 – Feriado nacional trabajado (valor unitario por feriado).
        # Verificado contra recibo RRHH: 84.046,706 × 3 = 252.140,12
        "feriado_unitario_0229": 84_046.706,

        # COD 0281 – Adicional por feriado (unitario publicado por UTEDYC).
        # Verificado contra recibo RRHH: 9.338,52 × 3 = 28.015,57 (≈ 28.015,56)
        "adicional_feriado_unitario_0281": 9_338.52,

        # COD 0283 – Turno nocturno (valor hora nocturna mensual UTEDYC).
        # Verificado contra recibo RRHH: 71.630,716 × 6 = 429.784,30
        "valor_nocturno_0283": 71_630.716,
    },
    # ── MESES FUTUROS: agregar coeficientes cuando lleguen recibos reales ──
    # "2026-05": { ... },
    # "2026-06": { ... },
    # ... etc.
}
