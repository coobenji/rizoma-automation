# 🎯 Tutorial Rápido - 5 Minutos

## ¿Qué hace este sistema?

Automatiza el registro de artículos científicos en Rizoma (CONAHCYT):

```
Archivos XML (EndNote)  →  Sistema  →  Rizoma completado ✓
     ⏱️ 2 horas manual            ⏱️ 10 minutos automático
```

---

## 🚀 Inicio en 3 Pasos

### Paso 1: Instalar (una sola vez)

**Windows:**
```bash
# Doble clic en:
instalar_windows.bat
```

**Mac/Linux:**
```bash
chmod +x instalar_mac_linux.sh
./instalar_mac_linux.sh
```

### Paso 2: Iniciar el Sistema

```bash
# Activar entorno virtual
# Windows:
venv\Scripts\activate

# Mac/Linux:
source venv/bin/activate

# Iniciar servidor
python app.py
```

Abre: `http://localhost:5000`

### Paso 3: Usar

1. **Crear Perfil** → Tus datos
2. **Agregar Publicación** → Tu artículo con citas
3. **Cargar XML** → Tu archivo de EndNote
4. **Automatizar Rizoma** → ¡Listo!

---

## 📊 Flujo Visual

```
┌─────────────────────────────────────────────────────────┐
│  1. PREPARAR EN ENDNOTE                                 │
│                                                          │
│  Artículo 1 con sus citas → articulo_1.xml             │
│  Artículo 2 con sus citas → articulo_2.xml             │
│  Artículo 3 con sus citas → articulo_3.xml             │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  2. CONFIGURAR EN EL SISTEMA WEB                        │
│                                                          │
│  Perfil Investigador                                    │
│  ├─ Nombre: Dr. Juan Pérez                              │
│  ├─ Institución: UNAM                                   │
│  └─ ORCID: 0000-0001-xxxx                               │
│                                                          │
│  Publicaciones                                          │
│  ├─ Artículo 1: Nature 2023 (DOI, FI, Q1...)          │
│  ├─ Artículo 2: Science 2024 (DOI, FI, Q1...)         │
│  └─ Artículo 3: Cell 2025 (DOI, FI, Q1...)            │
│                                                          │
│  Cargar XMLs                                            │
│  └─ articulo_1.xml, articulo_2.xml, articulo_3.xml     │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  3. AUTOMATIZAR RIZOMA                                  │
│                                                          │
│  [Ingresar credenciales Rizoma]                         │
│  [Clic en "Iniciar Automatización"]                     │
│                                                          │
│  🤖 El sistema automáticamente:                          │
│  ✓ Inicia sesión                                        │
│  ✓ Navega a la sección correcta                        │
│  ✓ Llena formulario de Artículo 1 → Guarda            │
│  ✓ Llena formulario de Artículo 2 → Guarda            │
│  ✓ Llena formulario de Artículo 3 → Guarda            │
└─────────────────────────────────────────────────────────┘
                        ↓
┌─────────────────────────────────────────────────────────┐
│  ✅ COMPLETADO                                          │
│                                                          │
│  3 artículos registrados en Rizoma                      │
│  Tiempo total: ~10 minutos                              │
│  Tiempo ahorrado: ~110 minutos                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎬 Ejemplo Práctico Completo

### Escenario
Investigadora con 2 artículos publicados que han recibido citas

### Archivos EndNote
```
cancer_research_2023.xml  →  12 citas (8 tipo A, 4 tipo B)
nature_medicine_2024.xml  →  7 citas (5 tipo A, 2 tipo B)
```

### Paso a Paso

#### 1. Abrir Sistema
```bash
python app.py
# Abre http://localhost:5000
```

#### 2. Crear Perfil
```
Nombre: Dra. María López González
Institución: Instituto Nacional de Cancerología
ORCID: 0000-0002-1234-5678
Período evaluación: 2023-2025
Fuentes: Scopus, Web of Science
```

#### 3. Agregar Primera Publicación
```
Referencia APA:
  López, M., García, J., & Pérez, A. (2023). 
  Novel approaches in cancer treatment. 
  Cancer Research, 83(5), 1234-1245. 
  https://doi.org/10.1158/0008-5472.CAN-23-1234

DOI: 10.1158/0008-5472.CAN-23-1234
Factor de Impacto: 11.2
Cuartil: Q1
ISSN Impreso: 0008-5472
ISSN Electrónico: 1538-7445
Librería EndNote: cancer_research_2023

URL Scopus: 
https://www.scopus.com/record/display.uri?eid=2-s2.0-85123456789

URL Web of Science:
https://www.webofscience.com/wos/woscc/full-record/WOS:000123456789
```

#### 4. Agregar Segunda Publicación
```
Referencia APA:
  López, M., & Martínez, L. (2024). 
  Immunotherapy advances. 
  Nature Medicine, 30(2), 456-467. 
  https://doi.org/10.1038/s41591-024-1234-5

DOI: 10.1038/s41591-024-1234-5
Factor de Impacto: 58.7
Cuartil: Q1
ISSN Impreso: 1078-8956
ISSN Electrónico: 1546-170X
Librería EndNote: nature_medicine_2024

URL Scopus:
https://www.scopus.com/record/display.uri?eid=2-s2.0-85234567890

URL Web of Science:
https://www.webofscience.com/wos/woscc/full-record/WOS:000234567890
```

#### 5. Cargar XMLs
```
Seleccionar archivos:
  ☑ cancer_research_2023.xml
  ☑ nature_medicine_2024.xml

[Cargar XMLs]

Resultado:
  ✓ Procesados: 2 archivos
  ✓ Citas encontradas: 19 total
    - Artículo 1: 12 citas (8A + 4B)
    - Artículo 2: 7 citas (5A + 2B)
```

#### 6. Vista Previa Informe SNI
```
Clic en [Vista Previa - Informe SNI]

Se muestra:
  📄 INFORME DE CITAS PARA SNI/SECIHTI
  
  Investigadora: Dra. María López González
  Período: 2023-2025
  Total artículos: 2
  Total citas: 19 (13 tipo A, 6 tipo B)
  
  ARTÍCULO 1
  López, M., García, J., & Pérez, A. (2023)...
  Factor de Impacto: 11.2 | Cuartil: Q1
  Citas: 12 (8A + 4B)
  
  [Listado detallado de las 12 citas...]
  
  ARTÍCULO 2
  López, M., & Martínez, L. (2024)...
  Factor de Impacto: 58.7 | Cuartil: Q1
  Citas: 7 (5A + 2B)
  
  [Listado detallado de las 7 citas...]
```

#### 7. Automatizar Rizoma
```
[Automatizar Rizoma (SNI)]

Credenciales Rizoma:
  Usuario: maria.lopez@incan.edu.mx
  Contraseña: ********

[Iniciar Automatización]

🤖 Iniciando... Se abre Chromium

Log en pantalla:
  [10:15:23] ✓ Iniciando sesión en Rizoma...
  [10:15:28] ✓ Sesión iniciada correctamente
  [10:15:32] ✓ Navegando a sección Artículos...
  
  [10:15:35] Procesando artículo 1/2
  [10:15:38] ✓ Título ingresado
  [10:15:40] ✓ Autores ingresados
  [10:15:42] ✓ Revista ingresada
  [10:15:44] ✓ Datos bibliográficos ingresados
  [10:15:46] ✓ DOI ingresado
  [10:15:48] ✓ ISSN ingresado
  [10:15:50] ✓ Factor de Impacto y Cuartil ingresados
  [10:15:52] ✓ URLs de bases de datos ingresadas
  [10:15:55] ✓ Artículo 1 GUARDADO
  
  [10:15:58] Procesando artículo 2/2
  [10:16:01] ✓ Título ingresado
  ...
  [10:16:25] ✓ Artículo 2 GUARDADO
  
  [10:16:28] ✅✅✅ AUTOMATIZACIÓN COMPLETADA ✅✅✅
  [10:16:28] Artículos procesados: 2/2
  [10:16:28] Exitosos: 2
  [10:16:28] Fallidos: 0
  [10:16:28] Tiempo total: 1 minuto 5 segundos
```

#### 8. Verificar en Rizoma
```
Entrar manualmente a Rizoma
→ Trayectoria Profesional
→ Producción
→ Humanista y Científica
→ Artículos

✓ Ver los 2 artículos registrados correctamente
✓ Todos los campos llenos
✓ URLs funcionando
```

---

## ⏱️ Comparación de Tiempos

| Tarea | Manual | Automático | Ahorro |
|-------|--------|------------|--------|
| Crear perfil | 5 min | 5 min | 0 |
| Registrar 1 artículo | 15 min | 2 min | 13 min |
| Registrar 10 artículos | 150 min | 20 min | 130 min |
| Generar informe | 30 min | 2 min | 28 min |
| **TOTAL (10 artículos)** | **~3 horas** | **~30 min** | **~2.5 horas** |

---

## 📋 Checklist Antes de Iniciar

**Primera vez:**
- [ ] Python instalado
- [ ] Ejecuté el instalador
- [ ] Servidor corriendo (`python app.py`)
- [ ] Puedo abrir http://localhost:5000

**Para automatizar:**
- [ ] Exporté mis XMLs desde EndNote
- [ ] Configuré campo `research-notes` (A/B/C)
- [ ] Creé mi perfil en el sistema
- [ ] Agregué todas mis publicaciones
- [ ] Cargué todos los XMLs
- [ ] Verifiqué la vista previa
- [ ] Tengo credenciales de Rizoma listas
- [ ] No hay artículos duplicados en Rizoma

---

## 🆘 Problemas Comunes - Solución Rápida

### "No puedo instalar Playwright"
```bash
pip install --upgrade pip
pip install playwright
python -m playwright install chromium
```

### "El servidor no inicia"
```bash
# Verifica que estás en la carpeta correcta
ls app.py  # Debe existir

# Activa el entorno virtual
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate      # Windows

# Inicia
python app.py
```

### "La automatización no inicia sesión"
- ✓ Verifica usuario/contraseña en Rizoma
- ✓ Asegúrate de tener cuenta activa
- ✓ Prueba login manual primero

### "No se llena un campo"
- ✓ Rizoma puede haber cambiado el formulario
- ✓ Reporta el problema
- ✓ Por ahora, llena ese campo manualmente

---

## 🎯 Próximos Pasos

**Ya dominas lo básico, ahora puedes:**

1. Exportar informes en DOCX/PDF
2. Manejar múltiples perfiles de investigadores
3. Generar reportes UNAM y SNI
4. Personalizar el sistema para tus necesidades

**Lee la guía completa:** `GUIA_COMPLETA.md`

---

**¡Felicidades! Ya puedes automatizar Rizoma** 🎉

Tiempo invertido aprendiendo: 5 minutos  
Tiempo ahorrado por artículo: 13 minutos  
ROI después de 1 artículo: ¡POSITIVO! ✅
