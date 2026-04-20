"""Pure functions for salary settlement calculations."""

from data.adicionales import ADICIONALES, CONCEPTOS_FIJOS_DEFAULT, DESCUENTOS, VARIABLES_DEFAULT
from data.escalas import BASICOS
from data.feriados import obtener_feriados_periodo_20_20
from logic.modelos import Asistencia, Empleado


def obtener_basico(categoria: str, mes: str) -> float:
    if mes not in BASICOS:
        raise KeyError(f"No hay escala cargada para el mes {mes}")
    if categoria not in BASICOS[mes]:
        raise KeyError(f"No existe la categoria {categoria} para el mes {mes}")
    return float(BASICOS[mes][categoria])


def obtener_basico_b(mes: str) -> float:
    return obtener_basico("B", mes)


def _plus_temporada(mes: str) -> float:
    mes_num = int(mes.split("-")[1])
    if mes_num in (12, 1, 2, 3):
        return ADICIONALES["plus_temporada_20"]
    if mes_num == 4:
        return ADICIONALES["plus_temporada_12"]
    return 0.0


def calcular_adicionales_porcentuales(empleado: Empleado, mes: str) -> dict:
    basico_b = obtener_basico_b(mes)
    detalle = {
        "puntualidad": basico_b * ADICIONALES["puntualidad"],
        "antiguedad": basico_b * empleado.antiguedad_anios * ADICIONALES["antiguedad_por_anio"],
        "titulo_secundario": 0.0,
        "tecnico": 0.0,
        "oficial_mantenimiento": 0.0,
        "medio_oficial_mantenimiento": 0.0,
        "mayor_funcion": 0.0,
        "liquidacion_sueldos": 0.0,
        "maquina_contable": 0.0,
        "maquina_coser": 0.0,
        "bonificacion_manual": 0.0,
        "permanencia_categoria": 0.0,
        "idiomas": 0.0,
        "horario_discontinuo": 0.0,
        "zona_fria": 0.0,
        "plus_temporada": basico_b * _plus_temporada(mes),
    }

    if empleado.titulo_secundario:
        detalle["titulo_secundario"] = basico_b * ADICIONALES["titulo_secundario"]
    if empleado.tecnico:
        detalle["tecnico"] = basico_b * ADICIONALES["tecnico"]
    if empleado.oficial_mantenimiento:
        detalle["oficial_mantenimiento"] = basico_b * ADICIONALES["oficial_mantenimiento"]
    if empleado.medio_oficial_mantenimiento:
        detalle["medio_oficial_mantenimiento"] = basico_b * ADICIONALES["medio_oficial_mantenimiento"]
    if empleado.mayor_funcion:
        clave = f"mayor_funcion_{empleado.mayor_funcion}"
        detalle["mayor_funcion"] = basico_b * ADICIONALES[clave]
    if empleado.liquidacion_sueldos:
        detalle["liquidacion_sueldos"] = basico_b * ADICIONALES["liquidacion_sueldos"]
    if empleado.maquina_contable:
        detalle["maquina_contable"] = basico_b * ADICIONALES["maquina_contable"]
    if empleado.maquina_coser:
        detalle["maquina_coser"] = basico_b * ADICIONALES["maquina_coser"]
    if empleado.bonificacion_manual:
        detalle["bonificacion_manual"] = basico_b * ADICIONALES["bonificacion_manual"]
    if empleado.permanencia_categoria:
        detalle["permanencia_categoria"] = basico_b * ADICIONALES["permanencia_categoria"]
    if empleado.idiomas:
        detalle["idiomas"] = basico_b * ADICIONALES["idiomas"]
    if empleado.horario_discontinuo:
        detalle["horario_discontinuo"] = basico_b * ADICIONALES["horario_discontinuo"]
    if empleado.zona_fria:
        detalle["zona_fria"] = basico_b * ADICIONALES["zona_fria"]

    detalle["total"] = sum(v for k, v in detalle.items() if k != "total")
    return detalle


def calcular_adicionales_variables(
    asistencia: Asistencia,
    mes: str,
    basico_categoria: float,
    basico_b: float,
    valores: dict | None = None,
    coef_feriado: float = 2.0,
    valor_feriado_manual: float | None = None,
    coef_adicional_feriado: float | None = None,
) -> dict:
    tabla = valores or VARIABLES_DEFAULT
    if valor_feriado_manual is not None:
        feriado_unitario = float(valor_feriado_manual)
    else:
        # COD 0229: sueldo mensual / 25, con multiplicador opcional para calibracion.
        feriado_unitario = basico_categoria * CONCEPTOS_FIJOS_DEFAULT["coef_feriado_229"] * coef_feriado

    mes_base_281 = CONCEPTOS_FIJOS_DEFAULT["mes_base_281"]
    monto_base_281 = float(CONCEPTOS_FIJOS_DEFAULT["monto_base_281"])
    basico_b_referencia = obtener_basico_b(mes_base_281)
    factor_arrastre_281 = basico_b / basico_b_referencia if basico_b_referencia else 1.0

    multiplicador_0281 = 1.0 if coef_adicional_feriado is None else coef_adicional_feriado
    adicional_feriado_base_0281 = monto_base_281 * factor_arrastre_281
    adicional_feriado_unitario = adicional_feriado_base_0281 * multiplicador_0281
    feriados_0229 = asistencia.feriados_trabajados * feriado_unitario
    # Politica empresa: COD 0281 se liquida todos los meses, y multiplica por cantidad si hay mas de un feriado.
    factor_0281 = max(1, asistencia.feriados_trabajados)
    feriados_0281 = adicional_feriado_unitario * factor_0281

    # COD 0283: hora extra = basico_categoria / 25 / 8 * 2 (tiempo doble, jornada de 8hs).
    hora_extra_unitaria = basico_categoria / 25 / 8 * 2.0
    total_horas_extras = asistencia.horas_extras * hora_extra_unitaria

    # Franco trabajado = 2 × feriado_unitario (el descanso trabajado vale doble feriado).
    franco_unitario = feriado_unitario * 2.0
    total_franco = asistencia.franco_trabajado * franco_unitario

    detalle = {
        "nocturnos": asistencia.nocturnos * tabla["valor_nocturno"],
        "feriado_unitario": feriado_unitario,
        "monto_base_281": monto_base_281,
        "mes_base_281": mes_base_281,
        "factor_arrastre_281": factor_arrastre_281,
        "basico_b_referencia_281": basico_b_referencia,
        "adicional_feriado_base_0281": adicional_feriado_base_0281,
        "adicional_feriado_unitario": adicional_feriado_unitario,
        "factor_adicional_0281": factor_0281,
        "feriados_nacionales_0229": feriados_0229,
        "adicional_feriado_0281": feriados_0281,
        "feriados_trabajados": feriados_0229 + feriados_0281,
        "hora_extra_unitaria": hora_extra_unitaria,
        "horas_extras": total_horas_extras,
        "franco_unitario": franco_unitario,
        "franco_trabajado": total_franco,
    }
    detalle["total"] = (
        detalle["nocturnos"]
        + detalle["feriados_trabajados"]
        + detalle["horas_extras"]
        + detalle["franco_trabajado"]
    )
    return detalle


def calcular_adicionales_fijos(
    empleado: Empleado,
    mes: str,
    asistencia: "Asistencia | None" = None,
) -> dict:
    basico_b = obtener_basico_b(mes)
    dias = asistencia.dias_trabajados if asistencia is not None else 30

    detalle = {
        "base_calculo_categoria_b": basico_b,
        "quebranto_caja_0218": basico_b * ADICIONALES["quebranto_caja"] if empleado.quebranto_caja else 0.0,
        "exigencia_operativa_0276": basico_b * ADICIONALES["exigencia_operativa"] if empleado.exigencia_operativa else 0.0,
        "refrigerio_0719": basico_b * ADICIONALES["refrigerio"] if empleado.refrigerio else 0.0,
        # Diario comida y desayuno: porcentaje diario sobre basico B * dias trabajados.
        "diario_comida_0280": basico_b * ADICIONALES["diario_comida"] * dias if empleado.diario_comida else 0.0,
        "diario_desayuno_0285": basico_b * ADICIONALES["diario_desayuno"] * dias if empleado.diario_desayuno else 0.0,
    }
    detalle["total"] = (
        detalle["quebranto_caja_0218"]
        + detalle["exigencia_operativa_0276"]
        + detalle["refrigerio_0719"]
        + detalle["diario_comida_0280"]
        + detalle["diario_desayuno_0285"]
    )
    return detalle


def _crear_items_cod(
    basico: float,
    adicionales_porcentuales: dict,
    adicionales_variables: dict,
    adicionales_fijos: dict,
    descuentos: dict,
) -> dict:
    remunerativos = [
        {"cod": "0201", "concepto": "Sueldo básico", "importe": basico},
        {"cod": "0214", "concepto": "Asistencia y puntualidad", "importe": adicionales_porcentuales["puntualidad"]},
        {"cod": "0216", "concepto": "Antigüedad", "importe": adicionales_porcentuales["antiguedad"]},
        {"cod": "0218", "concepto": "Quebranto de caja", "importe": adicionales_fijos["quebranto_caja_0218"]},
        {"cod": "0227", "concepto": "Plus por temporada", "importe": adicionales_porcentuales["plus_temporada"]},
        {"cod": "0229", "concepto": "Feriados nacionales", "importe": adicionales_variables["feriados_nacionales_0229"]},
        {"cod": "0273", "concepto": "Título secundario", "importe": adicionales_porcentuales["titulo_secundario"]},
        {"cod": "0274", "concepto": "Maq. computadoras", "importe": adicionales_porcentuales["maquina_contable"]},
        {
            "cod": "0276",
            "concepto": "Adic. var. exigencia operativa",
            "importe": adicionales_fijos["exigencia_operativa_0276"],
        },
        {"cod": "0281", "concepto": "Adicional por feriado", "importe": adicionales_variables["adicional_feriado_0281"]},
        {"cod": "0283", "concepto": "Extras por horario nocturno", "importe": adicionales_variables["nocturnos"]},
        {"cod": "0231", "concepto": "Franco trabajado", "importe": adicionales_variables["franco_trabajado"]},
        {"cod": "0232", "concepto": "Horas extras", "importe": adicionales_variables["horas_extras"]},
        {"cod": "0719", "concepto": "Refrigerio", "importe": adicionales_fijos["refrigerio_0719"]},
        {"cod": "0280", "concepto": "Diario por comida", "importe": adicionales_fijos["diario_comida_0280"]},
        {"cod": "0285", "concepto": "Diario por desayuno", "importe": adicionales_fijos["diario_desayuno_0285"]},
        {
            "cod": "0720",
            "concepto": "Permanencia categoría",
            "importe": adicionales_porcentuales["permanencia_categoria"],
        },
    ]

    descuentos_cod = [
        {"cod": "0401", "concepto": "Jubilación", "importe": descuentos["jubilacion"]},
        {"cod": "0402", "concepto": "Ley 19032", "importe": descuentos["ley_19032"]},
        {"cod": "0405", "concepto": "Ley 23660", "importe": descuentos["ley_23660"]},
        {"cod": "0426", "concepto": "Cuota sindical", "importe": descuentos["cuota_sindical"]},
        {"cod": "6982", "concepto": "Retención de ganancias", "importe": descuentos["ganancias"]},
    ]

    return {
        "remunerativos": remunerativos,
        "descuentos": descuentos_cod,
    }


def calcular_descuentos(total_remunerativo: float, alicuota_ganancias: float = 0.0) -> dict:
    detalle = {
        "jubilacion": total_remunerativo * DESCUENTOS["jubilacion"],
        "ley_19032": total_remunerativo * DESCUENTOS["ley_19032"],
        "ley_23660": total_remunerativo * DESCUENTOS["ley_23660"],
        # COD 0426 obligatorio mientras no cambie el marco legal.
        "cuota_sindical": total_remunerativo * DESCUENTOS["cuota_sindical"],
        "ganancias": 0.0,
    }
    if alicuota_ganancias > 0:
        detalle["ganancias"] = total_remunerativo * alicuota_ganancias

    detalle["total"] = sum(detalle.values())
    return detalle


def liquidar(
    empleado: Empleado,
    asistencia: Asistencia,
    mes: str,
    alicuota_ganancias: float = 0.0,
    coef_feriado: float = 2.0,
    valor_feriado_manual: float | None = None,
    coef_adicional_feriado: float | None = None,
) -> dict:
    basico = obtener_basico(empleado.categoria, mes)
    basico_b = obtener_basico_b(mes)
    adicionales_p = calcular_adicionales_porcentuales(empleado, mes)
    adicionales_v = calcular_adicionales_variables(
        asistencia,
        mes=mes,
        basico_categoria=basico,
        basico_b=basico_b,
        coef_feriado=coef_feriado,
        valor_feriado_manual=valor_feriado_manual,
        coef_adicional_feriado=coef_adicional_feriado,
    )
    adicionales_f = calcular_adicionales_fijos(empleado, mes=mes, asistencia=asistencia)
    feriados_periodo = obtener_feriados_periodo_20_20(mes)
    alertas = []
    if asistencia.feriados_trabajados > len(feriados_periodo):
        alertas.append(
            "Los feriados trabajados informados superan los feriados nacionales del periodo 20-20."
        )

    total_remunerativo = basico + adicionales_p["total"] + adicionales_v["total"] + adicionales_f["total"]
    descuentos = calcular_descuentos(
        total_remunerativo,
        alicuota_ganancias=alicuota_ganancias,
    )
    items_cod = _crear_items_cod(basico, adicionales_p, adicionales_v, adicionales_f, descuentos)

    return {
        "mes": mes,
        "categoria": empleado.categoria,
        "basico": basico,
        "feriados_periodo_20_20": {
            "cantidad": len(feriados_periodo),
            "fechas": feriados_periodo,
            "feriados_trabajados_informados": asistencia.feriados_trabajados,
        },
        "adicionales_porcentuales": adicionales_p,
        "adicionales_variables": adicionales_v,
        "adicionales_fijos": adicionales_f,
        "items_cod": items_cod,
        "total_remunerativo": total_remunerativo,
        "descuentos": descuentos,
        "neto_estimado": total_remunerativo - descuentos["total"],
        "alertas": alertas,
    }


def comparar_liquidaciones(
    empleado: Empleado,
    asistencia: Asistencia,
    mes_base: str,
    mes_objetivo: str,
    alicuota_ganancias: float = 0.0,
    coef_feriado: float = 2.0,
    valor_feriado_manual: float | None = None,
    coef_adicional_feriado: float | None = None,
) -> dict:
    liquidacion_base = liquidar(
        empleado,
        asistencia,
        mes_base,
        alicuota_ganancias=alicuota_ganancias,
        coef_feriado=coef_feriado,
        valor_feriado_manual=valor_feriado_manual,
        coef_adicional_feriado=coef_adicional_feriado,
    )
    liquidacion_objetivo = liquidar(
        empleado,
        asistencia,
        mes_objetivo,
        alicuota_ganancias=alicuota_ganancias,
        coef_feriado=coef_feriado,
        valor_feriado_manual=valor_feriado_manual,
        coef_adicional_feriado=coef_adicional_feriado,
    )

    delta_total = liquidacion_objetivo["total_remunerativo"] - liquidacion_base["total_remunerativo"]
    delta_descuentos = liquidacion_objetivo["descuentos"]["total"] - liquidacion_base["descuentos"]["total"]
    delta_neto = liquidacion_objetivo["neto_estimado"] - liquidacion_base["neto_estimado"]

    return {
        "mes_base": mes_base,
        "mes_objetivo": mes_objetivo,
        "liquidacion_base": liquidacion_base,
        "liquidacion_objetivo": liquidacion_objetivo,
        "diferencias": {
            "delta_total_remunerativo": delta_total,
            "delta_descuentos": delta_descuentos,
            "delta_neto": delta_neto,
        },
    }
