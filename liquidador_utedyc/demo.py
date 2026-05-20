"""Script de demostración de las nuevas funcionalidades."""

import json
from pathlib import Path

from logic.calculos import liquidar
from logic.modelos import Asistencia, Empleado
from logic.presentacion import (
    resumen_legible,
    generar_observaciones,
    clasificar_conceptos,
    generar_encabezado,
)
from logic.renderizado import renderizar_recibo_html, guardar_html


def demo_presentacion():
    """Demuestra las funcionalidades de presentación."""
    print("=" * 70)
    print("DEMO - LIQUIDADOR UTEDYC 183/92 - NUEVAS FUNCIONALIDADES")
    print("=" * 70)
    
    # Crear datos de ejemplo
    empleado = Empleado(
        categoria="D",
        antiguedad_anios=10,
        titulo_secundario=True,
        maquina_contable=True,
        permanencia_categoria=True,
        cuota_sindical=True,
    )
    
    asistencia = Asistencia(
        feriados_trabajados=2,
        nocturnos=6,
        horas_extras=0,
    )
    
    # Calcular liquidación
    resultado = liquidar(
        empleado,
        asistencia,
        mes="2026-05",
        coef_feriado=2.0,
        coef_adicional_feriado=1.0,
    )
    
    # 1. DEMOSTRACIÓN: RESUMEN LEGIBLE
    print("\n" + "=" * 70)
    print("1. RESUMEN LEGIBLE EN CONSOLA")
    print("=" * 70)
    print(resumen_legible(resultado))
    
    # 2. DEMOSTRACIÓN: ANÁLISIS AUTOMÁTICO
    print("\n" + "=" * 70)
    print("2. ANÁLISIS AUTOMÁTICO DE VARIACIONES")
    print("=" * 70)
    print(generar_observaciones(resultado))
    
    # 3. DEMOSTRACIÓN: CLASIFICACIÓN DE CONCEPTOS
    print("\n" + "=" * 70)
    print("3. CLASIFICACIÓN DE CONCEPTOS")
    print("=" * 70)
    conceptos = clasificar_conceptos(resultado)
    print(f"✓ Conceptos básicos: {len(conceptos['basicos'])} items")
    print(f"✓ Adicionales porcentuales: {len(conceptos['porcentuales'])} items")
    print(f"✓ Adicionales variables: {len(conceptos['variables'])} items")
    print(f"✓ Adicionales fijos: {len(conceptos['fijos'])} items")
    print(f"✓ Descuentos: {len(conceptos['descuentos'])} items")
    print(f"✓ Totales: {conceptos['totales']}")
    
    # 4. DEMOSTRACIÓN: GENERACIÓN DE ENCABEZADO
    print("\n" + "=" * 70)
    print("4. GENERACIÓN DE ENCABEZADO")
    print("=" * 70)
    empleado_datos = {
        "nombre": "Juan Pérez",
        "cuil": "20-12345678-9",
        "lugar_trabajo": "HOTEL 23 DE MAYO",
    }
    encabezado = generar_encabezado(resultado, empleado_datos)
    print(json.dumps(encabezado, indent=2, ensure_ascii=False))
    
    # 5. DEMOSTRACIÓN: RENDERIZADO HTML
    print("\n" + "=" * 70)
    print("5. GENERACIÓN DE RECIBO HTML")
    print("=" * 70)
    html_recibo = renderizar_recibo_html(resultado, empleado_datos=empleado_datos)
    print(f"✓ HTML generado: {len(html_recibo)} caracteres")
    
    # Guardar HTML
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    html_path = guardar_html(html_recibo, output_dir / "recibo_demo.html")
    print(f"✓ Guardado en: {html_path}")
    
    # 6. DEMOSTRACIÓN: EXPORTACIÓN A PDF (si está disponible)
    print("\n" + "=" * 70)
    print("6. GENERACIÓN DE PDF")
    print("=" * 70)
    try:
        from logic.renderizado import generar_pdf_desde_html
        
        pdf_path = generar_pdf_desde_html(html_recibo, output_dir / "recibo_demo.pdf")
        print(f"✓ PDF generado: {pdf_path}")
    except ImportError:
        print("⚠️ WeasyPrint no está instalado.")
        print("   Instálalo con: pip install weasyprint")
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETADA")
    print("=" * 70)
    print(f"\n✓ Archivos generados en: {output_dir.absolute()}")


if __name__ == "__main__":
    demo_presentacion()
