"""Streamlit app for salary projection."""

import streamlit as st

from data.escalas import BASICOS
from data.feriados import obtener_feriados_periodo_20_20
from logic.calculos import comparar_liquidaciones, liquidar
from logic.modelos import Asistencia, Empleado


st.set_page_config(page_title="Liquidador UTEDYC", layout="wide")
st.title("Liquidador Domestico UTEDYC 183/92")
st.caption("Estimacion de liquidacion con base convenio + asistencia del periodo 20 al 20")

COEF_FERIADO_0229 = 2.0
COEF_ADICIONAL_0281 = 1.0
ALICUOTA_GANANCIAS = 0.0

meses = sorted(BASICOS.keys())
categorias = sorted(BASICOS[meses[-1]].keys())
feriados_periodo_mes = []
feriados_periodo_objetivo = []

col1, col2, col3 = st.columns(3)
with col1:
    mes = st.selectbox("Mes", meses, index=len(meses) - 1)
    feriados_periodo_mes = obtener_feriados_periodo_20_20(mes)
    comparar = st.checkbox("Comparar contra otro mes", value=False)
    mes_objetivo = None
    if comparar:
        mes_objetivo = st.selectbox("Mes objetivo", meses, index=max(0, len(meses) - 2))
        feriados_periodo_objetivo = obtener_feriados_periodo_20_20(mes_objetivo)
    categoria = st.selectbox("Categoria", categorias, index=categorias.index("D"))
    antiguedad = st.number_input("Anios de antiguedad", min_value=0, max_value=50, value=10)
with col2:
    titulo = st.checkbox("Titulo secundario", value=True)
    maquina = st.checkbox("Maquina contable", value=True)
    permanencia = st.checkbox("Permanencia categoria", value=True)
    quebranto = st.checkbox("Quebranto de caja (0218)", value=False)
    exigencia_operativa = st.checkbox("Exigencia operativa (0276)", value=False)
    refrigerio = st.checkbox("Refrigerio (0719)", value=False)
    st.caption("Descuento COD 0426 (cuota sindical): obligatorio")
with col3:
    st.caption(f"Feriados nacionales (periodo 20-20): {len(feriados_periodo_mes)}")
    feriados = st.number_input("Feriados trabajados", min_value=0, max_value=10, value=2)
    usar_valor_feriado_manual = st.checkbox("Usar valor feriado manual", value=False)
    valor_feriado_manual = None
    if usar_valor_feriado_manual:
        valor_feriado_manual = st.number_input(
            "Valor unitario feriado manual",
            min_value=0.0,
            max_value=500000.0,
            value=80000.0,
            step=1000.0,
        )
    nocturnos = st.number_input("Nocturnos", min_value=0, max_value=31, value=6)
    extras = st.number_input("Horas extras", min_value=0, max_value=200, value=0)

st.subheader("Conceptos fijos")
st.caption("0218, 0276 y 0719 se calculan automaticamente sobre la base categoria B del mes.")

with st.expander("Ver feriados del periodo 20-20"):
    st.write({"mes": mes, "feriados": feriados_periodo_mes})
    if comparar and mes_objetivo:
        st.write({"mes_objetivo": mes_objetivo, "feriados": feriados_periodo_objetivo})

if st.button("Calcular liquidacion", type="primary"):
    empleado = Empleado(
        categoria=categoria,
        antiguedad_anios=int(antiguedad),
        titulo_secundario=titulo,
        maquina_contable=maquina,
        quebranto_caja=quebranto,
        exigencia_operativa=exigencia_operativa,
        refrigerio=refrigerio,
        permanencia_categoria=permanencia,
        cuota_sindical=True,
    )
    asistencia = Asistencia(
        feriados_trabajados=int(feriados),
        nocturnos=int(nocturnos),
        horas_extras=int(extras),
    )
    if comparar and mes_objetivo:
        resultado = comparar_liquidaciones(
            empleado,
            asistencia,
            mes_base=mes,
            mes_objetivo=mes_objetivo,
            alicuota_ganancias=ALICUOTA_GANANCIAS,
            coef_feriado=COEF_FERIADO_0229,
            valor_feriado_manual=float(valor_feriado_manual) if valor_feriado_manual is not None else None,
            coef_adicional_feriado=COEF_ADICIONAL_0281,
        )
        st.subheader("Comparacion")
        st.json(resultado)
    else:
        resultado = liquidar(
            empleado,
            asistencia,
            mes,
            alicuota_ganancias=ALICUOTA_GANANCIAS,
            coef_feriado=COEF_FERIADO_0229,
            valor_feriado_manual=float(valor_feriado_manual) if valor_feriado_manual is not None else None,
            coef_adicional_feriado=COEF_ADICIONAL_0281,
        )
        st.subheader("Resultado")
        st.json(resultado)
