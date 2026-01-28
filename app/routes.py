from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from app.models import Project, Skill, Experience, Education, BlogPost, ContactMessage
from app import db, mail
from app.github_service import GitHubService
from app.language_colors import get_language_color
from flask_mail import Message
import os
from functools import wraps

main_bp = Blueprint('main', __name__)

# Contraseña para acceso al blog (guardada en .env o variable de entorno)
BLOG_PASSWORD = os.getenv('BLOG_PASSWORD', 'nicolas2024')

def require_admin_auth(f):
    """Decorador para proteger rutas de administración"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_auth' not in session:
            return redirect(url_for('main.admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/')
def index():
    """Página principal - Hero y presentación"""
    featured_projects = Project.query.filter_by(featured=True).order_by(Project.order).limit(3).all()
    return render_template('index.html', featured_projects=featured_projects)

@main_bp.route('/proyectos')
def proyectos():
    """
    Página de proyectos - Opción A (Híbrida)
    
    Obtiene:
    1. Repos de GitHub de forma DINÁMICA (automáticamente se actualizan)
    2. Proyectos destacados de la BD (opcional)
    
    Los repos de GitHub aparecen en primer plano.
    """
    # Obtener repos de GitHub
    github_repos = GitHubService.get_repos()
    
    # Convertir repos de GitHub a formato compatible con template
    projects = []
    
    # Agregar repos de GitHub
    for repo in github_repos:
        # Procesar lenguajes del repositorio
        languages_data = repo.get('languages', {})
        languages_list = []
        if languages_data:
            # Ordenar lenguajes por cantidad de bytes (mayor a menor)
            sorted_langs = sorted(languages_data.items(), key=lambda x: x[1], reverse=True)
            for lang, bytes_count in sorted_langs:
                languages_list.append({
                    'name': lang,
                    'color': get_language_color(lang),
                    'bytes': bytes_count
                })
        
        projects.append({
            'title': repo['name'],
            'description': repo['description'],
            'technologies': repo['language'],
            'languages': languages_list,  # Nuevo: lista de lenguajes con colores
            'github_url': repo['github_url'],
            'live_url': None,
            'image_url': repo['image_url'],
            'featured': False,
            'is_github': True,
            'stars': repo['stars'],
        })
    
    # Obtener tecnologías únicas para los filtros
    all_techs = set()
    for project in projects:
        if project['technologies']:
            # Limpiar y agregar tecnologías
            techs = [tech.strip() for tech in str(project['technologies']).split(',')]
            all_techs.update(techs)
    
    technologies = sorted(list(all_techs))
    
    return render_template('proyectos.html', projects=projects, technologies=technologies)

@main_bp.route('/sobre-mi')
def sobre_mi():
    """Página de información personal"""
    skills_by_category = {}
    skills = Skill.query.order_by(Skill.category, Skill.order).all()
    
    for skill in skills:
        if skill.category not in skills_by_category:
            skills_by_category[skill.category] = []
        skills_by_category[skill.category].append(skill)
    
    experiences = Experience.query.order_by(Experience.order).all()
    educations = Education.query.order_by(Education.order).all()
    
    return render_template('sobre_mi.html', 
                         skills_by_category=skills_by_category,
                         experiences=experiences,
                         educations=educations)

@main_bp.route('/contacto', methods=['GET', 'POST'])
def contacto():
    """Página de contacto"""
    if request.method == 'POST':
        # Obtener datos del formulario
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip()
        subject = request.form.get('subject', '').strip()
        message = request.form.get('message', '').strip()
        
        # Validación básica
        if not all([name, email, subject, message]):
            return render_template('contacto.html', error='Todos los campos son requeridos')
        
        if len(message) < 10:
            return render_template('contacto.html', error='El mensaje debe tener al menos 10 caracteres')
        
        try:
            # Guardar en BD
            contact_msg = ContactMessage(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            db.session.add(contact_msg)
            db.session.commit()
            
            # Enviar email
            try:
                email_body = f"""
Nuevo mensaje de contacto desde tu portfolio:

Nombre: {name}
Email: {email}
Asunto: {subject}

Mensaje:
{message}

---
Responde directamente a: {email}
                """
                
                msg = Message(
                    subject=f'[Portfolio] {subject}',
                    recipients=['nnicolasnorato@gmail.com'],
                    body=email_body,
                    reply_to=email
                )
                mail.send(msg)
                
                # También enviar confirmación al usuario
                confirmation_msg = Message(
                    subject='Hemos recibido tu mensaje',
                    recipients=[email],
                    body=f"""Hola {name},

Gracias por contactarme. He recibido tu mensaje y me pondré en contacto contigo pronto.

Asunto: {subject}

Saludos,
Nicolás Norato
                    """
                )
                mail.send(confirmation_msg)
            except Exception as e:
                print(f"Error al enviar email: {e}")
                # Continuar aunque falle el email
            
            return render_template('contacto.html', success='¡Mensaje enviado exitosamente! Me pondré en contacto pronto.')
        
        except Exception as e:
            print(f"Error al procesar contacto: {e}")
            return render_template('contacto.html', error='Hubo un error al procesar tu mensaje. Intenta de nuevo.')
    
    return render_template('contacto.html')

@main_bp.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    """Login para acceder al panel de administración"""
    if request.method == 'POST':
        password = request.form.get('password', '')
        if password == BLOG_PASSWORD:
            session['admin_auth'] = True
            return redirect(url_for('main.admin_panel'))
        else:
            return render_template('admin_login.html', error='Contraseña incorrecta')
    return render_template('admin_login.html')

@main_bp.route('/admin')
@require_admin_auth
def admin_panel():
    """Panel de administración para crear/editar posts"""
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('admin.html', posts=posts)

@main_bp.route('/admin/crear', methods=['GET', 'POST'])
@require_admin_auth
def admin_crear_post():
    """Crear nuevo post"""
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        content = request.form.get('content', '').strip()
        summary = request.form.get('summary', '').strip()
        
        if not title or not content:
            return render_template('admin_create.html', error='Título y contenido son requeridos')
        
        post = BlogPost(
            title=title,
            content=content,
            summary=summary,
            order=BlogPost.query.count() + 1
        )
        db.session.add(post)
        db.session.commit()
        
        return redirect(url_for('main.admin_panel'))
    
    return render_template('admin_create.html')

@main_bp.route('/admin/editar/<int:post_id>', methods=['GET', 'POST'])
@require_admin_auth
def admin_editar_post(post_id):
    """Editar post existente"""
    post = BlogPost.query.get_or_404(post_id)
    
    if request.method == 'POST':
        post.title = request.form.get('title', '').strip()
        post.content = request.form.get('content', '').strip()
        post.summary = request.form.get('summary', '').strip()
        
        if not post.title or not post.content:
            return render_template('admin_edit.html', post=post, error='Título y contenido son requeridos')
        
        db.session.commit()
        return redirect(url_for('main.admin_panel'))
    
    return render_template('admin_edit.html', post=post)

@main_bp.route('/admin/eliminar/<int:post_id>', methods=['POST'])
@require_admin_auth
def admin_eliminar_post(post_id):
    """Eliminar post"""
    post = BlogPost.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('main.admin_panel'))

@main_bp.route('/blog')
def blog():
    """Blog público - cualquiera puede leer"""
    posts = BlogPost.query.order_by(BlogPost.created_at.desc()).all()
    return render_template('blog.html', posts=posts)

@main_bp.route('/blog/post/<int:post_id>')
def blog_post(post_id):
    """Ver post completo del blog - público"""
    post = BlogPost.query.get_or_404(post_id)
    return render_template('blog_post.html', post=post)

@main_bp.route('/admin/logout')
def admin_logout():
    """Logout del panel admin"""
    session.pop('admin_auth', None)
    return redirect(url_for('main.index'))

@main_bp.route('/api/proyectos-filtrado')
def api_proyectos_filtrado():
    """API para obtener proyectos filtrados y buscados"""
    search_query = request.args.get('search', '').lower().strip()
    technology = request.args.get('tech', '').strip()
    
    # Obtener repos de GitHub
    github_repos = GitHubService.get_repos()
    projects = []
    
    # Convertir repos de GitHub
    for repo in github_repos:
        projects.append({
            'title': repo['name'],
            'description': repo['description'],
            'technologies': repo['language'],
            'github_url': repo['github_url'],
            'live_url': None,
            'image_url': repo['image_url'],
            'featured': False,
            'is_github': True,
            'stars': repo['stars'],
        })
    
    # Agregar proyectos de BD
    featured_projects = Project.query.filter_by(featured=True).order_by(Project.order).all()
    for project in featured_projects:
        projects.append({
            'title': project.title,
            'description': project.description,
            'technologies': project.technologies,
            'github_url': project.github_url,
            'live_url': project.live_url,
            'image_url': project.image_url,
            'featured': True,
            'is_github': False,
        })
    
    # Filtrar por búsqueda
    if search_query:
        projects = [p for p in projects if 
                   search_query in p['title'].lower() or 
                   search_query in (p['description'] or '').lower()]
    
    # Filtrar por tecnología
    if technology:
        filtered = []
        for p in projects:
            techs = [tech.strip() for tech in str(p['technologies']).split(',')]
            if technology in techs:
                filtered.append(p)
        projects = filtered
    
    return jsonify(projects)

@main_bp.route('/api/proyectos')
def api_proyectos():
    """API para obtener proyectos en JSON"""
    projects = Project.query.order_by(Project.order).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'description': p.description,
        'technologies': p.technologies.split(','),
        'github_url': p.github_url,
        'live_url': p.live_url,
        'image_url': p.image_url,
        'featured': p.featured
    } for p in projects])

@main_bp.route('/api/habilidades')
def api_habilidades():
    """API para obtener habilidades en JSON"""
    skills = Skill.query.order_by(Skill.category, Skill.order).all()
    return jsonify([{
        'id': s.id,
        'category': s.category,
        'name': s.name,
        'proficiency': s.proficiency
    } for s in skills])


