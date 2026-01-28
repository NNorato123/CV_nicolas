"""
WSGI entry point para servidores de producción
Compatible con: Gunicorn, uWSGI, etc.
"""

import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

from run import app

if __name__ == '__main__':
    app.run()
