import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail

db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
        'DATABASE_URL', 'sqlite:///portfolio.db'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SESSION_COOKIE_SECURE'] = False  # Set True en producción con HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = 2592000  # 30 días
    
    # Configuración de Flask-Mail
    app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 587))
    app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS', True)
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.environ.get('MAIL_DEFAULT_SENDER', 'noreply@nicolasnorato.com')
    
    # Inicializar extensiones
    db.init_app(app)
    mail.init_app(app)
    
    # Registrar blueprints
    from app.routes import main_bp
    app.register_blueprint(main_bp)
    
    # Crear tablas e inicializar datos
    with app.app_context():
        db.create_all()
        # Inicializar BD si está vacía
        _initialize_db_if_empty()
    
    return app

def _initialize_db_if_empty():
    """Inicializa la BD con datos de ejemplo si está vacía"""
    from app.models import Skill, Experience, Education
    
    # Verificar si ya hay datos
    if Skill.query.first() is not None:
        return  # Ya hay datos, no inicializar
    
    print('⏳ Base de datos vacía. Inicializando con datos de ejemplo...')
    
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
    
    db.session.commit()
    print('✅ Base de datos inicializada con datos de ejemplo')
