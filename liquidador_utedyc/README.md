# Liquidador UTEDYC 183/92

Aplicación de apoyo para estimar la próxima liquidación de sueldo bajo el convenio UTEDYC 183/92.

El objetivo del proyecto es acercar una liquidación probable a partir de:

- básicos por categoría y período,
- adicionales convencionales,
- novedades del período 20-20,
- descuentos legales obligatorios,
- comparación entre distintos meses,
- contraste posterior contra recibos reales para medir precisión.

No pretende reemplazar la liquidación oficial del empleador ni el asesoramiento profesional. La intención es ofrecer una herramienta práctica de control, simulación y auditoría personal.

## Alcance actual

El proyecto ya contempla:

- cálculo por categoría y mes,
- adicionales porcentuales sobre categoría B,
- cálculo dinámico de feriados trabajados,
- cálculo dinámico de horas extras,
- cálculo de franco trabajado,
- adicionales fijos y condiciones particulares,
- descuento sindical obligatorio según criterio actual del proyecto,
- simulación desde CLI,
- simulación desde interfaz Streamlit,
- base preparada para calibrar contra recibos reales,
- **resumen legible en consola con formato amigable**,
- **generación de recibos HTML profesionales**,
- **exportación a PDF** (con WeasyPrint),
- **análisis automático de variaciones**.

## Funcionalidades de Presentación

### Resumen Legible en Consola

Transforma los datos JSON técnicos en un formato legible y amigable:

```
==================================================
LIQUIDACIÓN DE SUELDO - 2026-05 / CATEGORÍA D
==================================================

DETALLE DE REMUNERACIONES:
--------------------------------------------------
Sueldo básico:                      $ 1.150.520
Adicionales % (antiguedad, puntualidad, etc):    $ 719.391
Variables (nocturnos, feriados, extras):         $ 552.329
...
```

### Recibo HTML/PDF

Genera recibos profesionales que respetan la estructura tradicional de recibos de sueldo con:

- Encabezado con datos del empleado y período
- Tabla de conceptos remunerativos agrupados
- Tabla de descuentos
- Totales formateados
- Análisis automático de variaciones
- Diseño responsive (imprime bien en A4)

### Análisis Automático

Detecta automáticamente:

- Variaciones significativas vs. mes anterior
- Presencia de plus de temporada
- Peso de nocturnidad
- Feriados trabajados
- Composición de descuentos

## Uso

### Interfaz Streamlit (Recomendada)

```bash
streamlit run app.py
```

Ofrece:
1. **Tab "Resumen Amigable"** - Visualización de datos formateada
2. **Tab "Recibo Formal"** - Preview HTML + botones de descarga
3. **Tab "Datos JSON"** - Datos crudos para análisis avanzado

### Línea de Comandos

#### Resumen legible:
```bash
python main.py --mes 2026-05 --categoria D --antiguedad 10 \
  --titulo --maquina --permanencia --nocturnos 6 \
  --formato resumen
```

#### Generar HTML:
```bash
python main.py --mes 2026-05 --categoria D --antiguedad 10 \
  --titulo --maquina --permanencia --nocturnos 6 \
  --formato html --output recibo_mayo.html \
  --nombre "Juan Perez" --cuil "20-12345678-9"
```

#### Generar PDF:
```bash
python main.py --mes 2026-05 --categoria D --antiguedad 10 \
  --titulo --maquina --permanencia --nocturnos 6 \
  --formato pdf --output recibo_mayo.pdf \
  --nombre "Juan Perez" --cuil "20-12345678-9"
```

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Si deseas usar la funcionalidad de PDF, asegúrate de tener WeasyPrint instalado:

```bash
pip install weasyprint
```

En sistemas Linux/Mac, WeasyPrint requiere librerías gráficas adicionales. Ver: https://weasyprint.org/

## Objetivo de evolución

La idea de fondo es que cada trabajador pueda cargar su situación particular y comparar el resultado de la app con su recibo real. Con suficientes casos validados, el proyecto puede evolucionar hacia:

- un registro local de participantes,
- simulación masiva por mes,
- medición de desvíos por concepto,
- mejora progresiva de fórmulas y parámetros,
- reportes de precisión por persona y por período.

## Privacidad y datos sensibles

Este repositorio público o remoto no debe incluir datos personales reales, recibos, imágenes, planillas ni legajos.

La estrategia del proyecto es separar:

- código y documentación aptos para publicar,
- datos locales privados para pruebas y calibración,
- recibos e imágenes fuera del flujo Git.

Los datos privados de participantes pueden mantenerse en una carpeta local ignorada por Git para evitar publicación accidental.

## Uso por terminal

Ejemplo de liquidación simple:

```bash
python3 main.py --mes 2026-03 --categoria D --antiguedad 10 --titulo --maquina --permanencia --feriados 2 --nocturnos 6 --extras 0
```

Ejemplo con valor manual de feriado:

```bash
python3 main.py --mes 2026-01 --categoria D --antiguedad 10 --feriados 2 --valor-feriado-manual 80000
```

Ejemplo de comparación entre meses:

```bash
python3 main.py --comparar --mes 2026-03 --mes-objetivo 2026-04 --categoria D --antiguedad 10 --titulo --maquina --permanencia --feriados 2 --nocturnos 6 --extras 0
```

## Uso con Streamlit

Desde la carpeta del proyecto:

```bash
python3 -m streamlit run app.py
```

## Criterios de cálculo relevantes

- El valor del feriado trabajado se calcula sobre el básico de la categoría del mes.
- El COD 0229 usa un multiplicador interno fijo de 2.0 sobre la fórmula sueldo mensual / 25.
- El franco trabajado se calcula como 2 veces el valor unitario del feriado.
- La hora extra se calcula dinámicamente a partir del básico de categoría del mes.
- El COD 0281 se arrastra desde una base de referencia sobre categoría B.
- El COD 0426 se considera obligatorio en esta versión.
- La alícuota de ganancias queda fijada en 0.0 para esta etapa del proyecto.
- Algunos conceptos pueden seguir requiriendo calibración con recibos reales, especialmente aquellos que no deriven linealmente del básico.

## Estructura del proyecto

- `data/`: escalas, adicionales y feriados.
- `logic/`: modelos y motor de cálculo.
- `tests/`: pruebas automáticas de regresión.
- `app.py`: interfaz Streamlit.
- `main.py`: entrada por línea de comandos.

## Estado del proyecto

Proyecto en evolución activa.

La prioridad actual es mejorar la precisión usando casos reales locales, pero sin publicar información sensible en el repositorio remoto.
