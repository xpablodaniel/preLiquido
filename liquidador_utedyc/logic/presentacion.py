"""Funciones para formateo y presentación de datos de liquidación."""

from datetime import datetime
from typing import Any


def formato_moneda(valor: float, simbolo: str = "$") -> str:
    """Formatea un valor numérico como moneda con separador de miles.
    
    Args:
        valor: Valor numérico a formatear
        simbolo: Símbolo de moneda (default: $)
    
    Returns:
        String con formato: "$ 1.234.567" (Argentina)
    """
    if valor < 0:
        return f"-{simbolo} {abs(valor):,.0f}".replace(",", ".")
    return f"{simbolo} {valor:,.0f}".replace(",", ".")


def resumen_legible(resultado: dict) -> str:
    """Genera un resumen legible de la liquidación.
    
    Transforma la salida JSON técnica en un formato amigable para lectura.
    
    Args:
        resultado: Dict con estructura de liquidación (contiene items_cod, descuentos, neto_estimado)
    
    Returns:
        String formateado para presentación en consola o UI
    """
    mes = resultado.get("mes", "N/A")
    categoria = resultado.get("categoria", "N/A")
    
    total_remunerativo = resultado.get("total_remunerativo", 0)
    descuentos_total = resultado.get("descuentos", {}).get("total", 0)
    neto = resultado.get("neto_estimado", 0)
    
    linea = "-" * 50
    
    resumen = f"""
{'='*50}
LIQUIDACIÓN DE SUELDO - {mes} / CATEGORÍA {categoria}
{'='*50}

DETALLE DE REMUNERACIONES:
{linea}
"""
    
    # Agrupar remunerativos por categoría
    items_cod = resultado.get("items_cod", {})
    remunerativos = items_cod.get("remunerativos", [])
    
    # Agrupar por tipo
    basico = sum(i["importe"] for i in remunerativos if i["cod"] == "0201")
    porcentuales = sum(i["importe"] for i in remunerativos 
                      if i["cod"] in ["0214", "0216", "0218", "0273", "0274", "0720"])
    variables = sum(i["importe"] for i in remunerativos 
                   if i["cod"] in ["0229", "0281", "0283", "0231", "0232"])
    fijos = sum(i["importe"] for i in remunerativos 
               if i["cod"] in ["0276", "0719", "0280", "0285"])
    
    resumen += f"Sueldo básico:              {formato_moneda(basico):>15}\n"
    if porcentuales > 0:
        resumen += f"Adicionales % (antiguedad, puntualidad, etc): {formato_moneda(porcentuales):>15}\n"
    if variables > 0:
        resumen += f"Variables (nocturnos, feriados, extras):     {formato_moneda(variables):>15}\n"
    if fijos > 0:
        resumen += f"Adicionales fijos (refrigerio, etc):         {formato_moneda(fijos):>15}\n"
    
    resumen += f"\n{'='*50}\n"
    resumen += f"TOTAL REMUNERATIVO:         {formato_moneda(total_remunerativo):>15}\n"
    
    resumen += f"\n{'DESCUENTOS':<35} {'IMPORTE':>14}\n"
    resumen += linea + "\n"
    
    descuentos = resultado.get("descuentos", {})
    for concepto, valor in descuentos.items():
        if concepto != "total" and valor > 0:
            label = _etiqueta_descuento(concepto)
            resumen += f"{label:<35} {formato_moneda(valor):>15}\n"
    
    resumen += linea + "\n"
    resumen += f"{'TOTAL DESCUENTOS':<35} {formato_moneda(descuentos_total):>15}\n"
    
    resumen += f"\n{'='*50}\n"
    resumen += f"{'NETO A PERCIBIR':<35} {formato_moneda(neto):>15}\n"
    resumen += f"{'='*50}\n"
    
    # Alertas si existen
    alertas = resultado.get("alertas", [])
    if alertas:
        resumen += f"\n⚠️ ALERTAS:\n"
        for alerta in alertas:
            resumen += f"  • {alerta}\n"
    
    return resumen


def clasificar_conceptos(resultado: dict) -> dict:
    """Agrupa conceptos por tipo y categoría para presentación en PDF/HTML.
    
    Args:
        resultado: Dict con estructura de liquidación
    
    Returns:
        Dict con claves: remunerativos, variables, fijos, descuentos, totales
    """
    items_cod = resultado.get("items_cod", {})
    remunerativos = items_cod.get("remunerativos", [])
    descuentos = items_cod.get("descuentos", [])
    
    clasificados = {
        "basicos": [],
        "porcentuales": [],
        "variables": [],
        "fijos": [],
        "descuentos": [],
        "totales": {
            "total_remunerativo": resultado.get("total_remunerativo", 0),
            "total_descuentos": resultado.get("descuentos", {}).get("total", 0),
            "neto_estimado": resultado.get("neto_estimado", 0),
        }
    }
    
    # Clasificar remunerativos
    for item in remunerativos:
        cod = item["cod"]
        if cod == "0201":
            clasificados["basicos"].append(item)
        elif cod in ["0214", "0216", "0218", "0273", "0274", "0720", "0227"]:
            clasificados["porcentuales"].append(item)
        elif cod in ["0229", "0281", "0283", "0231", "0232"]:
            clasificados["variables"].append(item)
        elif cod in ["0276", "0719", "0280", "0285"]:
            clasificados["fijos"].append(item)
    
    # Copiar descuentos
    clasificados["descuentos"] = descuentos
    
    return clasificados


def generar_observaciones(resultado: dict, resultado_anterior: dict | None = None) -> str:
    """Genera observaciones automáticas sobre variaciones y factores relevantes.
    
    Args:
        resultado: Dict con liquidación del mes actual
        resultado_anterior: Dict con liquidación del mes anterior (opcional)
    
    Returns:
        String con observaciones en lenguaje natural
    """
    observaciones = []
    
    # Analizar variaciones
    if resultado_anterior:
        neto_actual = resultado.get("neto_estimado", 0)
        neto_anterior = resultado_anterior.get("neto_estimado", 0)
        variacion = neto_actual - neto_anterior
        pct_variacion = (variacion / neto_anterior * 100) if neto_anterior else 0
        
        if variacion < -100000:
            observaciones.append(
                f"⚠️ El neto es {abs(variacion):,.0f} menor al mes anterior ({pct_variacion:.1f}%)"
            )
        elif variacion > 100000:
            observaciones.append(
                f"✓ El neto es {variacion:,.0f} mayor al mes anterior ({pct_variacion:.1f}%)"
            )
    
    # Analizar plus de temporada
    items_cod = resultado.get("items_cod", {})
    remunerativos = items_cod.get("remunerativos", [])
    plus_temporada = next((i["importe"] for i in remunerativos if i["cod"] == "0227"), 0)
    if plus_temporada == 0:
        observaciones.append("ℹ️ Sin plus de temporada este mes")
    else:
        observaciones.append(f"✓ Plus de temporada: {formato_moneda(plus_temporada)}")
    
    # Analizar nocturnidad
    nocturnos = next((i["importe"] for i in remunerativos if i["cod"] == "0283"), 0)
    if nocturnos > 0:
        pct_nocturnos = (nocturnos / resultado.get("total_remunerativo", 1)) * 100
        if pct_nocturnos > 15:
            observaciones.append(
                f"⚠️ Nocturnidad significativa: {pct_nocturnos:.1f}% del remunerativo"
            )
    
    # Analizar feriados trabajados
    feriados_total = sum(i["importe"] for i in remunerativos 
                        if i["cod"] in ["0229", "0281"])
    if feriados_total > 0:
        observaciones.append(f"✓ Feriados trabajados incluidos: {formato_moneda(feriados_total)}")
    
    # Analizar descuentos
    descuentos = resultado.get("descuentos", {})
    if descuentos.get("total", 0) > 0:
        pct_descuentos = (descuentos["total"] / resultado.get("total_remunerativo", 1)) * 100
        observaciones.append(f"📊 Descuentos totales: {pct_descuentos:.1f}% del remunerativo")
    
    return "\n".join(observaciones) if observaciones else "Sin observaciones relevantes."


def _etiqueta_descuento(cod_concepto: str) -> str:
    """Retorna etiqueta legible para un concepto de descuento."""
    mapa = {
        "jubilacion": "Jubilación (AFP/SPP)",
        "ley_19032": "Seguro Ley 19.032",
        "ley_23660": "Obra social Ley 23.660",
        "cuota_sindical": "Cuota sindical",
        "ganancias": "Retención de ganancias",
    }
    return mapa.get(cod_concepto, cod_concepto.replace("_", " ").title())


def generar_encabezado(resultado: dict, empleado_datos: dict | None = None) -> dict:
    """Genera información de encabezado para PDF/HTML.
    
    Args:
        resultado: Dict con liquidación
        empleado_datos: Dict opcional con datos del empleado (nombre, C.U.I.L., etc)
    
    Returns:
        Dict con info de encabezado formateada
    """
    mes_str = resultado.get("mes", "")
    mes_obj = datetime.strptime(mes_str, "%Y-%m") if mes_str else None
    
    encabezado = {
        "mes": mes_str,
        "mes_legible": mes_obj.strftime("%B %Y") if mes_obj else mes_str,
        "categoria": resultado.get("categoria", "N/A"),
        "empleado": empleado_datos or {},
        "fecha_generacion": datetime.now().strftime("%d/%m/%Y"),
    }
    
    if empleado_datos:
        encabezado["nombre"] = empleado_datos.get("nombre", "")
        encabezado["cuil"] = empleado_datos.get("cuil", "")
        encabezado["lugar_trabajo"] = empleado_datos.get("lugar_trabajo", "")
    
    return encabezado
