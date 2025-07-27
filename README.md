🤖 Asistente Inteligente para la Generación de Documentos
Este proyecto es un asistente que utiliza la API de Google Gemini para automatizar la creación de planes de sesión o documentos de trabajo, con una configuración especializada para Ingeniería Civil. A partir de una simple frase en lenguaje natural, el sistema infiere la profesión del usuario, planifica, redacta y ensambla un documento de Word (.docx) completo y profesional.

✨ Características Clave
Enfoque Multi-fase Inteligente:

Inferencia de Profesión: Detecta el campo profesional del usuario (ej. Ingeniero, Pedagogo) para adaptar el tono y la terminología.

Planificación Estratégica: La IA analiza la solicitud y crea un plan estructurado, seleccionando competencias y ejes temáticos relevantes del archivo de configuración.

Redacción Contextual: Con el plan ya definido, la IA redacta todo el contenido detallado, asegurando coherencia y calidad.

Adaptabilidad Universal: El núcleo del sistema es agnóstico a la profesión. Su especialización (actualmente en Ingeniería Civil) reside en el archivo config.py. ¡Puedes editar este archivo para adaptar el asistente a cualquier carrera o nivel académico! Simplemente modifica las competencias y ejes para que se ajusten a tu campo de estudio.

Valores por Defecto Inteligentes: Rellena automáticamente la fecha actual, docente, institución y otros datos si no se especifican, ahorrando tiempo y esfuerzo.

Notificaciones Útiles: Si muchos datos son autocompletados, el documento final incluirá una nota sugiriendo al usuario ser más específico en la próxima solicitud.

Seguro y Modular: Mantiene la clave de la API fuera del código fuente y organiza el código en módulos para un fácil mantenimiento y personalización.

Control Total de Guardado: Permite al usuario elegir dónde guardar el archivo generado a través de un diálogo nativo del sistema.

🚀 Cómo Usarlo
Sigue estos pasos para poner en marcha el generador.

Prerrequisitos
Python 3.8 o superior.

Una clave de API de Google Gemini (puedes obtenerla en Google AI Studio).

1. Clonar el Repositorio
git clone [URL_DE_TU_REPOSITORIO_EN_GITHUB]
cd [NOMBRE_DE_LA_CARPETA_DEL_PROYECTO]

2. Configurar el Entorno
Crea un archivo llamado .env en la raíz del proyecto. No lo subas a GitHub.

Abre el archivo .env con un editor de texto y pega tu clave de API de Gemini:

# .env
GEMINI_API_KEY="AIzaSy...TU_CLAVE_AQUI"

3. Instalar las Dependencias
Crea un entorno virtual (recomendado) e instala las librerías necesarias.

# Crear y activar un entorno virtual (opcional pero recomendado)
python -m venv venv
source venv/bin/activate  # En Windows usa `venv\Scripts\activate`

# Instalar las librerías
pip install -r requirements.txt

4. Ejecutar el Generador
Ejecuta el script desde tu terminal usando el argumento -p o --prompt.

Ejemplo Simple (usará muchos valores por defecto):

python main.py -p "Necesito una sesión sobre análisis de suelos para cimentaciones."

(El sistema inferirá "Ingeniería Civil" y usará los valores por defecto para la mayoría de los campos)

Ejemplo Completo (especificando todos los datos):

python main.py -p "Prepara una sesión de trabajo para la unidad 2, sesión número 3. El tema es 'Diseño de una viga de concreto postensado'. Es para el nivel de Postgrado, en el área de 'Ingeniería Estructural', para el noveno semestre. La duración debe ser de 180 minutos. El docente a cargo es 'Dr. Ricardo Morandi' y la institución es la 'Universidad Politécnica de Milán'. La fecha es el 15 de octubre de 2025."

¡Espera unos segundos, elige dónde guardar y tu archivo .docx estará listo!