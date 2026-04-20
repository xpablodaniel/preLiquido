# Proyecto Liquidador de Recibo de Sueldo

# 1\. Documentación del Proyecto: "Liquidador Doméstico UTEDYC"

Objetivo: Crear una herramienta de auditoría y proyección salarial personal para empleados bajo el Convenio 183/92.  
Alcance: Cálculo de haberes remunerativos, descuentos de ley y proyecciones de meses futuros basados en actas acuerdo.  
Diferenciador: Capacidad de comparar el impacto del fin de la temporada (Mar del Plata) entre Marzo y Abril.

# **🏗️ Estructura final del proyecto**

Tu idea está muy bien, solo la ajusto para que quede más limpia y mantenible:

liquidador\_utedyc/  
├── app.py                     \# Interfaz Streamlit  
├── main.py                    \# Ejecución por terminal (CLI)  
├── logic/  
│   ├── \_\_init\_\_.py  
│   ├── modelos.py             \# Clases: Empleado, MesConvenio, Asistencia, Liquidacion  
│   └── calculos.py            \# Funciones puras de cálculo  
├── data/  
│   ├── \_\_init\_\_.py  
│   ├── escalas.py             \# Básicos por categoría y mes  
│   ├── adicionales.py         \# Porcentajes del convenio  
│   └── feriados.py            \# Calendario de feriados nacionales  
├── docs/  
│   ├── convenio26.pdf  
│   └── manual\_usuario.md  
└── requirements.txt

# 

# **🎯 2\. Objetivo del Sistema**

El proyecto permite **prever el sueldo del próximo mes** antes de que RRHH liquide, utilizando:

* Asistencia del período **20 al 20**  
* Básicos vigentes según paritarias  
* Adicionales del convenio 183/92  
* Adicionales variables (feriados, nocturnos, extras)  
* Descuentos previsionales  
* Plus de temporada según mes  
* Particularidades de cada empleado (título, antigüedad, nocturnidad, etc.)

El sistema está diseñado para ser:

* **Modular**  
* **Escalable**  
* **Reutilizable por cualquier empleado del hotel**  
* **Fácil de extender a una API o base de datos**

# **🧩 3\. Componentes Principales**

## **3.1. Perfil del Empleado**

Define características fijas:

* Categoría  
* Antigüedad  
* Título secundario  
* Máquina contable  
* Quebranto de caja  
* Nocturnidad fija  
* Permanencia categoría (si antigüedad ≥ 5\)  
* Zona fría  
* Horario discontinuo  
* Idiomas  
* Cuota sindical

Ejemplo:

´Json´  
**{**  
  **"categoria": "D",**  
  **"antiguedad\_anios": 10,**  
  **"titulo\_secundario": true,**  
  **"maquina\_contable": true,**  
  **"quebranto\_caja": true,**  
  **"nocturnidad\_fija": true,**  
  **"permanencia\_categoria": true,**  
  **"zona\_fria": false,**  
  **"horario\_discontinuo": false,**  
  **"idiomas": false,**  
  **"cuota\_sindical": true**  
**}**

## **3.2. Parámetros del Mes (Convenio)**

Incluye:

* Básico por categoría según mes (Anexo A)  
* Básico categoría B (base para adicionales)  
* Plus de temporada (20% dic–mar / 12% abr)  
* Porcentajes del convenio:  
  * Puntualidad 15%  
  * Antigüedad 2% por año  
  * Título 10%  
  * Máquina 10%  
  * Permanencia 6%  
* Feriados nacionales del período

## **3.3. Asistencia del Período**

Datos variables:

* Feriados trabajados  
* Nocturnos  
* Horas extras  
* Días trabajados  
* Licencias  
* Franco trabajado

# 

# **🧮 4\. Lógica de Cálculo**

## **4.1. Básico del Mes**

Se obtiene desde `data/escalas.py`.

## **4.2. Adicionales Porcentuales (sobre básico B)**

Incluye:

* Puntualidad 15%  
* Antigüedad 2% × años  
* Título 10%  
* Máquina 10%  
* Permanencia 6%  
* Plus temporada 20% (dic–mar)

Ejemplo del convenio:

“Adicionales y Bonificaciones deben ser calculados/categoría B.”

## **4.3. Adicionales Variables**

Dependen de la asistencia:

* Feriados trabajados  
* Nocturnos  
* Horas extras

Ejemplo del recibo real:

* Nocturnos: 444.110,45  
* Feriados: 32.534,21

## **4.5. Descuentos**

Incluye:

* Jubilación 11%  
* Ley 19032 (3%)  
* Ley 23660 (3%)  
* Cuota sindical (si aplica)  
* Ganancias (si aplica)

Ejemplo del recibo:

* Jubilación: 379.556,82  
* Ley 19032: 103.515,50

# **🧱 5\. Archivos Principales**

## **5.1. `data/escalas.py`**

Contiene los básicos por categoría y mes.

## **5.2. `data/adicionales.py`**

Porcentajes del convenio.

## **5.3. `logic/modelos.py`**

Define:

* `Empleado`  
* `Asistencia`  
* `MesConvenio`

## **5.4. `logic/calculos.py`**

Implementa:

* Cálculo de básicos  
* Adicionales porcentuales  
* Adicionales variables  
* Descuentos  
* Liquidación completa

## **5.5. `main.py`**

Permite ejecutar la liquidación desde terminal.

## **5.6. `app.py`**

Interfaz web con Streamlit.

# **🌐 6\. Interfaz Web (Streamlit)**

La app permite:

* Seleccionar categoría  
* Ingresar antigüedad  
* Activar/desactivar adicionales  
* Cargar asistencia  
* Elegir mes  
* Ver resultado en JSON

# **📦 7\. Dependencias (`requirements.txt`)**

´Code´

**streamlit**

**pandas**

# **📝 8\. Notas Finales**

Este proyecto está diseñado para:

* Ser mantenible  
* Ser ampliable  
* Ser comprensible por cualquier compañero  
* Adaptarse a futuras paritarias sin reescribir lógica

# 

# **🧠 Filosofía del diseño**

### **✔ Separación total entre:**

* **Lógica de negocio** (cálculos)  
* **Modelos** (empleado, mes, asistencia)  
* **Datos del convenio**  
* **Interfaz** (CLI \+ Streamlit)

### **✔ Ventajas**

* Podés testear la lógica sin abrir Streamlit.  
* Podés agregar BD más adelante sin romper nada.  
* Podés agregar API Flask si querés.  
* Podés compartirlo con compañeros sin que toquen el código.

## 📦 1\. Archivo `data/escalas.py`

´Python´

**`# data/escalas.py`**

**`BASICOS = {`**  
    **`"2025-11": {"A1": 1155329, "A2": 1124158, "A2B": 1110538, "A3": 1104690,`**  
                **`"B": 1093560, "C": 1078800, "D": 1066846},`**  
    **`"2025-12": {"A1": 1177982, "A2": 1146201, "A2B": 1132314, "A3": 1126350,`**  
                **`"B": 1115003, "C": 1099953, "D": 1087764},`**  
    **`"2026-01": {"A1": 1200636, "A2": 1168243, "A2B": 1154089, "A3": 1148011,`**  
                **`"B": 1136445, "C": 1121106, "D": 1108683},`**  
    **`"2026-02": {"A1": 1223289, "A2": 1190285, "A2B": 1175864, "A3": 1169671,`**  
                **`"B": 1157887, "C": 1142259, "D": 1129601},`**  
    **`"2026-03": {"A1": 1245943, "A2": 1212328, "A2B": 1197639, "A3": 1191332,`**  
                **`"B": 1179330, "C": 1163412, "D": 1150520}`**  
**`}`**

## 📦 2\. Archivo data/[adicionales.py](http://adicionales.py)

´Python´

**\# data/adicionales.py**

**ADICIONALES \= {**  
    **"puntualidad": 0.15,**  
    **"antiguedad": 0.02,**  
    **"titulo\_secundario": 0.10,**  
    **"maquina\_contable": 0.10,**  
    **"permanencia\_categoria": 0.06,**  
    **"plus\_temporada\_20": 0.20,**  
    **"plus\_temporada\_12": 0.12**  
**}**

### 📦 3\. Archivo `logic/modelos.py`

´Python´

\# logic/modelos.py

**class Empleado:**  
    **def \_\_init\_\_(self, categoria, antiguedad, titulo, maquina, quebranto,**  
                 **nocturno, permanencia, zona\_fria, discontinuo, idiomas, sindical):**  
        **self.categoria \= categoria**  
        **self.antiguedad \= antiguedad**  
        **self.titulo \= titulo**  
        **self.maquina \= maquina**  
        **self.quebranto \= quebranto**  
        **self.nocturno \= nocturno**  
        **self.permanencia \= permanencia**  
        **self.zona\_fria \= zona\_fria**  
        **self.discontinuo \= discontinuo**  
        **self.idiomas \= idiomas**  
        **self.sindical \= sindical**

**class Asistencia:**  
    **def \_\_init\_\_(self, feriados, nocturnos, extras):**  
        **self.feriados \= feriados**  
        **self.nocturnos \= nocturnos**  
        **self.extras \= extras**

**class MesConvenio:**  
    **def \_\_init\_\_(self, mes):**  
        **self.mes \= mes  \# formato YYYY-MM**

## 

## 📦 4\. Archivo `logic/calculos.py`

´Python´

**\# logic/calculos.py**

**from data.escalas import BASICOS**  
**from data.adicionales import ADICIONALES**

**def obtener\_basico(categoria, mes):**  
    **return BASICOS\[mes\]\[categoria\]**

**def obtener\_basico\_B(mes):**  
    **return BASICOS\[mes\]\["B"\]**

**def calcular\_adicionales\_porcentuales(empleado, mes):**  
    **basico\_B \= obtener\_basico\_B(mes)**  
    **total \= 0**

    **total \+= basico\_B \* ADICIONALES\["puntualidad"\]**  
    **total \+= basico\_B \* (empleado.antiguedad \* ADICIONALES\["antiguedad"\])**

    **if empleado.titulo:**  
        **total \+= basico\_B \* ADICIONALES\["titulo\_secundario"\]**

    **if empleado.maquina:**  
        **total \+= basico\_B \* ADICIONALES\["maquina\_contable"\]**

    **if empleado.permanencia:**  
        **total \+= basico\_B \* ADICIONALES\["permanencia\_categoria"\]**

    **\# plus temporada**  
    **mes\_num \= int(mes.split("-")\[1\])**  
    **if mes\_num in \[12, 1, 2, 3\]:**  
        **total \+= basico\_B \* ADICIONALES\["plus\_temporada\_20"\]**

    **return total**

**def calcular\_adicionales\_variables(asistencia):**  
    **nocturnos\_valor \= 74018  \# ejemplo, se puede parametrizar**  
    **feriado\_valor \= 10844    \# ejemplo**  
    **extra\_valor \= 15000      \# ejemplo**

    **return (**  
        **asistencia.nocturnos \* nocturnos\_valor \+**  
        **asistencia.feriados \* feriado\_valor \+**  
        **asistencia.extras \* extra\_valor**  
    **)**

**def calcular\_descuentos(total\_rem):**  
    **jubilacion \= total\_rem \* 0.11**  
    **ley19032 \= total\_rem \* 0.03**  
    **ley23660 \= total\_rem \* 0.03**  
    **sindical \= total\_rem \* 0.03**

    **return jubilacion \+ ley19032 \+ ley23660 \+ sindical**

**def liquidar(empleado, asistencia, mes):**  
    **basico \= obtener\_basico(empleado.categoria, mes)**  
    **adicionales\_porc \= calcular\_adicionales\_porcentuales(empleado, mes)**  
    **adicionales\_var \= calcular\_adicionales\_variables(asistencia)**

    **total\_rem \= basico \+ adicionales\_porc \+ adicionales\_var**  
    **descuentos \= calcular\_descuentos(total\_rem)**

    **neto \= total\_rem \- descuentos**

    **return {**  
        **"basico": basico,**  
        **"adicionales\_porcentuales": adicionales\_porc,**  
        **"adicionales\_variables": adicionales\_var,**  
        **"total\_remunerativo": total\_rem,**  
        **"descuentos": descuentos,**  
        **"neto": neto**  
    **}**

## 

## 📦 5\. Archivo `main.py` (ejecución por terminal)

´Python´

**\# main.py**

**from logic.modelos import Empleado, Asistencia**  
**from logic.calculos import liquidar**

**empleado \= Empleado(**  
    **categoria="D",**  
    **antiguedad=10,**  
    **titulo=True,**  
    **maquina=True,**  
    **quebranto=True,**  
    **nocturno=True,**  
    **permanencia=True,**  
    **zona\_fria=False,**  
    **discontinuo=False,**  
    **idiomas=False,**  
    **sindical=True**  
**)**

**asistencia \= Asistencia(**  
    **feriados=2,**  
    **nocturnos=6,**  
    **extras=0**  
**)**

**resultado \= liquidar(empleado, asistencia, "2026-03")**

**print(resultado)**

## 📦 6\. Archivo `app.py` (Streamlit)

´Python´

**\# app.py**

**import streamlit as st**  
**from logic.modelos import Empleado, Asistencia**  
**from logic.calculos import liquidar**

**st.title("Liquidador UTEDYC 183/92")**

**categoria \= st.selectbox("Categoría", \["A1","A2","A2B","A3","B","C","D"\])**  
**antiguedad \= st.number\_input("Años de antigüedad", 0, 40, 10\)**  
**titulo \= st.checkbox("Título secundario")**  
**maquina \= st.checkbox("Máquina contable")**  
**permanencia \= antiguedad \>= 5**

**feriados \= st.number\_input("Feriados trabajados", 0, 10, 2\)**  
**nocturnos \= st.number\_input("Nocturnos", 0, 10, 6\)**  
**extras \= st.number\_input("Horas extras", 0, 100, 0\)**

**mes \= st.selectbox("Mes", \["2025-11","2025-12","2026-01","2026-02","2026-03"\])**

**if st.button("Calcular"):**  
    **empleado \= Empleado(categoria, antiguedad, titulo, maquina, True, True, permanencia, False, False, False, True)**  
    **asistencia \= Asistencia(feriados, nocturnos, extras)**  
    **resultado \= liquidar(empleado, asistencia, mes)**  
    **st.json(resultado)**

