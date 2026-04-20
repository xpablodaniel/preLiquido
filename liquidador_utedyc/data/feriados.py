"""Feriados nacionales y utilidades de consulta por periodo."""

from datetime import date, datetime


FERIADOS_2026 = [
    "2026-01-01",  # Año Nuevo
    "2026-02-16",  # Carnaval
    "2026-02-17",  # Carnaval
    "2026-03-24",  # Memoria, Verdad y Justicia
    "2026-04-02",  # Malvinas
    "2026-04-03",  # Viernes Santo
    "2026-05-01",  # Día del Trabajador
    "2026-05-25",  # Revolución de Mayo
    "2026-06-15",  # Güemes (trasladable)
    "2026-06-20",  # Belgrano
    "2026-07-09",  # Independencia
    "2026-08-17",  # San Martín (trasladable)
    "2026-10-12",  # Diversidad Cultural
    "2026-11-23",  # Soberanía Nacional (trasladable)
    "2026-12-08",  # Inmaculada Concepción
    "2026-12-25",  # Navidad
]


FERIADOS_POR_ANIO = {
    2026: FERIADOS_2026,
}


def obtener_feriados_anio(anio: int) -> list[str]:
    return FERIADOS_POR_ANIO.get(anio, [])


def obtener_feriados_mes(mes: str) -> list[str]:
    anio_str, mes_str = mes.split("-")
    anio = int(anio_str)
    return [fecha for fecha in obtener_feriados_anio(anio) if fecha.startswith(f"{anio_str}-{mes_str}")]


def obtener_feriados_periodo_20_20(mes: str) -> list[str]:
    anio_str, mes_str = mes.split("-")
    anio = int(anio_str)
    mes_num = int(mes_str)

    fecha_hasta = date(anio, mes_num, 20)
    if mes_num == 1:
        fecha_desde = date(anio - 1, 12, 20)
    else:
        fecha_desde = date(anio, mes_num - 1, 20)

    feriados = []
    for anio_consulta in (fecha_desde.year, fecha_hasta.year):
        for fecha_str in obtener_feriados_anio(anio_consulta):
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
            if fecha_desde <= fecha <= fecha_hasta:
                feriados.append(fecha_str)

    return sorted(set(feriados))
