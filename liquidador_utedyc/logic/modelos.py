"""Core data models used by the liquidador."""

from dataclasses import dataclass


@dataclass
class Empleado:
    categoria: str
    antiguedad_anios: int
    titulo_secundario: bool = False
    maquina_contable: bool = False
    quebranto_caja: bool = False
    exigencia_operativa: bool = False
    refrigerio: bool = False
    nocturnidad_fija: bool = False
    permanencia_categoria: bool = False
    zona_fria: bool = False
    horario_discontinuo: bool = False
    idiomas: bool = False
    cuota_sindical: bool = False

    def __post_init__(self) -> None:
        if self.antiguedad_anios < 0:
            raise ValueError("La antiguedad no puede ser negativa")


@dataclass
class Asistencia:
    feriados_trabajados: int = 0
    nocturnos: int = 0
    horas_extras: int = 0
    dias_trabajados: int = 30
    dias_licencia: int = 0
    franco_trabajado: int = 0

    def __post_init__(self) -> None:
        campos = {
            "feriados_trabajados": self.feriados_trabajados,
            "nocturnos": self.nocturnos,
            "horas_extras": self.horas_extras,
            "dias_trabajados": self.dias_trabajados,
            "dias_licencia": self.dias_licencia,
            "franco_trabajado": self.franco_trabajado,
        }
        for nombre, valor in campos.items():
            if valor < 0:
                raise ValueError(f"{nombre} no puede ser negativo")


@dataclass
class MesConvenio:
    mes: str

    def __post_init__(self) -> None:
        try:
            anio, mes = self.mes.split("-")
            if len(anio) != 4 or len(mes) != 2:
                raise ValueError
            numero_mes = int(mes)
            if numero_mes < 1 or numero_mes > 12:
                raise ValueError
        except ValueError as exc:
            raise ValueError("El mes debe tener formato YYYY-MM") from exc
