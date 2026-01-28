import os
from app import create_app, db
from app.models import Project, Skill, Experience, Education, BlogPost

app = create_app()

# Configuración para Render (debe estar en el bloque principal)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    # host='0.0.0.0' permite que se acceda desde cualquier dirección (necesario en Render)
    app.run(host='0.0.0.0', port=port, debug=False)

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Project': Project,
        'Skill': Skill,
        'Experience': Experience,
        'Education': Education,
        'BlogPost': BlogPost    
    }

@app.cli.command()
def init_db():
    """Inicializar la base de datos con datos de ejemplo"""
    db.drop_all()
    db.create_all()
    
    # Agregar habilidades
    skills_data = [
        # Lenguajes de Programación
        ('Lenguajes', 'Python', 95),
        ('Lenguajes', 'C#', 85),
        ('Lenguajes', 'JavaScript', 80),
        ('Lenguajes', 'Java', 75),
        
        # Desarrollo de Videojuegos
        ('Videojuegos', 'Unity', 90),
        ('Videojuegos', 'C# para Juegos', 88),
        ('Videojuegos', 'Gamedev', 85),
        
        # IA e Integración de APIs
        ('IA & APIs', 'Integración de APIs', 90),
        ('IA & APIs', 'Inteligencia Artificial', 80),
        ('IA & APIs', 'ChatGPT API', 85),
        ('IA & APIs', 'Machine Learning', 75),
        
        # Desarrollo Web
        ('Desarrollo Web', 'Flask', 88),
        ('Desarrollo Web', 'HTML/CSS', 85),
        ('Desarrollo Web', 'JavaScript Web', 82),
        ('Desarrollo Web', 'Responsive Design', 88),
        
        # Herramientas
        ('Herramientas', 'Git', 90),
        ('Herramientas', 'GitHub', 90),
        ('Herramientas', 'VS Code', 95),
        ('Herramientas', 'SQL', 85),
    ]
    
    for i, (category, name, proficiency) in enumerate(skills_data):
        skill = Skill(category=category, name=name, proficiency=proficiency, order=i)
        db.session.add(skill)
    
    # Agregar experiencia
    experiences_data = [
        {
            'title': 'Cajero / Atención al Cliente',
            'company': 'ÉXITO (Los Almacenes)',
            'location': 'Bucaramanga, Colombia',
            'start_date': 'Agosto 2025',
            'end_date': 'Septiembre 2025',
            'description': 'Atención profesional al cliente, gestión de caja, control de inventario y resolución de problemas. Experiencia que desarrolló mis habilidades de comunicación, paciencia y trabajo bajo presión.'
        },
        {
            'title': 'Operario Multifuncional',
            'company': 'Cine (Cinematografía)',
            'location': 'Bucaramanga, Colombia',
            'start_date': 'Noviembre 2025',
            'end_date': 'Enero 2026',
            'description': 'Servicio al cliente, operaciones de cine, mantenimiento de instalaciones y gestión de eventos. Experiencia en ambiente dinámico que fortaleció mi adaptabilidad y capacidad de aprendizaje rápido.'
        },
        {
            'title': 'Estudiante Técnico en Sistemas & Desarrollador',
            'company': 'UTS + Proyectos Personales',
            'location': 'Bucaramanga, Colombia',
            'start_date': '2026 - Presente',
            'end_date': None,
            'description': 'Cursando Técnico en Sistemas en UTS mientras desarrollo proyectos personales en Python, Unity y desarrollo web. Integración de APIs de IA y participación activa en comunidades tecnológicas.'
        },
    ]
    
    for i, exp in enumerate(experiences_data):
        experience = Experience(order=i, **exp)
        db.session.add(experience)
    
    # Agregar educación
    educations_data = [
        {
            'degree': 'Técnico en Sistemas',
            'institution': 'UTS (Unidades Tecnológicas de Santander)',
            'field': 'Formación Técnica en Sistemas',
            'year': '2026',
            'description': 'Formación técnica en desarrollo de sistemas, programación, redes y tecnologías de información. En curso desde enero 2026.'
        },
    ]
    
    for i, edu in enumerate(educations_data):
        education = Education(order=i, **edu)
        db.session.add(education)
    
    # Agregar proyectos
    projects_data = [
        {
            'title': 'Portfolio Web Personal',
            'description': 'Portfolio web moderno con diseño oscuro, modo claro/oscuro, animaciones suaves, filtros de proyectos y formulario de contacto funcional con integración de Gmail.',
            'technologies': 'Python, Flask, JavaScript, CSS3, HTML5',
            'github_url': 'https://github.com/NNorato123/paginaweb_cv',
            'live_url': None,
            'featured': True,
            'order': 0
        },
        {
            'title': 'Chatbot con IA (ChatGPT API)',
            'description': 'Aplicación de chatbot interactivo que integra la API de ChatGPT/OpenAI. Incluye historial de conversaciones, personalización de parámetros y múltiples modos de interacción.',
            'technologies': 'Python, Flask, OpenAI API, JavaScript, SQLite',
            'github_url': 'https://github.com/NNorato123/chatbot-ia',
            'live_url': None,
            'featured': True,
            'order': 1
        },
        {
            'title': 'Juego 2D en Unity',
            'description': 'Juego indie 2D desarrollado en Unity con mecánicas originales, sistemas de puntuación, interfaz gráfica interactiva y optimización de rendimiento.',
            'technologies': 'Unity, C#, Blender (Modelado 3D)',
            'github_url': 'https://github.com/NNorato123/unity-game-2d',
            'live_url': None,
            'featured': True,
            'order': 2
        },
        {
            'title': 'API REST de Gestor de Tareas',
            'description': 'Servicio API RESTful completo para gestión de tareas. Incluye autenticación JWT, validación de datos, documentación automática con Swagger y pruebas unitarias.',
            'technologies': 'Python, Flask, PostgreSQL, JWT, Docker',
            'github_url': 'https://github.com/NNorato123/task-api',
            'live_url': None,
            'featured': False,
            'order': 3
        },
        {
            'title': 'Sistema de Procesamiento de Imágenes',
            'description': 'Herramienta de procesamiento de imágenes usando APIs de IA. Detección de objetos, análisis de contenido y generación de descripciones automáticas con Vision API.',
            'technologies': 'Python, OpenCV, Vision API, Flask',
            'github_url': 'https://github.com/NNorato123/image-processor-ai',
            'live_url': None,
            'featured': False,
            'order': 4
        },
    ]
    
    for project in projects_data:
        proj = Project(**project)
        db.session.add(proj)
    
    # Agregar posts de blog de ejemplo
    blog_posts_data = [
        {
            'title': 'Mi Viaje en el Mundo de la Programación',
            'content': '''Bienvenido a mi espacio privado de reflexiones y aprendizajes.

## Mi Historia

Comencé mi viaje en la tecnología como técnico en sistemas en la UTS. Sin experiencia previa en programación, decidí aprovechar mi tiempo en el sector de servicios (ÉXITO y cine) para desarrollar habilidades blandas mientras aprendía a programar de forma autodidacta.

## Lo que he aprendido

- **Python**: Mi lenguaje favorito para desarrollo backend
- **Desarrollo de videojuegos**: Explorando Unity y C#
- **IA e Integración de APIs**: Usando ChatGPT y OpenAI APIs
- **Desarrollo Web Full-Stack**: Con Flask, JavaScript y modernos frameworks
- **Adaptabilidad**: La clave para crecer rápido en tecnología

## Mi filosofía

Creo que el aprendizaje constante y la curiosidad son las herramientas más poderosas en tecnología. Cada proyecto es una oportunidad para crecer y resolver problemas reales.

## Siguientes metas

- Especializarme en IA y Machine Learning
- Contribuir a proyectos open-source
- Crear herramientas útiles para la comunidad
- Continuar innovando en videojuegos

¡Espero que disfrutes explorando mi portfolio! 🚀''',
            'summary': 'Mi viaje en programación y aprendizaje constante',
            'order': 0
        }
    ]
    
    for post in blog_posts_data:
        blog_post = BlogPost(**post)
        db.session.add(blog_post)
    
    db.session.commit()
    print('✅ Base de datos inicializada con datos de ejemplo')

if __name__ == '__main__':
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()
        print('✅ Tablas de la base de datos creadas')
    
    app.run(debug=True, host='0.0.0.0', port=5000)
