"""CLI entrypoint for payroll projection."""

import argparse
import json

from logic.calculos import comparar_liquidaciones, liquidar
from logic.modelos import Asistencia, Empleado


COEF_FERIADO_0229 = 2.0
COEF_ADICIONAL_0281 = 1.0
ALICUOTA_GANANCIAS = 0.0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Liquidador UTEDYC 183/92")
    parser.add_argument("--mes", required=True, help="Mes base en formato YYYY-MM")
    parser.add_argument("--mes-objetivo", help="Mes objetivo para comparar, formato YYYY-MM")
    parser.add_argument("--comparar", action="store_true", help="Compara mes base contra mes objetivo")
    parser.add_argument("--categoria", required=True, help="Categoria segun escala vigente del mes")
    parser.add_argument("--antiguedad", type=int, default=0, help="Anios de antiguedad")
    parser.add_argument("--titulo", action="store_true", help="Aplica titulo secundario")
    parser.add_argument("--maquina", action="store_true", help="Aplica maquina contable")
    parser.add_argument("--permanencia", action="store_true", help="Aplica permanencia de categoria")
    parser.add_argument("--quebranto", action="store_true", help="Aplica quebranto de caja (COD 0218)")
    parser.add_argument(
        "--exigencia-operativa",
        action="store_true",
        help="Aplica adicional por exigencia operativa (COD 0276)",
    )
    parser.add_argument("--refrigerio", action="store_true", help="Aplica refrigerio (COD 0719)")
    parser.add_argument("--feriados", type=int, default=0, help="Cantidad de feriados trabajados")
    parser.add_argument(
        "--valor-feriado-manual",
        type=float,
        help="Sobrescribe el valor unitario de feriado trabajado",
    )
    parser.add_argument("--nocturnos", type=int, default=0, help="Cantidad de turnos nocturnos")
    parser.add_argument("--extras", type=int, default=0, help="Cantidad de horas extras")
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if args.comparar and not args.mes_objetivo:
        raise ValueError("Si usas --comparar, debes informar --mes-objetivo")

    empleado = Empleado(
        categoria=args.categoria,
        antiguedad_anios=args.antiguedad,
        titulo_secundario=args.titulo,
        maquina_contable=args.maquina,
        quebranto_caja=args.quebranto,
        exigencia_operativa=args.exigencia_operativa,
        refrigerio=args.refrigerio,
        permanencia_categoria=args.permanencia,
        cuota_sindical=True,
    )
    asistencia = Asistencia(
        feriados_trabajados=args.feriados,
        nocturnos=args.nocturnos,
        horas_extras=args.extras,
    )

    if args.comparar:
        resultado = comparar_liquidaciones(
            empleado,
            asistencia,
            mes_base=args.mes,
            mes_objetivo=args.mes_objetivo,
            alicuota_ganancias=ALICUOTA_GANANCIAS,
            coef_feriado=COEF_FERIADO_0229,
            valor_feriado_manual=args.valor_feriado_manual,
            coef_adicional_feriado=COEF_ADICIONAL_0281,
        )
    else:
        resultado = liquidar(
            empleado,
            asistencia,
            args.mes,
            alicuota_ganancias=ALICUOTA_GANANCIAS,
            coef_feriado=COEF_FERIADO_0229,
            valor_feriado_manual=args.valor_feriado_manual,
            coef_adicional_feriado=COEF_ADICIONAL_0281,
        )

    print(json.dumps(resultado, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
