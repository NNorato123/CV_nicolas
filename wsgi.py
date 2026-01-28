"""
WSGI entry point para servidores de producción
Compatible con: Gunicorn, uWSGI, etc.
Usado por Render y otros hosting
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from run import app

# Variable 'app' es lo que Render (y otros servidores) buscan
