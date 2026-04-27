# 🎓 Sistema de Automatización Rizoma (CONAHCYT)

Sistema completo para automatizar el registro de artículos científicos en la plataforma Rizoma del Sistema Nacional de Investigadores (SNI/SECIHTI).

## 🌟 Características Principales

- ✅ **Importación Automática**: Lee archivos XML de EndNote sin intervención manual
- ✅ **Clasificación Inteligente**: Identifica automáticamente citas tipo A, B y C
- ✅ **Generación de Informes**: Formatos UNAM (todos los tipos) y SNI (solo A+B)
- ✅ **Exportación Múltiple**: DOCX y PDF con formato profesional
- ✅ **Automatización Completa**: Registro automático en Rizoma con Playwright
- ✅ **Interfaz Web Moderna**: Dashboard intuitivo y responsivo
- ✅ **Monitoreo en Tiempo Real**: Seguimiento del progreso de automatización

## 🚀 Instalación Rápida

### Windows

\\\powershell
# 1. Clonar repositorio
git clone https://github.com/coobenji/rizoma-automation.git

# 2. Navegar al proyecto
cd rizoma-automation

# 3. Crear entorno virtual
python -m venv venv

# 4. Activar entorno virtual
venv\Scripts\activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Instalar navegador Chromium
python -m playwright install chromium

# 7. Ejecutar aplicación
python app.py
\\\

### Mac/Linux

\\\ash
# 1. Clonar repositorio
git clone https://github.com/coobenji/rizoma-automation.git

# 2. Navegar al proyecto
cd rizoma-automation

# 3. Crear entorno virtual
python3 -m venv venv

# 4. Activar entorno virtual
source venv/bin/activate

# 5. Instalar dependencias
pip install -r requirements.txt

# 6. Instalar navegador Chromium
python -m playwright install chromium

# 7. Ejecutar aplicación
python app.py
\\\

## 💻 Uso

1. Ejecuta \python app.py\
2. Abre tu navegador en \http://localhost:5000\
3. Crea un perfil de investigador
4. Agrega tus publicaciones con sus metadatos
5. Carga los archivos XML exportados desde EndNote
6. Genera informes o automatiza el registro en Rizoma

## 📊 Flujo de Trabajo

\\\
EndNote (XML) → Importación → Clasificación → Informe → Rizoma
     ↓              ↓              ↓            ↓         ↓
  Export      Parse XML      A/B/C Type    DOCX/PDF   Auto-fill
\\\

## 📚 Documentación Completa

- **GUIA_COMPLETA.md**: Documentación técnica completa
- **TUTORIAL_RAPIDO.md**: Tutorial paso a paso para usuarios
- **FAQ.md**: Preguntas frecuentes y solución de problemas

## 🛠️ Tecnologías Utilizadas

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| Python | 3.9+ | Lenguaje principal |
| Flask | 3.0.0 | Framework web |
| Playwright | 1.40.0 | Automatización de navegador |
| python-docx | 1.1.0 | Generación de documentos Word |
| reportlab | 4.0.7 | Generación de PDFs |

## 📁 Estructura del Proyecto

\\\
rizoma-automation/
│
├── app.py                      # Aplicación Flask principal
├── rizoma_automation.py        # Motor de automatización
├── requirements.txt            # Dependencias de Python
├── README.md                   # Este archivo
├── .gitignore                  # Archivos a ignorar
│
├── GUIA_COMPLETA.md           # Documentación técnica
├── TUTORIAL_RAPIDO.md         # Tutorial de usuario
├── FAQ.md                      # Preguntas frecuentes
│
├── uploads/                    # XMLs cargados (gitignored)
├── outputs/                    # Informes generados (gitignored)
└── venv/                       # Entorno virtual (gitignored)
\\\

## ⚙️ Configuración

### Ubicación Recomendada (Windows)

\\\
C:\Users\TU_USUARIO\Documents\Rizoma
\\\

### Archivos XML de EndNote

Los archivos XML deben tener el campo \esearch-notes\ configurado:
- **Vacío o "A"**: Publicación Individual
- **"B"**: Publicación Colaborativa
- **"C"**: Autocita

El nombre del archivo XML debe coincidir con el campo "Librería EndNote" en la publicación.

### Credenciales de Rizoma

Las credenciales se solicitan al momento de ejecutar la automatización y **no se almacenan en disco**.

## 🎯 Casos de Uso

### Investigador Individual
- **Tiempo manual**: 6-8 horas
- **Tiempo automatizado**: 15-20 minutos
- **Ahorro**: ~90%

### Equipo de Investigación (10 personas)
- **Tiempo manual**: 60-80 horas
- **Tiempo automatizado**: 3-4 horas
- **Ahorro**: 75+ horas

## 🔒 Seguridad y Privacidad

- ✅ Todos los datos se almacenan localmente
- ✅ No se envía información a servidores externos
- ✅ Credenciales no se guardan en disco
- ✅ Archivos sensibles excluidos del repositorio (.gitignore)

## 🐛 Solución de Problemas

### Error: "No module named 'playwright'"

\\\powershell
pip install playwright
python -m playwright install chromium
\\\

### Error: "No se puede conectar a Rizoma"

- Verifica tu conexión a internet
- Comprueba que tus credenciales sean correctas
- Asegúrate de que Rizoma esté disponible

### Los XMLs no se cargan

- Verifica que sean archivos XML válidos de EndNote
- Asegúrate de que el nombre del archivo coincida con "Librería EndNote"
- Revisa que tengan el campo \esearch-notes\ configurado

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (\git checkout -b feature/NuevaCaracteristica\)
3. Commit tus cambios (\git commit -m 'Agregar nueva característica'\)
4. Push a la rama (\git push origin feature/NuevaCaracteristica\)
5. Abre un Pull Request

## 📝 Changelog

### v1.0.0 (2026-04-27)
- ✅ Versión inicial
- ✅ Importación de XMLs de EndNote
- ✅ Clasificación automática de citas
- ✅ Generación de informes UNAM y SNI
- ✅ Automatización completa de Rizoma
- ✅ Interfaz web con Flask

## 📄 Licencia

Proyecto académico desarrollado para BCCT/UNAM.

## 👥 Autor

**Benjamín** - [@coobenji](https://github.com/coobenji)

Desarrollado para el Laboratorio de Ciencias - BCCT/UNAM

## 🙏 Agradecimientos

- **CONAHCYT** por la plataforma Rizoma
- **Playwright** por el framework de automatización
- **Comunidad de Python** por las herramientas y librerías

## 📞 Soporte

¿Problemas o preguntas? 

- 📧 Abre un [issue](https://github.com/coobenji/rizoma-automation/issues)
- 📖 Consulta la [documentación completa](GUIA_COMPLETA.md)
- ❓ Revisa las [preguntas frecuentes](FAQ.md)

---

**⭐ Si este proyecto te fue útil, considera darle una estrella!**

**🔗 Repositorio**: https://github.com/coobenji/rizoma-automation
