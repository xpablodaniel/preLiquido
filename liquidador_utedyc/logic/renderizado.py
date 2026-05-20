"""Funciones para renderizar recibos usando Jinja2 y exportar a PDF."""

import os
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape

from logic.presentacion import (
    clasificar_conceptos,
    generar_observaciones,
    generar_encabezado,
)


def obtener_directorio_templates() -> Path:
    """Retorna la ruta al directorio de templates."""
    base_dir = Path(__file__).parent.parent
    templates_dir = base_dir / "templates"
    if not templates_dir.exists():
        raise FileNotFoundError(f"No se encontró el directorio de templates: {templates_dir}")
    return templates_dir


def crear_ambiente_jinja() -> Environment:
    """Crea y configura el ambiente de Jinja2."""
    templates_dir = obtener_directorio_templates()
    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    
    # Agregar filtros personalizados
    env.filters["moneda"] = formato_moneda_jinja
    
    return env


def formato_moneda_jinja(valor: float) -> str:
    """Filtro Jinja2 para formatear moneda."""
    if valor < 0:
        return f"-$ {abs(valor):,.2f}".replace(",", ".")
    return f"$ {valor:,.2f}".replace(",", ".")


def renderizar_recibo_html(
    resultado: dict,
    resultado_anterior: dict | None = None,
    empleado_datos: dict | None = None,
) -> str:
    """Renderiza el recibo como HTML usando Jinja2.
    
    Args:
        resultado: Dict con la liquidación del mes actual
        resultado_anterior: Dict opcional con liquidación del mes anterior
        empleado_datos: Dict opcional con datos del empleado
    
    Returns:
        String con HTML renderizado
    """
    env = crear_ambiente_jinja()
    template = env.get_template("recibo.html")
    
    # Preparar contexto
    encabezado = generar_encabezado(resultado, empleado_datos)
    conceptos = clasificar_conceptos(resultado)
    observaciones = generar_observaciones(resultado, resultado_anterior)
    
    context = {
        "encabezado": encabezado,
        "conceptos": conceptos,
        "observaciones": observaciones,
    }
    
    return template.render(context)


def guardar_html(html_content: str, output_path: str | Path) -> Path:
    """Guarda el HTML a archivo.
    
    Args:
        html_content: String con contenido HTML
        output_path: Ruta donde guardar el archivo
    
    Returns:
        Path del archivo guardado
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(html_content, encoding="utf-8")
    return output_path


def generar_pdf_desde_html(html_content: str, output_path: str | Path) -> Path:
    """Genera PDF desde HTML usando WeasyPrint.
    
    Args:
        html_content: String con contenido HTML
        output_path: Ruta donde guardar el PDF
    
    Returns:
        Path del archivo PDF generado
    
    Raises:
        ImportError: Si WeasyPrint no está instalado
    """
    try:
        from weasyprint import HTML, CSS
    except ImportError:
        raise ImportError(
            "WeasyPrint no está instalado. Instálalo con: pip install weasyprint"
        )
    
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Generar PDF
    HTML(string=html_content).write_pdf(str(output_path))
    return output_path


def generar_recibo_completo(
    resultado: dict,
    formato: str = "html",
    output_path: str | Path | None = None,
    resultado_anterior: dict | None = None,
    empleado_datos: dict | None = None,
) -> str | Path:
    """Genera recibo en el formato especificado.
    
    Args:
        resultado: Dict con liquidación
        formato: "html" o "pdf"
        output_path: Ruta para guardar el archivo (si es None, retorna string)
        resultado_anterior: Dict opcional para comparaciones
        empleado_datos: Dict opcional con datos del empleado
    
    Returns:
        Si output_path es None: retorna string con contenido
        Si output_path es especificado: retorna Path del archivo generado
    """
    html_content = renderizar_recibo_html(resultado, resultado_anterior, empleado_datos)
    
    if output_path is None:
        if formato == "html":
            return html_content
        elif formato == "pdf":
            raise ValueError("Para generar PDF, debes especificar output_path")
    
    output_path = Path(output_path)
    
    if formato == "html":
        return guardar_html(html_content, output_path)
    elif formato == "pdf":
        # Primero guardar HTML temporal para facilitar debugging
        return generar_pdf_desde_html(html_content, output_path)
    else:
        raise ValueError(f"Formato no soportado: {formato}. Usa 'html' o 'pdf'")


def mostrar_resumen_consola(resultado: dict) -> None:
    """Muestra un resumen en consola con formato legible.
    
    Args:
        resultado: Dict con liquidación
    """
    from logic.presentacion import resumen_legible, generar_observaciones
    
    print(resumen_legible(resultado))
    print("\n📊 ANÁLISIS:")
    print(generar_observaciones(resultado))
    print("\n" + "="*50)
