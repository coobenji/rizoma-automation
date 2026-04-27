# 🚀 Guía Completa: Automatización de Rizoma CONAHCYT

## 📋 Índice
1. [Instalación](#instalación)
2. [Preparación de Datos](#preparación-de-datos)
3. [Uso del Sistema](#uso-del-sistema)
4. [Automatización Rizoma](#automatización-rizoma)
5. [Solución de Problemas](#solución-de-problemas)

---

## 🔧 Instalación

### Paso 1: Requisitos Previos

- **Python 3.8+** instalado en tu sistema
- Conexión a internet
- Cuenta activa en Rizoma (https://rizoma.conahcyt.mx)

### Paso 2: Descargar el Proyecto

```bash
# Opción 1: Si tienes Git
git clone <URL_DEL_REPOSITORIO>
cd rizoma_automation

# Opción 2: Descargar ZIP y extraer
# Luego abrir terminal en la carpeta extraída
```

### Paso 3: Crear Entorno Virtual (Recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Paso 4: Instalar Dependencias

```bash
# Instalar todas las dependencias
pip install flask python-docx reportlab playwright

# Instalar navegador Chromium para automatización
python -m playwright install chromium
```

### Paso 5: Verificar Instalación

```bash
# Iniciar el servidor
python app.py

# Deberías ver algo como:
# * Running on http://127.0.0.1:5000
```

Abre tu navegador en: `http://localhost:5000`

---

## 📊 Preparación de Datos

### Paso 1: Exportar Referencias desde EndNote

Para cada artículo científico que quieras registrar en Rizoma:

1. **Abrir EndNote** y tu biblioteca de referencias
2. **Seleccionar las citas** que citaron tu artículo
3. **Exportar a XML:**
   - `File > Export`
   - Formato: `XML`
   - Guardar con nombre descriptivo: `articulo_1.xml`

#### 📌 Campo Importante: `research-notes`

En EndNote, configura el campo `Research Notes` de cada cita con:

- **A** = Cita individual (sin coautores del investigador)
- **B** = Cita colaborativa (con coautores del investigador)  
- **C** = Autocita (citando trabajo propio)

**Para SNI/SECIHTI solo se usan citas A y B**

### Paso 2: Estructura del XML de EndNote

El sistema espera archivos XML con esta estructura:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<xml>
  <records>
    <record>
      <!-- Autores -->
      <contributors>
        <authors>
          <author>Bahino, J.</author>
          <author>Dominutti, P.</author>
        </authors>
      </contributors>
      
      <!-- Títulos -->
      <titles>
        <title>Diurnal Variation and Health Risk Assessment...</title>
        <secondary-title>Aerosol and Air Quality Research</secondary-title>
      </titles>
      
      <!-- Datos de publicación -->
      <dates><year>2025</year></dates>
      <volume>25</volume>
      <number>8</number>
      <pages>123-145</pages>
      
      <!-- DOI -->
      <electronic-resource-num>10.1007/s44408-025-00049-3</electronic-resource-num>
      
      <!-- TIPO DE CITA (IMPORTANTE) -->
      <research-notes>A</research-notes>
      
      <!-- Base de datos -->
      <remote-database-name>Scopus</remote-database-name>
      
      <!-- URLs -->
      <urls>
        <related-urls>
          <url>https://www.scopus.com/inward/record.uri?...</url>
        </related-urls>
      </urls>
    </record>
  </records>
</xml>
```

---

## 🎯 Uso del Sistema

### Paso 1: Abrir la Aplicación

```bash
python app.py
```

Abre: `http://localhost:5000`

### Paso 2: Crear Perfil de Investigador

1. Clic en **"Nuevo Perfil"**
2. Llena los datos:

```
Nombre: Dr. Juan Pérez García
Institución: Universidad Nacional Autónoma de México
ORCID: 0000-0001-2345-6789
Período: 2020-2025
Fuentes: Scopus, Web of Science
```

3. Guarda el perfil

### Paso 3: Agregar Publicaciones

Por cada artículo tuyo que tiene citas:

1. Clic en **"Agregar Publicación"**
2. Llena los campos:

**Ejemplo:**
```
Referencia APA:
  Pérez, J., García, M., & López, A. (2023). 
  Advances in machine learning. 
  Nature, 25(3), 123-145. 
  https://doi.org/10.1038/nature12345

DOI: 10.1038/nature12345
Factor de Impacto: 43.070
Cuartil: Q1
ISSN Impreso: 0028-0836
ISSN Electrónico: 1476-4687
Librería EndNote: articulo_1
URL Scopus: https://www.scopus.com/record/display.uri?eid=2-s2.0-85123456789
URL Web of Science: https://www.webofscience.com/wos/woscc/full-record/WOS:000123456789
```

3. Clic en **"Agregar Publicación"**

### Paso 4: Cargar XMLs de Citas

1. Clic en **"Cargar XMLs"**
2. Selecciona tus archivos XML de EndNote:
   - `articulo_1.xml`
   - `articulo_2.xml`
   - etc.

3. El sistema automáticamente:
   - ✅ Lee cada XML
   - ✅ Extrae las citas
   - ✅ Identifica el tipo (A/B/C)
   - ✅ Las asocia con tus publicaciones

### Paso 5: Ver Vista Previa del Informe

1. Selecciona tipo de informe:
   - **UNAM**: Todas las citas (A, B, C)
   - **SNI/SECIHTI**: Solo A y B, con URLs

2. Clic en **"Vista Previa"**

3. Revisa que todo esté correcto

### Paso 6: Exportar Informe (Opcional)

- **Exportar DOCX**: Documento Word editable
- **Exportar PDF**: Documento PDF

---

## 🤖 Automatización Rizoma

### ¿Qué hace la automatización?

El sistema **automáticamente**:

1. ✅ Abre navegador Chromium
2. ✅ Inicia sesión en Rizoma
3. ✅ Navega a la sección correcta
4. ✅ Por cada artículo:
   - Clic en "Agregar"
   - Llena todos los campos del formulario
   - Guarda
5. ✅ Reporta progreso en tiempo real

### Paso a Paso

#### 1. Preparar Credenciales

Necesitas:
- Usuario de Rizoma (correo electrónico)
- Contraseña

#### 2. Iniciar Automatización

1. En la interfaz web, ve a **"Automatizar Rizoma"**
2. Ingresa credenciales:
   ```
   Usuario: mi.correo@institucion.edu.mx
   Contraseña: ********
   ```
3. Clic en **"Iniciar Automatización"**

#### 3. Observar el Proceso

Se abrirá una ventana de Chromium y verás:

```
[2025-04-23 10:30:15] Iniciando automatización...
[2025-04-23 10:30:18] ✓ Sesión iniciada exitosamente
[2025-04-23 10:30:22] ✓ Navegando a sección de artículos
[2025-04-23 10:30:25] Procesando artículo 1/3...
[2025-04-23 10:30:28] ✓ Título ingresado
[2025-04-23 10:30:30] ✓ Autores ingresados
[2025-04-23 10:30:32] ✓ DOI ingresado
...
[2025-04-23 10:31:05] ✓ Artículo 1 guardado exitosamente
[2025-04-23 10:31:08] Procesando artículo 2/3...
...
```

#### 4. Esperar Confirmación

Al finalizar verás:

```
[2025-04-23 10:35:42] ✓✓✓ AUTOMATIZACIÓN COMPLETADA ✓✓✓
[2025-04-23 10:35:42] Artículos procesados: 3/3
[2025-04-23 10:35:42] Exitosos: 3
[2025-04-23 10:35:42] Fallidos: 0
```

### Mapeo de Campos

El sistema llena automáticamente:

| Campo Rizoma | Fuente de Datos |
|--------------|-----------------|
| Título del artículo | Tu publicación registrada |
| Autor principal | Primer autor de tu artículo |
| Coautores | Otros autores |
| Revista | Tu publicación |
| Año | Tu publicación |
| Volumen | Tu publicación |
| Número | Tu publicación |
| Páginas | Tu publicación |
| DOI | Tu publicación |
| ISSN Impreso | Tu publicación |
| ISSN Electrónico | Tu publicación |
| Factor de Impacto | Tu publicación |
| Cuartil | Tu publicación |
| URL Scopus | Tu publicación |
| URL WoS | Tu publicación |
| Tipo de participación | Individual/Colaborativa (según tus datos) |

---

## 🔍 Solución de Problemas

### Problema: "Playwright no instalado"

**Solución:**
```bash
pip install playwright
python -m playwright install chromium
```

### Problema: "No se pudo iniciar sesión"

**Causas posibles:**
- ❌ Credenciales incorrectas
- ❌ Cuenta bloqueada o suspendida
- ❌ Cambió la página de login de Rizoma

**Solución:**
1. Verifica tus credenciales manualmente en Rizoma
2. Asegúrate de tener acceso activo
3. Si Rizoma cambió, reporta el problema

### Problema: "El campo X no se llena"

**Causa:** Rizoma cambió el formulario

**Solución:**
1. Abre Rizoma manualmente
2. Inspecciona el elemento (F12 > Inspector)
3. Encuentra el selector CSS correcto
4. Edita `rizoma_automation.py`:

```python
# Busca el método _llenar_formulario()
# Agrega/modifica el selector:

await self._fill_any(
    page,
    [
        "input[name='nuevo_nombre']",  # Agrega este
        "#campo_id",
        "input[placeholder*='texto']"
    ],
    valor
)
```

### Problema: "Se detiene en medio de la automatización"

**Causas:**
- Internet lento
- Timeout muy corto
- Elemento dinámico que tarda en cargar

**Solución:**
1. Mejora tu conexión
2. Aumenta los timeouts en `rizoma_automation.py`:

```python
# En __init__:
self.default_timeout = 10000  # 10 segundos en lugar de 5
```

### Problema: "Error al parsear XML"

**Causa:** XML mal formado o diferente estructura

**Solución:**
1. Abre el XML en un editor de texto
2. Verifica que tenga estructura válida
3. Asegúrate de exportar desde EndNote en formato XML correcto

### Problema: "Artículos duplicados en Rizoma"

**Prevención:**
- El sistema NO verifica duplicados automáticamente
- Revisa manualmente en Rizoma antes de ejecutar
- Mantén un registro de qué ya subiste

---

## 📝 Consejos y Mejores Prácticas

### 1. Organización de Archivos

```
mi_proyecto/
├── xml_originales/
│   ├── articulo_1.xml
│   ├── articulo_2.xml
│   └── articulo_3.xml
├── informes_generados/
│   ├── informe_sni_2025.docx
│   └── informe_unam_2025.pdf
└── profiles.json (generado automáticamente)
```

### 2. Verificación Antes de Automatizar

✅ **Checklist previo:**
- [ ] Todos los XMLs están validados
- [ ] Publicaciones tienen todos los datos completos
- [ ] Credenciales de Rizoma son correctas
- [ ] Revisé la vista previa del informe
- [ ] Verifiqué que no haya duplicados en Rizoma

### 3. Monitoreo Durante Automatización

- 👀 Observa el navegador mientras corre
- 📋 Lee los mensajes de log
- ⏸️ Si algo falla, detén y revisa
- 💾 Los datos quedan guardados hasta donde llegó

### 4. Respaldo de Datos

```bash
# Hacer backup de profiles.json periódicamente
cp profiles.json profiles_backup_$(date +%Y%m%d).json
```

---

## 🎓 Ejemplos Completos

### Ejemplo 1: Investigador con 3 Artículos

**Archivos:**
- `articulo_cancer_research.xml` (15 citas)
- `articulo_nature_medicine.xml` (23 citas)
- `articulo_lancet.xml` (8 citas)

**Proceso:**
1. Crear perfil: "Dr. Ana Martínez - UNAM"
2. Agregar 3 publicaciones con sus datos
3. Cargar los 3 XMLs
4. Generar informe SNI
5. Automatizar Rizoma → 3 artículos registrados automáticamente

**Tiempo estimado:** 15 minutos (vs 2 horas manual)

### Ejemplo 2: Actualización Anual SNI

**Escenario:** Tienes 10 nuevos artículos con citas

**Proceso:**
1. Exportar 10 XMLs desde EndNote
2. Abrir perfil existente
3. Agregar las 10 nuevas publicaciones
4. Cargar los 10 XMLs
5. Generar informe SNI actualizado
6. Automatizar Rizoma

**Tiempo estimado:** 30 minutos (vs 5 horas manual)

---

## 🆘 Soporte y Contacto

**Si encuentras un problema:**

1. 📖 Consulta esta guía
2. 🔍 Revisa "Solución de Problemas"
3. 📊 Revisa los logs del sistema
4. 📧 Contacta al equipo de desarrollo

**Información útil para reportar bugs:**

```
Sistema Operativo: Windows 11 / macOS 14 / Ubuntu 22.04
Versión de Python: python --version
Versión de Playwright: pip show playwright
Navegador: Chromium (automático)
Mensaje de error: [copiar mensaje completo]
Archivo XML problemático: [adjuntar si es posible]
```

---

## 📚 Recursos Adicionales

- [Documentación de EndNote](https://endnote.com/support/)
- [Guía oficial de Rizoma](https://rizoma.conahcyt.mx/ayuda)
- [Playwright Python Docs](https://playwright.dev/python/)

---

## ✅ Checklist de Inicio Rápido

**Primera vez usando el sistema:**

- [ ] Python 3.8+ instalado
- [ ] Entorno virtual creado y activado
- [ ] Dependencias instaladas (`pip install ...`)
- [ ] Playwright y Chromium instalados
- [ ] Servidor Flask corriendo (`python app.py`)
- [ ] Perfil de investigador creado
- [ ] Primera publicación agregada
- [ ] Primer XML cargado exitosamente
- [ ] Vista previa del informe generada
- [ ] Credenciales de Rizoma listas
- [ ] Primera automatización ejecutada

---

**¡Listo! Ya puedes automatizar tus registros en Rizoma 🎉**

**Última actualización**: Abril 2026  
**Versión**: 2.1  
**Soporte**: BCCT/UNAM
