"""Convenio percentages and default rates used by the calculator."""

ADICIONALES = {
    "puntualidad": 0.15,
    "antiguedad_por_anio": 0.02,
    "titulo_secundario": 0.10,
    "maquina_contable": 0.10,
    "permanencia_categoria": 0.06,
    "quebranto_caja": 0.10,
    # Calibrado con recibos de diciembre y marzo.
    "exigencia_operativa": 0.15608964,
    # Calibrado con recibos de diciembre y marzo.
    "refrigerio": 0.48,
    "plus_temporada_20": 0.20,
    "plus_temporada_12": 0.12,
}

DESCUENTOS = {
    "jubilacion": 0.11,
    "ley_19032": 0.03,
    "ley_23660": 0.03,
    "cuota_sindical": 0.03,
}


VARIABLES_DEFAULT = {
    # Calibrados segun recibos de referencia.
    "valor_nocturno": 74018.41,
    "valor_hora_extra": 15000.00,
}


CONCEPTOS_FIJOS_DEFAULT = {
    # Ítem 229 – Feriado nacional trabajado
    # Fórmula legal: sueldo_mensual / 25
    # Se calcula dinámicamente en calculos.py
    "coef_feriado_229": 1 / 25,

    # Ítem 281 – Adicional por feriado
    # Politica empresa: valor base mensual con arrastre por aumentos.
    "monto_base_281": 15000.0,
    # Mes de referencia para arrastre por aumentos (indexado por basico B).
    "mes_base_281": "2025-11",
}
