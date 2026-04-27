#!/bin/bash
# ============================================
# INSTALADOR AUTOMATICO - Rizoma Automation
# Para Mac/Linux
# ============================================

echo ""
echo "============================================"
echo "   INSTALADOR RIZOMA AUTOMATION v2.1"
echo "============================================"
echo ""

# Verificar Python
echo "[1/6] Verificando Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ ERROR: Python no está instalado"
    echo "Por favor instala Python 3.8+ desde https://www.python.org"
    exit 1
fi
echo "✓ OK - Python encontrado"
echo ""

# Crear entorno virtual
echo "[2/6] Creando entorno virtual..."
if [ -d "venv" ]; then
    echo "Entorno virtual ya existe, omitiendo..."
else
    python3 -m venv venv
    echo "✓ OK - Entorno virtual creado"
fi
echo ""

# Activar entorno virtual
echo "[3/6] Activando entorno virtual..."
source venv/bin/activate
echo "✓ OK - Entorno virtual activado"
echo ""

# Instalar dependencias
echo "[4/6] Instalando dependencias Python..."
echo "Esto puede tomar unos minutos..."
pip install --quiet --upgrade pip
pip install --quiet flask python-docx reportlab playwright
echo "✓ OK - Dependencias instaladas"
echo ""

# Instalar Chromium
echo "[5/6] Instalando navegador Chromium..."
echo "Esto puede tomar varios minutos..."
python -m playwright install chromium
echo "✓ OK - Chromium instalado"
echo ""

# Crear directorios necesarios
echo "[6/6] Creando estructura de directorios..."
mkdir -p uploads outputs scripts
echo "✓ OK - Directorios creados"
echo ""

# Verificar archivos necesarios
echo "Verificando archivos del proyecto..."
if [ ! -f "app.py" ]; then
    echo "⚠️  ADVERTENCIA: app.py no encontrado"
    echo "Asegúrate de estar en la carpeta correcta del proyecto"
fi
if [ ! -f "rizoma_automation.py" ]; then
    echo "⚠️  ADVERTENCIA: rizoma_automation.py no encontrado"
fi
echo ""

echo "============================================"
echo "   INSTALACIÓN COMPLETADA ✓"
echo "============================================"
echo ""
echo "Para iniciar el sistema:"
echo "  1. Abre una terminal en esta carpeta"
echo "  2. Ejecuta: source venv/bin/activate"
echo "  3. Ejecuta: python app.py"
echo "  4. Abre tu navegador en: http://localhost:5000"
echo ""
echo "Lee GUIA_COMPLETA.md para instrucciones detalladas"
echo ""
