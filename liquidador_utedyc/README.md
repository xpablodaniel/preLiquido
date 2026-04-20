# Liquidador Domestico UTEDYC 183/92

Proyecto para estimar liquidaciones de sueldo segun convenio 183/92 usando:

- Basicos por categoria y mes.
- Adicionales porcentuales sobre categoria B.
- Adicionales variables por asistencia.
- Descuentos legales y sindicales.

## Uso por terminal

```bash
python main.py --mes 2026-03 --categoria D --antiguedad 10 --titulo --maquina --permanencia --sindical --feriados 2 --nocturnos 6 --extras 0
```

Con ajuste de formula de feriado o valor manual:

```bash
python main.py --mes 2026-01 --categoria D --antiguedad 10 --feriados 2 --coef-feriado 1.0
python main.py --mes 2026-01 --categoria D --antiguedad 10 --feriados 2 --valor-feriado-manual 80000
```

Comparar impacto entre dos meses (ejemplo: fin de temporada):

```bash
python main.py --comparar --mes 2026-03 --mes-objetivo 2026-04 --categoria D --antiguedad 10 --titulo --maquina --permanencia --sindical --feriados 2 --nocturnos 6 --extras 0
```

## Uso con Streamlit

```bash
streamlit run app.py
```

## Notas de calibracion

- El valor unitario de feriado se calcula por defecto como basico_categoria/25 y se actualiza automaticamente con aumentos del mes.
- El COD 0229 usa por defecto la formula legal sueldo_mensual/25, con un multiplicador opcional para calibracion.
- El COD 0281 se calcula por defecto como porcentaje del basico B del mes y se liquida una sola vez cuando hubo al menos un feriado trabajado en el periodo.
- Si necesitas fijar un valor puntual (por ejemplo, una planilla nueva), podes usar valor feriado manual en CLI o Streamlit.
- Los conceptos 0218 (quebranto), 0276 (exigencia operativa) y 0719 (refrigerio) se calculan automaticamente sobre la base categoria B del mes cuando estan activados para el empleado.
- La escala 2026-04 se deja como escala puente para medir el efecto del cambio de plus de temporada (20% a 12%).
