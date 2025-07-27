# config.py
import os
from dotenv import load_dotenv

def load_api_key():
    """Carga la API Key de Gemini desde el archivo .env de forma segura."""
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("❌ Error: La variable de entorno GEMINI_API_KEY no está definida. Por favor, crea un archivo .env y añade tu clave.")
    return api_key

# Estos son los datos pedagógicos base que la IA usará para tomar decisiones.
DATOS_FIJOS = {
    "competencias": {
        "Diseno_Estructural": {
            "texto": "DISEÑA Y ANALIZA SISTEMAS ESTRUCTURALES",
            "capacidades": "• Aplica principios de estática, dinámica y mecánica de materiales.\n• Modela y simula el comportamiento de estructuras bajo cargas estáticas y sísmicas.\n• Selecciona y dimensiona elementos de concreto armado y acero según normativas vigentes."
        },
        "Gestion_Proyectos": {
            "texto": "GESTIONA PROYECTOS DE INFRAESTRUCTURA CIVIL",
            "capacidades": "• Planifica y programa las fases de un proyecto utilizando metodologías como PMBOK o Lean Construction.\n• Estima costos, presupuestos y gestiona la cadena de suministro.\n• Supervisa la ejecución de obras garantizando la calidad, seguridad y cumplimiento de plazos."
        },
        "Geotecnia_Cimentaciones": {
            "texto": "APLICA PRINCIPIOS DE GEOTECNIA Y DISEÑO DE CIMENTACIONES",
            "capacidades": "• Interpreta estudios de mecánica de suelos para caracterizar el subsuelo.\n• Diseña cimentaciones superficiales y profundas para diversas estructuras.\n• Evalúa la estabilidad de taludes y diseña sistemas de contención."
        },
        "Hidraulica_Recursos_Hidricos": {
            "texto": "DISEÑA Y GESTIONA OBRAS HIDRÁULICAS Y RECURSOS HÍDRICOS",
            "capacidades": "• Aplica los principios de la mecánica de fluidos en canales y tuberías.\n• Diseña sistemas de abastecimiento de agua potable y alcantarillado.\n• Modela y gestiona cuencas hidrográficas y obras de aprovechamiento hídrico."
        },
        "Ingenieria_Transporte": {
            "texto": "PLANIFICA Y DISEÑA INFRAESTRUCTURA DE TRANSPORTE",
            "capacidades": "• Realiza estudios de demanda y flujo de tráfico para la planificación vial.\n• Diseña la geometría de carreteras, intersecciones y pavimentos.\n• Aplica normativas de diseño vial y seguridad para optimizar la movilidad."
        }
    },
    "ejes": {
        "Sostenibilidad y Resiliencia Ambiental": {
            "valor": "Sostenibilidad",
            "actitud": "Integra soluciones de bajo impacto ambiental, utiliza materiales eco-amigables y diseña infraestructuras resilientes al cambio climático."
        },
        "Seguridad y Ética Profesional": {
            "valor": "Responsabilidad Profesional",
            "actitud": "Prioriza la seguridad estructural y ocupacional en todas las fases del proyecto, adhiriéndose a los códigos de ética y normativas."
        },
        "Optimización de Recursos y Materiales": {
            "valor": "Eficiencia",
            "actitud": "Busca la optimización de materiales, costos y plazos mediante el uso de tecnologías, prefabricados y metodologías innovadoras."
        },
        "Impacto Social y Desarrollo Urbano": {
            "valor": "Compromiso Social",
            "actitud": "Diseña proyectos que mejoran la calidad de vida de la comunidad, son accesibles y se integran armónicamente con el entorno urbano."
        },
        "Transformacion Digital BIM": {
            "valor": "Innovación Tecnológica",
            "actitud": "Utiliza herramientas digitales como BIM (Building Information Modeling) para la gestión integrada del ciclo de vida del proyecto."
        },
        "Automatizacion Robótica Construcción": {
            "valor": "Automatización",
            "actitud": "Investiga e implementa el uso de robótica, drones y sensores para automatizar tareas de inspección, monitoreo y construcción."
        }
    }
}