@echo off
echo ====================================
echo Configurando Portfolio Web CV
echo ====================================

echo.
echo [1] Verificando Python...
python --version

echo.
echo [2] Instalando dependencias...
pip install -r requirements.txt

echo.
echo [3] Inicializando base de datos...
python -c "from run import app, db; app.app_context().push(); db.create_all(); print('✅ Base de datos creada')"

echo.
echo ====================================
echo Instalacion completada exitosamente
echo ====================================
echo.
echo Para iniciar la aplicación, ejecuta:
echo   python run.py
echo.
echo Luego accede a:
echo   http://localhost:5000
echo.
pause
