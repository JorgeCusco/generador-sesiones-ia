# main.py
import google.generativeai as genai
from docxtpl import DocxTemplate
import json
import os
import argparse
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# Importamos nuestras propias funciones y variables desde los otros archivos
from config import DATOS_FIJOS, load_api_key
from prompts import get_planificador_prompt, get_redactor_prompt, get_profesion_prompt

def solicitar_a_ia(model, prompt_text, return_json=True):
    """Función centralizada para hacer llamadas a la API de Gemini."""
    try:
        response = model.generate_content(prompt_text)
        if not return_json:
            return response.text.strip()
        
        cleaned_json = response.text.replace('```json', '').replace('```', '').strip()
        return json.loads(cleaned_json)
    except Exception as e:
        print(f"❌ Error crítico durante la llamada a la IA: {e}")
        print(f"Respuesta recibida (si la hubo):\n{response.text if 'response' in locals() else 'No response'}")
        return None

def formatar_lista_con_vinetas(lista_items):
    """Convierte una lista en una cadena de texto con viñetas."""
    if not isinstance(lista_items, list):
        return lista_items
    return "\n".join([f"• {item}" for item in lista_items])

def run(prompt_del_usuario):
    """Función principal que orquesta todo el proceso."""
    try:
        api_key = load_api_key()
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-pro-latest')
    except ValueError as e:
        print(e)
        return

    # --- PRE-FASE: INFERENCIA DE PROFESIÓN ---
    print("🧠 Infiriendo la profesión del usuario...")
    profesion_prompt = get_profesion_prompt(prompt_del_usuario)
    profesion_inferida = solicitar_a_ia(model, profesion_prompt, return_json=False) or "profesional"
    print(f"✅ Profesión inferida: {profesion_inferida}")

    # --- FASE 1: PLANIFICACIÓN ---
    print("🤖 Fase 1: La IA está planificando la sesión...")
    prompt_fase1 = get_planificador_prompt(prompt_del_usuario, profesion_inferida)
    plan_de_sesion = solicitar_a_ia(model, prompt_fase1)
    if not plan_de_sesion:
        return

    print(f"✅ Planificación completada. Tema: '{plan_de_sesion.get('tema_central', 'N/A')}'")
    
    # --- FASE 2: REDACCIÓN ---
    print("🤖 Fase 2: La IA está redactando el contenido pedagógico...")
    competencia_info = DATOS_FIJOS["competencias"].get(plan_de_sesion.get("competencia_seleccionada", "Gestion_Proyectos"))
    
    duracion_total = int(plan_de_sesion.get('duracion') or 90)
    
    tiempos = {
        'inicio': int(duracion_total * 0.15),
        'cierre': int(duracion_total * 0.15),
        'desarrollo': duracion_total - int(duracion_total * 0.15) * 2
    }
    prompt_fase2 = get_redactor_prompt(plan_de_sesion, competencia_info, tiempos)
    contenido_redactado = solicitar_a_ia(model, prompt_fase2)
    if not contenido_redactado:
        return

    print("✅ Contenido pedagógico redactado.")

    # --- FASE 3: ENSAMBLAJE Y VALORES POR DEFECTO ---
    print("📄 Ensamblando el documento de Word final...")
    doc = DocxTemplate("plantilla_sesion.docx")
    
    campos_por_defecto_usados = []
    def get_valor(clave, valor_defecto):
        valor = plan_de_sesion.get(clave)
        if not valor:
            campos_por_defecto_usados.append(clave)
            return valor_defecto
        return valor

    ejes_seleccionados = plan_de_sesion.get('ejes_seleccionados', [])
    enfoque1_eje = ejes_seleccionados[0] if len(ejes_seleccionados) > 0 else None
    enfoque2_eje = ejes_seleccionados[1] if len(ejes_seleccionados) > 1 else None
    enfoque1 = DATOS_FIJOS['ejes'].get(enfoque1_eje, {})
    enfoque2 = DATOS_FIJOS['ejes'].get(enfoque2_eje, {})

    contexto_final = {
        'titulo': contenido_redactado.get('titulo', ''),
        'numero_unidad': get_valor('numero_unidad', '1'),
        'numero_sesion': get_valor('numero_sesion', '1'),
        'nivel_academico': get_valor('nivel_academico', 'Postgrado'),
        'semestre': get_valor('semestre', '6'),
        'docente': get_valor('docente', 'Mgt. Jorge Dueñas'),
        'institucion_educativa': get_valor('institucion_educativa', 'Universidad de San Antonio Abad del Cusco'),
        'area': get_valor('area', 'Maestría en Infraestructura Inteligente y Automatización de Procesos'),
        'tiempo': f"{duracion_total} minutos",
        'fecha': get_valor('fecha', datetime.now().strftime("%d/%m/%Y")),
        
        'competencia': competencia_info.get('texto', ''),
        'capacidades': competencia_info.get('capacidades', ''),
        'desempenos': formatar_lista_con_vinetas(contenido_redactado.get('desempenos', [])),
        'evidencia': contenido_redactado.get('evidencia', ''),
        
        'eje_1': enfoque1_eje or '',
        'valores_1': enfoque1.get('valor', ''),
        'actitudes_1': enfoque1.get('actitud', ''),
        'eje_2': enfoque2_eje or '',
        'valores_2': enfoque2.get('valor', ''),
        'actitudes_2': enfoque2.get('actitud', ''),
        
        'preparacion': formatar_lista_con_vinetas(contenido_redactado.get('preparacion', [])),
        
        'tiempo_inicio': f"{tiempos['inicio']} min",
        'actividades_inicio': formatar_lista_con_vinetas(contenido_redactado.get('actividades_inicio', [])),
        'tiempo_desarrollo': f"{tiempos['desarrollo']} min",
        'actividades_desarrollo': formatar_lista_con_vinetas(contenido_redactado.get('actividades_desarrollo', [])),
        'tiempo_cierre': f"{tiempos['cierre']} min",
        'actividades_cierre': formatar_lista_con_vinetas(contenido_redactado.get('actividades_cierre', [])),
        
        'reflexiones': formatar_lista_con_vinetas(contenido_redactado.get('reflexiones', [])),
        'datos_faltantes': "Nota: Algunos datos fueron autocompletados. Para mayor precisión, colócalos en la próxima solicitud" if len(campos_por_defecto_usados) > 3 else ""
    }
    
    doc.render(contexto_final)
    
    print("📂 Por favor, elige dónde guardar el archivo...")
    root = tk.Tk()
    root.withdraw()

    nombre_sugerido = f"SESION_{plan_de_sesion.get('tema_central', 'SIN_TEMA').replace(' ', '_')}.docx"
    
    filepath = filedialog.asksaveasfilename(
        initialfile=nombre_sugerido,
        defaultextension=".docx",
        filetypes=[("Word Documents", "*.docx"), ("All Files", "*.*")]
    )
    
    if filepath:
        doc.save(filepath)
        print(f"🎉 ¡Éxito! La sesión ha sido guardada en: '{filepath}'")
    else:
        print("❌ Operación de guardado cancelada por el usuario.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generador de Sesiones de Aprendizaje con IA.")
    parser.add_argument("-p", "--prompt", required=True, help="El prompt del usuario para generar la sesión.")
    
    args = parser.parse_args()
    
    if not os.path.exists("plantilla_sesion.docx"):
        print("❌ Error fatal: El archivo 'plantilla_sesion.docx' no se encuentra en esta carpeta.")
    else:
        run(args.prompt)
