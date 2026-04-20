"""Convenio percentages and default rates used by the calculator."""

ADICIONALES = {
    # ── Asistencia ──────────────────────────────────────────────────────────
    "puntualidad": 0.15,
    # ── Antigüedad ──────────────────────────────────────────────────────────
    "antiguedad_por_anio": 0.02,
    # ── Títulos / capacitación ───────────────────────────────────────────────
    "titulo_secundario": 0.10,
    "tecnico": 0.15,
    # ── Función / cargo ──────────────────────────────────────────────────────
    "oficial_mantenimiento": 0.12,
    "medio_oficial_mantenimiento": 0.06,
    "mayor_funcion_30": 0.30,
    "mayor_funcion_25": 0.25,
    "mayor_funcion_20": 0.20,
    "mayor_funcion_18": 0.18,
    "liquidacion_sueldos": 0.04,
    "permanencia_categoria": 0.06,
    # ── Herramientas / operativa ─────────────────────────────────────────────
    "maquina_contable": 0.10,
    "maquina_coser": 0.04,
    "bonificacion_manual": 0.04,
    # ── Condiciones de trabajo ───────────────────────────────────────────────
    "idiomas": 0.10,
    "horario_discontinuo": 0.10,
    "zona_fria": 0.30,
    # ── Quebranto de caja (art. convenio) ────────────────────────────────────
    # Hasta $1.000: 7 %;  desde $1.001: 10 %.
    "quebranto_caja_hasta_1000": 0.07,
    "quebranto_caja": 0.10,
    # ── Vianda / refrigerio ──────────────────────────────────────────────────
    "diario_comida": 0.02,
    "diario_desayuno": 0.01,
    # ── Empresa (calibrados con recibos de referencia) ───────────────────────
    "exigencia_operativa": 0.15608964,
    "refrigerio": 0.48,
    # ── Plus de temporada ────────────────────────────────────────────────────
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
    # Valor por turno nocturno calibrado con recibos de referencia.
    # ATENCION: este valor es estatico y debe actualizarse manualmente
    # con cada acuerdo paritario (no se deriva del basico de categoria).
    "valor_nocturno": 74018.41,
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
