# 🌐 Portafolio CV Profesional

Una aplicación web moderna y completa para showcasear tu portafolio profesional, CV, proyectos y blog personal. Construida con Flask, SQLAlchemy y un diseño responsive.

## 📋 Características Principales

### 🎯 Páginas Públicas
- **Inicio (Hero)**: Presentación atractiva con información destacada
- **Sobre Mí**: Sección de perfil con:
  - Información personal
  - Habilidades técnicas organizadas por categorías
  - Experiencia laboral
  - Educación y formación
- **Proyectos**: Galería de proyectos con:
  - Integración automática con repositorios de GitHub
  - Filtrado por tecnologías
  - Links a código fuente y demos en vivo
  - Proyectos destacados de la base de datos
- **Blog**: Artículos y posts personales
- **Contacto**: Formulario para recibir mensajes de visitantes

### 🔐 Panel de Administración
- Login seguro con contraseña
- Gestión completa de contenido:
  - Crear, editar y eliminar proyectos
  - Administrar habilidades y categorías
  - Publicar posts en el blog
  - Ver mensajes de contacto recibidos
- Sesiones seguras con cookies protegidas

### 🔄 Integración GitHub
- Obtención automática de repositorios desde tu cuenta GitHub
- Actualización dinámica de proyectos
- Caché de 5 segundos para optimizar API calls
- Información de stars y lenguaje de programación

### 🌍 Características Web
- **Diseño Responsive**: Compatible con móviles, tablets y desktops
- **Tema Oscuro/Claro**: Sistema de tema intercambiable
- **Internacionalización (i18n)**: Soporte multiidioma
- **Animations**: Transiciones suaves y efectos visuales
- **PWA Ready**: Manifiesto de sitio web incluido

## 🛠️ Stack Tecnológico

### Backend
- **Framework**: Flask 2.3.3
- **Base de Datos**: SQLAlchemy (SQLite por defecto)
- **Templating**: Jinja2
- **Email**: Flask-Mail (SMTP)
- **Forms**: WTForms con validación
- **API Integration**: Requests (GitHub API)

### Frontend
- **HTML5**: Estructura semántica
- **CSS3**: Estilos modernos y responsive
- **JavaScript Vanilla**: Interactividad sin dependencias
- **i18n.js**: Internacionalización en cliente

### DevOps
- **Versioning**: Git
- **Deployment**: Compatible con Heroku (Procfile incluido)
- **WSGI**: Gunicorn via wsgi.py

## 📦 Requisitos

- Python 3.8+
- pip (gestor de paquetes Python)
- Git

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/NNorato123/paginaweb_cv.git
cd paginaweb_cv
```

### 2. Crear entorno virtual
```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Crea un archivo `.env` en la raíz del proyecto:
```env
# Configuración Flask
SECRET_KEY=tu-clave-secreta-super-segura-cambiar-en-produccion
FLASK_ENV=development

# Configuración Base de Datos
DATABASE_URL=sqlite:///portfolio.db

# Contraseña para panel de administración
BLOG_PASSWORD=tu-contraseña-admin

# GitHub
GITHUB_TOKEN=tu_token_github_opcional
GITHUB_USERNAME=NNorato123

# Email (opcional, para contacto)
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=tu-email@gmail.com
MAIL_PASSWORD=tu-contraseña-app
MAIL_DEFAULT_SENDER=tu-email@gmail.com
```

### 5. Inicializar la base de datos
```bash
python run.py
flask init-db
```

### 6. Ejecutar la aplicación
```bash
python run.py
```

La aplicación estará disponible en `http://localhost:5000`

## 📂 Estructura del Proyecto

```
paginaweb_cv/
├── app/
│   ├── __init__.py              # Configuración de Flask
│   ├── routes.py                # Rutas y lógica principal
│   ├── models.py                # Modelos de base de datos
│   ├── github_service.py        # Servicio de integración GitHub
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Estilos principales
│   │   ├── js/
│   │   │   ├── main.js          # JavaScript principal
│   │   │   ├── theme.js         # Gestión de tema oscuro/claro
│   │   │   ├── i18n.js          # Internacionalización
│   │   │   └── animations.js    # Animaciones
│   │   ├── images/              # Imágenes del sitio
│   │   ├── translations.json    # Traducciones
│   │   └── site.webmanifest     # Configuración PWA
│   └── templates/
│       ├── base.html            # Template base
│       ├── index.html           # Página inicio
│       ├── sobre_mi.html        # Perfil y habilidades
│       ├── proyectos.html       # Galería de proyectos
│       ├── blog.html            # Listado de posts
│       ├── blog_post.html       # Detalle de post
│       ├── contacto.html        # Formulario contacto
│       ├── admin.html           # Panel admin
│       ├── admin_login.html     # Login admin
│       ├── admin_create.html    # Crear contenido
│       └── admin_edit.html      # Editar contenido
├── instance/                    # Datos de instancia (BD, etc)
├── run.py                       # Punto de entrada
├── wsgi.py                      # Para producción (WSGI)
├── requirements.txt             # Dependencias Python
├── .env                         # Variables de entorno
├── .gitignore                   # Archivos ignorados por Git
├── Procfile                     # Configuración Heroku
└── README.md                    # Este archivo
```

## 🗄️ Modelos de Base de Datos

### Project
- Proyectos mostrados en la galería
- Puede venir de GitHub o estar en BD

### Skill
- Habilidades técnicas
- Organizadas por categoría (Backend, Frontend, Herramientas, etc.)
- Nivel de proficiencia (0-100)

### Experience
- Experiencia laboral
- Títulos, empresas, fechas y descripciones

### Education
- Educación formal
- Instituciones, títulos, años

### BlogPost
- Posts del blog
- Título, contenido, resumen
- Timestamps de creación y actualización

### ContactMessage
- Mensajes recibidos del formulario de contacto
- Nombre, email, asunto, mensaje
- Marcable como leído/no leído

## 🔒 Seguridad

- Contraseña protegida para panel de administración
- Sesiones seguras con cookies HTTP-only
- CSRF protection con WTForms
- Variables sensibles en `.env` (no en repositorio)
- Validación de email con email-validator

## 📱 Responsividad

La aplicación es completamente responsive y se adapta a:
- Móviles (320px+)
- Tablets (768px+)
- Desktops (1024px+)
- Pantallas grandes (1440px+)

## 🌐 Internacionalización

Soporta múltiples idiomas mediante `i18n.js`:
- Español
- Inglés (extensible a más idiomas)

Edita `static/translations.json` para agregar más idiomas.

## 📧 Contacto

El formulario de contacto envía emails usando SMTP (Gmail por defecto). Configura las credenciales en `.env`.

## 🚢 Deploy

### Heroku
```bash
git push heroku main
```

El archivo `Procfile` está configurado para Heroku con Gunicorn.

### Otros servidores
Usa `wsgi.py` con:
```bash
gunicorn wsgi:app
```

## 📝 Licencia

Este proyecto es personal. Siéntete libre de adaptarlo a tus necesidades.

## 👨‍💻 Autor

**Nicolás Norato** - [@NNorato123](https://github.com/NNorato123)

---

⭐ Si te es útil, considera dejar una estrella en GitHub
