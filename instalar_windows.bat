@echo off
REM ============================================
REM INSTALADOR AUTOMATICO - Rizoma Automation
REM Para Windows
REM ============================================

echo.
echo ============================================
echo   INSTALADOR RIZOMA AUTOMATION v2.1
echo ============================================
echo.

REM Verificar Python
echo [1/6] Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python no esta instalado
    echo Por favor instala Python 3.8+ desde https://www.python.org
    pause
    exit /b 1
)
echo OK - Python encontrado
echo.

REM Crear entorno virtual
echo [2/6] Creando entorno virtual...
if exist venv (
    echo Entorno virtual ya existe, omitiendo...
) else (
    python -m venv venv
    echo OK - Entorno virtual creado
)
echo.

REM Activar entorno virtual
echo [3/6] Activando entorno virtual...
call venv\Scripts\activate.bat
echo OK - Entorno virtual activado
echo.

REM Instalar dependencias
echo [4/6] Instalando dependencias Python...
echo Esto puede tomar unos minutos...
pip install --quiet --upgrade pip
pip install --quiet flask python-docx reportlab playwright
echo OK - Dependencias instaladas
echo.

REM Instalar Chromium
echo [5/6] Instalando navegador Chromium...
echo Esto puede tomar varios minutos...
python -m playwright install chromium
echo OK - Chromium instalado
echo.

REM Crear directorios necesarios
echo [6/6] Creando estructura de directorios...
if not exist uploads mkdir uploads
if not exist outputs mkdir outputs
if not exist scripts mkdir scripts
echo OK - Directorios creados
echo.

REM Verificar archivos necesarios
echo Verificando archivos del proyecto...
if not exist app.py (
    echo ADVERTENCIA: app.py no encontrado
    echo Asegurate de estar en la carpeta correcta del proyecto
)
if not exist rizoma_automation.py (
    echo ADVERTENCIA: rizoma_automation.py no encontrado
)
echo.

echo ============================================
echo   INSTALACION COMPLETADA
echo ============================================
echo.
echo Para iniciar el sistema:
echo   1. Abre una terminal en esta carpeta
echo   2. Ejecuta: venv\Scripts\activate
echo   3. Ejecuta: python app.py
echo   4. Abre tu navegador en: http://localhost:5000
echo.
echo Lee GUIA_COMPLETA.md para instrucciones detalladas
echo.
pause
