# ❓ Preguntas Frecuentes (FAQ)

## 📑 Índice
- [General](#general)
- [Instalación](#instalación)
- [EndNote y XMLs](#endnote-y-xmls)
- [Uso del Sistema](#uso-del-sistema)
- [Automatización Rizoma](#automatización-rizoma)
- [Errores Comunes](#errores-comunes)

---

## General

### ¿Qué hace exactamente este sistema?

Automatiza 3 tareas principales:

1. **Parsea archivos XML** de EndNote con referencias bibliográficas
2. **Genera informes** de citas en formatos UNAM y SNI/SECIHTI
3. **Llena automáticamente** los formularios de Rizoma usando un navegador

**Ahorra ~13 minutos por artículo** vs llenar manualmente.

### ¿Es seguro usar este sistema?

✅ **SÍ**, porque:
- Usa tu navegador real (Chromium)
- Tus credenciales NO se guardan
- Solo interactúa con Rizoma como tú lo harías manualmente
- Todo es local en tu computadora

### ¿Necesito saber programar?

**NO**. Solo necesitas:
- Instalar el sistema (1 clic en Windows, 1 comando en Mac/Linux)
- Usar la interfaz web (como cualquier página)
- Tener tus archivos XML de EndNote listos

### ¿Funciona en mi computadora?

✅ **Windows** (7, 10, 11)  
✅ **Mac** (macOS 10.14+)  
✅ **Linux** (Ubuntu, Debian, Fedora, etc.)

Requisito único: **Python 3.8+**

### ¿Cuánto cuesta?

**Gratis**. Es software interno del BCCT/UNAM para uso académico.

---

## Instalación

### ¿Cómo instalo Python?

**Windows:**
1. Descarga desde: https://www.python.org/downloads/
2. **IMPORTANTE**: Marca "Add Python to PATH" al instalar
3. Siguiente, Siguiente, Instalar

**Mac:**
```bash
# Opción 1: Con Homebrew (recomendado)
brew install python3

# Opción 2: Desde python.org
# Descargar instalador macOS y ejecutar
```

**Linux:**
```bash
# Ubuntu/Debian
sudo apt update
sudo apt install python3 python3-pip python3-venv

# Fedora
sudo dnf install python3 python3-pip
```

### ¿Qué es un "entorno virtual"?

Es una carpeta aislada donde se instalan las dependencias del proyecto. 

**Ventajas:**
- No contamina tu sistema
- Cada proyecto tiene sus versiones
- Fácil de borrar si algo sale mal

**No te preocupes**, el instalador lo crea automáticamente.

### La instalación falló, ¿qué hago?

**Paso 1:** Identifica el error

```bash
# Ejecuta manualmente:
python --version  # ¿Funciona?
pip --version     # ¿Funciona?
```

**Paso 2:** Errores comunes

| Error | Solución |
|-------|----------|
| "python no reconocido" | No está en PATH, reinstala marcando esa opción |
| "pip no reconocido" | Instala pip: `python -m ensurepip` |
| "Permission denied" | En Linux/Mac usa: `sudo` |
| "Network error" | Problema de internet, reintenta |

**Paso 3:** Instalación manual

```bash
# Activar entorno virtual
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Instalar una por una
pip install flask
pip install python-docx
pip install reportlab
pip install playwright
python -m playwright install chromium
```

### ¿Cómo actualizo el sistema?

```bash
# Descargar nueva versión
git pull  # Si usas Git

# O reemplazar archivos manualmente

# Reinstalar dependencias por si hay nuevas
pip install --upgrade flask python-docx reportlab playwright
```

---

## EndNote y XMLs

### ¿Cómo exporto desde EndNote?

**Paso a paso:**

1. Abre tu biblioteca EndNote
2. Selecciona las referencias (citas que recibió tu artículo)
3. `File > Export`
4. Formato: **XML**
5. Guardar como: `mi_articulo.xml`

**Importante:** 
- Un XML por cada artículo tuyo
- El XML contiene las **citas que recibió** ese artículo

### ¿Qué es el campo "research-notes"?

Es un campo personalizado en EndNote para marcar el **tipo de cita**:

- **A** = Cita individual (sin coautores tuyos)
- **B** = Cita colaborativa (con coautores tuyos)
- **C** = Autocita (citando tu propio trabajo)

**Para SNI solo se usan A y B**.

### ¿Cómo configuro "research-notes" en EndNote?

1. En EndNote, abre una referencia
2. Busca el campo `Research Notes`
3. Escribe: `A`, `B`, o `C`
4. Guarda
5. Repite para cada cita

**Atajo:** Puedes editar por lotes:
- Selecciona varias referencias
- `Edit > Change/Move/Copy Fields`
- Campo: Research Notes
- Valor: A

### Mi XML no funciona, ¿por qué?

**Causas comunes:**

1. **No es formato XML de EndNote**
   - Solución: Exporta de nuevo, asegúrate de seleccionar "XML"

2. **Archivo corrupto**
   - Solución: Abre en editor de texto, verifica que diga `<?xml version`

3. **Falta el campo research-notes**
   - Solución: Agrega A, B o C a cada cita en EndNote

4. **Caracteres especiales problemáticos**
   - Solución: EndNote debería manejarlos, pero evita símbolos raros

### ¿Puedo usar otros gestores bibliográficos?

**Actualmente solo EndNote**, porque el sistema espera el formato XML específico de EndNote.

**Zotero/Mendeley:** 
- Exporta a EndNote primero
- O exporta a BibTeX y conviértelo a XML EndNote

---

## Uso del Sistema

### ¿Cómo inicio el sistema?

```bash
# 1. Abrir terminal en la carpeta del proyecto

# 2. Activar entorno virtual
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# 3. Iniciar servidor
python app.py

# 4. Abrir navegador
# http://localhost:5000
```

### ¿Puedo cerrar la terminal?

**NO mientras esté en uso**. El servidor Flask corre en la terminal.

Para detenerlo: `Ctrl + C`

### ¿Qué pasa si cierro el navegador?

Nada. El servidor sigue corriendo. Solo abre de nuevo:  
`http://localhost:5000`

### ¿Los datos se guardan?

**SÍ**, en `profiles.json`. 

**Incluye:**
- Perfiles de investigadores
- Publicaciones
- Citas cargadas

**NO incluye:**
- Credenciales de Rizoma (nunca se guardan)

### ¿Puedo tener múltiples perfiles?

**SÍ**. Útil para:
- Varios investigadores en un laboratorio
- Separar períodos de evaluación
- Pruebas vs producción

### ¿Cómo hago backup?

```bash
# Copiar profiles.json
cp profiles.json backup_profiles_2025.json

# O usar la interfaz: 
# "Exportar Perfil" (si está implementado)
```

### ¿Cómo borro un perfil?

**Opción 1:** Interfaz web (si hay botón "Eliminar")

**Opción 2:** Editar `profiles.json` manualmente
- Abre con editor de texto
- Encuentra el perfil
- Borra su sección
- Guarda

### ¿Puedo editar una publicación después de agregarla?

Depende de la versión. Revisa si hay botón "Editar".

**Alternativa:**
1. Edita `profiles.json` manualmente
2. Reinicia el servidor
3. Refresca el navegador

---

## Automatización Rizoma

### ¿Qué necesito para automatizar?

✅ Cuenta activa en Rizoma  
✅ Usuario (correo) y contraseña  
✅ Internet estable  
✅ Al menos 1 publicación agregada en el sistema  

### ¿Se guardan mis credenciales?

**NO**. Se usan solo durante la automatización y se descartan.

### ¿Puedo ver lo que hace?

**SÍ**. Se abre una ventana de Chromium donde verás todo en tiempo real:
- Login
- Navegación
- Llenado de campos
- Guardado

**También hay logs** en la interfaz web.

### ¿Puedo cancelar la automatización?

**SÍ**. Simplemente cierra la ventana de Chromium.

**Nota:** Lo que ya se guardó en Rizoma queda guardado.

### ¿Funciona en modo headless (sin ventana)?

Aún no implementado, pero se puede agregar editando:

```python
# En rizoma_automation.py
browser = await p.chromium.launch(headless=True)
```

### ¿Qué pasa si falla a la mitad?

El sistema:
1. Registra el error en logs
2. Intenta continuar con el siguiente artículo
3. Al final reporta cuántos exitosos/fallidos

**Los artículos exitosos SÍ quedan guardados en Rizoma.**

### ¿Detecta duplicados?

**NO actualmente**. 

**Recomendación:** 
- Revisa Rizoma manualmente antes
- Mantén un registro de qué ya subiste

### ¿Puedo pausar y reanudar?

No directamente. 

**Alternativa:**
- Cancela la automatización
- Elimina los artículos ya procesados de tu lista
- Reinicia solo con los pendientes

### ¿Funciona con VPN?

**Generalmente SÍ**, pero:
- Puede ser más lento
- Algunos servicios bloquean VPNs
- Si falla, intenta sin VPN

---

## Errores Comunes

### Error: "Module 'playwright' not found"

**Causa:** Playwright no instalado

**Solución:**
```bash
pip install playwright
python -m playwright install chromium
```

### Error: "Address already in use"

**Causa:** Puerto 5000 ocupado por otra aplicación

**Solución:**
```bash
# Opción 1: Cambiar puerto en app.py
# Busca: app.run(debug=True)
# Cambia a: app.run(debug=True, port=5001)

# Opción 2: Matar proceso en puerto 5000
# Windows:
netstat -ano | findstr :5000
taskkill /PID <numero> /F

# Mac/Linux:
lsof -ti:5000 | xargs kill -9
```

### Error: "Login failed"

**Causas:**
1. Credenciales incorrectas
2. Cuenta suspendida
3. Rizoma cambió su sistema de login

**Soluciones:**
1. Verifica credenciales manualmente en Rizoma
2. Contacta a Rizoma si tu cuenta tiene problemas
3. Reporta el error al equipo de desarrollo

### Error: "Selector not found"

**Causa:** Rizoma cambió el diseño de su formulario

**Solución temporal:**
1. Completa manualmente los campos que fallan
2. Reporta cuáles campos fallaron

**Solución permanente:**
1. Inspecciona el elemento en Rizoma (F12)
2. Encuentra el nuevo selector
3. Actualiza `rizoma_automation.py`

### El navegador se abre pero no hace nada

**Causas:**
- Internet muy lento
- Timeout muy corto
- Rizoma no responde

**Soluciones:**
```python
# En rizoma_automation.py, aumenta timeouts:
self.default_timeout = 10000  # 10 segundos
```

### "XMLSyntaxError" al cargar XML

**Causa:** XML mal formado

**Solución:**
1. Abre el XML en editor de texto
2. Verifica que empiece con `<?xml version="1.0"?>`
3. Verifica que esté bien cerrado `</xml>`
4. Si hay errores, exporta de nuevo desde EndNote

### Los artículos se duplican en Rizoma

**Prevención:**
- Mantén registro de lo que subes
- Revisa Rizoma antes de automatizar
- Filtra artículos ya subidos de tu lista

**Corrección:**
- Elimina duplicados manualmente en Rizoma

### "Python no reconocido como comando"

**Windows:**
1. Reinstala Python
2. ✅ Marca "Add Python to PATH"
3. Reinicia terminal

**Mac/Linux:**
```bash
# Verifica instalación
which python3

# Si no existe
sudo apt install python3  # Ubuntu/Debian
brew install python3       # Mac con Homebrew
```

---

## 🆘 Soporte

**Si tu problema no está aquí:**

1. Lee `GUIA_COMPLETA.md`
2. Revisa los logs en la interfaz web
3. Busca el error en Google
4. Contacta al equipo de desarrollo con:
   - Sistema operativo
   - Mensaje de error completo
   - Pasos para reproducir el problema

---

**Última actualización:** Abril 2026  
**Versión:** 2.1
