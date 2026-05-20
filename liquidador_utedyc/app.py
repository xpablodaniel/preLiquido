"""Streamlit app for salary projection."""

import html
import io
import streamlit as st
import streamlit.components.v1 as components

from data.escalas import BASICOS
from data.feriados import obtener_feriados_periodo_20_20
from logic.calculos import comparar_liquidaciones, liquidar
from logic.modelos import Asistencia, Empleado
from logic.presentacion import resumen_legible, generar_observaciones
from logic.renderizado import renderizar_recibo_html, generar_pdf_desde_html


def _render_resumen_html(resumen_texto: str, observaciones_texto: str) -> str:
        resumen_safe = html.escape(resumen_texto)
        observaciones_safe = html.escape(observaciones_texto).replace("\n", "<br>")
        return f"""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8" />
            <style>
                :root {{
                    color-scheme: light;
                }}
                body {{
                    margin: 0;
                    padding: 14px;
                    font-family: Arial, sans-serif;
                    background: #ffffff;
                    color: #111827;
                }}
                .card {{
                    border: 1px solid #dbe3ef;
                    border-radius: 10px;
                    padding: 12px;
                    background: #f8fafc;
                }}
                .title {{
                    margin: 0 0 8px 0;
                    font-size: 13px;
                    font-weight: 700;
                }}
                pre {{
                    margin: 0;
                    white-space: pre-wrap;
                    word-break: break-word;
                    font-family: Consolas, "DejaVu Sans Mono", Menlo, monospace;
                    font-size: 12px;
                    line-height: 1.42;
                    color: #1f2937;
                }}
                .obs {{
                    margin-top: 10px;
                    border-left: 3px solid #3b82f6;
                    background: #eff6ff;
                    padding: 8px 10px;
                    font-size: 12px;
                    line-height: 1.4;
                }}
                .obs b {{
                    font-size: 12px;
                }}
            </style>
        </head>
        <body>
            <div class="card">
                <p class="title">Resumen amigable</p>
                <pre>{resumen_safe}</pre>
            </div>
            <div class="obs"><b>Analisis y Observaciones:</b><br>{observaciones_safe}</div>
        </body>
        </html>
        """


st.set_page_config(page_title="Liquidador UTEDYC", layout="wide")
st.title("Liquidador Domestico UTEDYC 183/92")
st.caption("Estimacion de liquidacion con base convenio + asistencia del periodo 20 al 20")

# Inicializar session_state
if "resultado" not in st.session_state:
    st.session_state.resultado = None
if "nombre_empleado" not in st.session_state:
    st.session_state.nombre_empleado = ""
if "cuil_empleado" not in st.session_state:
    st.session_state.cuil_empleado = ""
if "lugar_trabajo" not in st.session_state:
    st.session_state.lugar_trabajo = "HOTEL 23 DE MAYO"

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
        st.session_state.resultado = comparar_liquidaciones(
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
        st.json(st.session_state.resultado)
    else:
        st.session_state.resultado = liquidar(
            empleado,
            asistencia,
            mes,
            alicuota_ganancias=ALICUOTA_GANANCIAS,
            coef_feriado=COEF_FERIADO_0229,
            valor_feriado_manual=float(valor_feriado_manual) if valor_feriado_manual is not None else None,
            coef_adicional_feriado=COEF_ADICIONAL_0281,
        )

# Mostrar tabs si hay resultado guardado
if st.session_state.resultado is not None:
    resultado = st.session_state.resultado
    
    # Tabs para diferentes vistas
    tab_resumen, tab_recibo, tab_json = st.tabs(["📋 Resumen Amigable", "🧾 Recibo Formal", "📊 Datos JSON"])
    
    with tab_resumen:
        resumen_texto = resumen_legible(resultado)
        observaciones_texto = generar_observaciones(resultado)
        resumen_html = _render_resumen_html(resumen_texto, observaciones_texto)
        components.html(resumen_html, height=560, scrolling=True)
    
    with tab_recibo:
        # Opciones de empleado
        col_emp1, col_emp2 = st.columns(2)
        with col_emp1:
            nombre_empleado = st.text_input(
                "Nombre (opcional)",
                value=st.session_state.nombre_empleado,
                key="nombre_input",
            )
            st.session_state.nombre_empleado = nombre_empleado

        with col_emp2:
            cuil_empleado = st.text_input(
                "C.U.I.L. (opcional)",
                value=st.session_state.cuil_empleado,
                key="cuil_input",
            )
            st.session_state.cuil_empleado = cuil_empleado

        lugar_trabajo = st.text_input(
            "Lugar de trabajo (opcional)",
            value=st.session_state.lugar_trabajo,
            key="lugar_input",
        )
        st.session_state.lugar_trabajo = lugar_trabajo

        empleado_datos = {
            "nombre": nombre_empleado,
            "cuil": cuil_empleado,
            "lugar_trabajo": lugar_trabajo,
        }

        # Generar HTML del recibo
        html_recibo = renderizar_recibo_html(resultado, empleado_datos=empleado_datos)

        # Mostrar preview
        st.markdown("#### Vista Previa del Recibo")
        components.html(html_recibo, height=800, scrolling=True)

        # Botones de descarga
        col_down1, col_down2 = st.columns(2)

        with col_down1:
            st.download_button(
                label="⬇️ Descargar como HTML",
                data=html_recibo,
                file_name=f"recibo_{resultado.get('mes', 'liquidacion')}.html",
                mime="text/html",
            )

        with col_down2:
            try:
                # Generar PDF en memoria
                pdf_bytes = io.BytesIO()
                from weasyprint import HTML

                HTML(string=html_recibo).write_pdf(pdf_bytes)
                pdf_bytes.seek(0)

                st.download_button(
                    label="⬇️ Descargar como PDF",
                    data=pdf_bytes,
                    file_name=f"recibo_{resultado.get('mes', 'liquidacion')}.pdf",
                    mime="application/pdf",
                )
            except ImportError:
                st.warning("⚠️ WeasyPrint no está instalado. No puedes descargar PDF.")
                st.info("Instálalo con: `pip install weasyprint`")

    with tab_json:
        st.json(resultado)
