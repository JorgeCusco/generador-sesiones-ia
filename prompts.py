# prompts.py
import json
from config import DATOS_FIJOS

def get_profesion_prompt(prompt_del_usuario):
    """Devuelve un prompt simple para inferir la profesión del usuario."""
    return f"""
    Analiza la siguiente solicitud de un usuario y dime cuál es su profesión o campo de estudio más probable en una o dos palabras.
    Ejemplos: 'pedagogo', 'ingeniero civil', 'abogado', 'médico'.
    Solicitud: "{prompt_del_usuario}"
    """

def get_planificador_prompt(prompt_del_usuario, profesion_inferida):
    """Devuelve el prompt para la Fase 1: Planificación."""
    return f"""
    Actúa como un asistente experto en {profesion_inferida}. Analiza la solicitud de un profesional y crea un plan estructurado para una sesión o tarea.
    
    Solicitud: "{prompt_del_usuario}"

    Tu tarea es devolver un objeto JSON con la siguiente estructura:
    1.  Extrae los siguientes datos si se especifican en la solicitud. Si un dato no se especifica, su valor debe ser null: "tema_central", "fecha", "numero_unidad", "numero_sesion", "nivel_academico", "semestre", "docente", "institucion_educativa", "area", "duracion" (número entero de minutos).
    2.  Analiza el tema y elige la competencia más adecuada de esta lista: {json.dumps(list(DATOS_FIJOS['competencias'].keys()))}. Pon el nombre en la clave "competencia_seleccionada".
    3.  Analiza el tema y selecciona los DOS ejes más relevantes de esta lista: {json.dumps(list(DATOS_FIJOS['ejes'].keys()))}. Devuelve los nombres en una lista en la clave "ejes_seleccionados".
    
    Devuelve EXCLUSIVAMENTE un objeto JSON.
    """

def get_redactor_prompt(plan_de_sesion, competencia_info, tiempos):
    """Devuelve el prompt para la Fase 2: Redacción."""
    return f"""
    Actúa como un experto en {plan_de_sesion.get('nivel_academico', 'educación superior')} y creativo. Basado en el siguiente plan de sesión, redacta el contenido pedagógico.

    Plan de Sesión:
    - Tema Central: {plan_de_sesion.get('tema_central', 'No especificado')}
    - Semestre: {plan_de_sesion.get('semestre', 'No especificado')}
    - Nivel Académico: {plan_de_sesion.get('nivel_academico', 'No especificado')}
    - Competencia a trabajar: {competencia_info.get('texto', 'No especificado')}
    - Duración Total: {plan_de_sesion.get('duracion', 90)} minutos

    Tu tarea es devolver un objeto JSON con el siguiente contenido redactado:
    - "titulo": Un título creativo y profesional para la sesión.
    - "desempenos": Una lista de cadenas de texto con los desempeños o resultados esperados.
    - "evidencia": La evidencia de aprendizaje o entregable que producirán los participantes.
    - "preparacion": Una lista de 3 a 4 cadenas de texto con los materiales o preparativos necesarios.
    - "actividades_inicio": Una lista de cadenas de texto con las actividades para el INICIO ({tiempos['inicio']} min).
    - "actividades_desarrollo": Una lista de cadenas de texto con las actividades para el DESARROLLO ({tiempos['desarrollo']} min).
    - "actividades_cierre": Una lista de cadenas de texto con las actividades para el CIERRE ({tiempos['cierre']} min).
    - "reflexiones": Una lista de 3 cadenas de texto con preguntas de reflexión para el profesional que dirige la sesión.

    Devuelve EXCLUSIVAMENTE un objeto JSON.
    """