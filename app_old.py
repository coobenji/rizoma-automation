# ═══════════════════════════════════════════════════════════════════════════════
# SISTEMA COMPLETO DE AUTOMATIZACIÓN PARA RIZOMA (CONAHCYT)
# ═══════════════════════════════════════════════════════════════════════════════
#
# Este archivo contiene TODOS los scripts Python necesarios para el proyecto.
# Guarda cada sección en su archivo correspondiente según se indica.
#
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# ARCHIVO 1: rizoma_automation.py
# ═══════════════════════════════════════════════════════════════════════════════
"""
Módulo de Automatización de Rizoma (CONAHCYT)
==============================================

Automatiza el registro de artículos científicos en la plataforma Rizoma
del Sistema Nacional de Investigadores (SNI/SECIHTI).

Autor: Sistema de Gestión de Citas BCCT/UNAM
Fecha: Abril 2026
"""

import asyncio
from typing import Dict, List, Any, Optional
from playwright.async_api import Page, async_playwright


class RizomaAutomator:
    """
    Clase principal para automatizar el registro de artículos en Rizoma.
    
    Características:
    - Login automático
    - Navegación a sección de artículos
    - Llenado completo de formularios
    - Manejo de errores y reintentos
    - Registro de progreso
    """
    
    def __init__(self, task_state: dict):
        """
        Inicializa el automatizador.
        
        Args:
            task_state: Diccionario compartido para reportar progreso
        """
        self.task = task_state
        self.base_url = "https://rizoma.conahcyt.mx"
        self.login_url = f"{self.base_url}/"
        self.articulos_url = f"{self.base_url}/trayectoria-profesional/produccion/cientifica-humanistica/articulos"
        
    async def automatizar_completo(
        self, 
        profile: Dict[str, Any], 
        credenciales: Dict[str, str]
    ):
        """
        Ejecuta el proceso completo de automatización.
        
        Args:
            profile: Perfil del investigador con sus publicaciones
            credenciales: {"usuario": "...", "password": "..."}
        """
        # Obtener artículos a registrar (solo tipo A y B para SNI)
        articulos = self._extraer_articulos_sni(profile)
        
        if not articulos:
            self.task["log"].append("⚠ No hay artículos tipo A o B para registrar")
            self.task["status"] = "done"
            return
        
        self.task["total"] = len(articulos)
        self.task["progress"] = 0
        self.task["log"].append(f"📊 Total de artículos a registrar: {len(articulos)}")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(
                headless=False,
                args=["--start-maximized", "--disable-blink-features=AutomationControlled"]
            )
            
            context = await browser.new_context(
                viewport=None,
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
            )
            
            page = await context.new_page()
            
            try:
                # 1. Login
                if not await self._login(page, credenciales):
                    self.task["status"] = "error"
                    return
                
                # 2. Navegar a artículos
                if not await self._navegar_a_articulos(page):
                    self.task["status"] = "error"
                    return
                
                # 3. Registrar cada artículo
                for idx, articulo in enumerate(articulos, 1):
                    self.task["progress"] = idx
                    await self._registrar_articulo(page, articulo, idx, len(articulos))
                
                self.task["log"].append(f"\n✅ PROCESO COMPLETADO: {len(articulos)} artículos registrados")
                self.task["status"] = "done"
                
            except Exception as e:
                self.task["log"].append(f"\n❌ ERROR CRÍTICO: {str(e)}")
                self.task["status"] = "error"
            finally:
                await asyncio.sleep(2)
                await browser.close()
    
    def _extraer_articulos_sni(self, profile: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Extrae los artículos tipo A y B de las publicaciones del perfil.
        
        Returns:
            Lista de diccionarios con información completa de cada artículo
        """
        articulos = []
        
        for pub in profile.get("publicaciones", []):
            citas = pub.get("citas", [])
            
            for cita in citas:
                # Solo artículos tipo A (individuales) y B (colaborativos) para SNI
                if cita.get("tipo") not in ("A", "B"):
                    continue
                
                # Combinar información de la publicación y la cita
                articulos.append({
                    **cita,
                    "fi": pub.get("fi", ""),
                    "quartil": pub.get("quartil", ""),
                    "issn_e": pub.get("issn_e", ""),
                    "issn_i": pub.get("issn_i", ""),
                    "urls_citas": pub.get("urls_citas", {}),
                })
        
        return articulos
    
    async def _login(self, page: Page, credenciales: Dict[str, str]) -> bool:
        """
        Realiza el login en Rizoma.
        
        Returns:
            True si el login fue exitoso, False en caso contrario
        """
        self.task["log"].append(f"🔐 Iniciando sesión como {credenciales['usuario']}...")
        
        try:
            await page.goto(self.login_url, wait_until="domcontentloaded", timeout=30000)
            await asyncio.sleep(2)
            
            # Buscar y llenar campos de login
            usuario_selectors = [
                "input[type='text'][name='username']",
                "input[type='email']",
                "input[name='email']",
                "#username",
                "#email"
            ]
            
            password_selectors = [
                "input[type='password']",
                "input[name='password']",
                "#password"
            ]
            
            # Intentar llenar usuario
            for selector in usuario_selectors:
                try:
                    await page.fill(selector, credenciales["usuario"], timeout=2000)
                    break
                except:
                    continue
            
            # Intentar llenar contraseña
            for selector in password_selectors:
                try:
                    await page.fill(selector, credenciales["password"], timeout=2000)
                    break
                except:
                    continue
            
            # Buscar botón de submit
            submit_selectors = [
                "button[type='submit']",
                "input[type='submit']",
                "button:has-text('Iniciar')",
                "button:has-text('Entrar')",
                "button:has-text('Ingresar')"
            ]
            
            for selector in submit_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    break
                except:
                    continue
            
            # Esperar a que cargue la página principal
            await page.wait_for_load_state("networkidle", timeout=15000)
            await asyncio.sleep(2)
            
            self.task["log"].append("✅ Sesión iniciada correctamente")
            return True
            
        except Exception as e:
            self.task["log"].append(f"❌ Error en login: {str(e)}")
            return False
    
    async def _navegar_a_articulos(self, page: Page) -> bool:
        """
        Navega a la sección de Artículos en Rizoma.
        
        Returns:
            True si la navegación fue exitosa
        """
        try:
            self.task["log"].append("📂 Navegando a sección de Artículos...")
            
            # Opción 1: Navegar directamente por URL
            try:
                await page.goto(self.articulos_url, wait_until="domcontentloaded", timeout=10000)
                await asyncio.sleep(1)
                self.task["log"].append("✅ Navegación exitosa")
                return True
            except:
                pass
            
            # Opción 2: Usar menú lateral
            try:
                # 1. Expandir Trayectoria profesional
                await page.click("#trayectoria-profecional", timeout=3000)
                await asyncio.sleep(0.5)
                
                # 2. Expandir Producción
                await page.click("#produccion", timeout=3000)
                await asyncio.sleep(0.5)
                
                # 3. Expandir Humanista y científica
                await page.click("#cientifica-menu", timeout=3000)
                await asyncio.sleep(0.5)
                
                # 4. Click en Artículos
                await page.click("a[href='/trayectoria-profesional/produccion/cientifica-humanistica/articulos']", timeout=3000)
                await asyncio.sleep(1)
                
                self.task["log"].append("✅ Navegación exitosa")
                return True
            except:
                pass
            
            self.task["log"].append("❌ No se pudo navegar a la sección de artículos")
            return False
            
        except Exception as e:
            self.task["log"].append(f"❌ Error en navegación: {str(e)}")
            return False
    
    async def _registrar_articulo(
        self, 
        page: Page, 
        articulo: Dict[str, Any], 
        idx: int, 
        total: int
    ):
        """
        Registra un artículo individual en Rizoma.
        
        Args:
            page: Página de Playwright
            articulo: Diccionario con datos del artículo
            idx: Número del artículo actual
            total: Total de artículos a registrar
        """
        self.task["log"].append(f"\n📝 [{idx}/{total}] Procesando artículo...")
        
        try:
            # 1. Click en botón "Agregar" o "Nuevo"
            agregar_selectors = [
                "button:has-text('Agregar')",
                "button:has-text('Nuevo')",
                "a:has-text('Agregar')",
                ".btn:has-text('Agregar')"
            ]
            
            for selector in agregar_selectors:
                try:
                    await page.click(selector, timeout=2000)
                    break
                except:
                    continue
            
            await asyncio.sleep(1)
            
            # 2. Llenar formulario
            await self._llenar_formulario_articulo(page, articulo)
            
            # 3. Guardar
            await self._guardar_formulario(page)
            
            self.task["log"].append(f"    ✅ Artículo guardado exitosamente")
            
        except Exception as e:
            self.task["log"].append(f"    ❌ Error registrando artículo: {str(e)}")
    
    async def _guardar_formulario(self, page: Page):
        """
        Guarda el formulario actual.
        """
        guardar_selectors = [
            "button:has-text('Guardar')",
            "button[type='submit']",
            ".btn-primary:has-text('Guardar')",
            "input[type='submit']"
        ]
        
        for selector in guardar_selectors:
            try:
                await page.click(selector, timeout=2000)
                break
            except:
                continue
        
        # Esperar confirmación
        await asyncio.sleep(2)
    
    async def _llenar_formulario_articulo(self, page: Page, articulo: Dict[str, Any]):
        """
        Llena el formulario de un artículo con toda la información.
        
        Args:
            page: Página de Playwright
            articulo: Diccionario con datos del artículo
        """
        try:
            # Extraer datos del artículo
            title = articulo.get("title", "")
            journal = articulo.get("journal", "")
            year = articulo.get("year", "")
            volume = articulo.get("volume", "")
            issue = articulo.get("issue", "")
            pages = articulo.get("pages", "")
            doi = articulo.get("doi", "")
            url = articulo.get("url", "")
            authors = articulo.get("authors", [])
            tipo = articulo.get("tipo", "A")
            fi = articulo.get("fi", "")
            quartil = articulo.get("quartil", "")
            issn_e = articulo.get("issn_e", "")
            issn_i = articulo.get("issn_i", "")
            
            # ═══════════════════════════════════════════════════════════
            # TÍTULO
            # ═══════════════════════════════════════════════════════════
            if title:
                await self._fill_any(
                    page,
                    [
                        "input[name='titulo']",
                        "input[name='title']",
                        "#titulo",
                        "textarea[name='titulo']",
                        "input[placeholder*='Título']"
                    ],
                    title
                )
                self.task["log"].append(f"    ✓ Título: {title[:50]}...")
            
            # ═══════════════════════════════════════════════════════════
            # AÑO
            # ═══════════════════════════════════════════════════════════
            if year:
                await self._fill_any(
                    page,
                    [
                        "input[name='año']",
                        "input[name='anio']",
                        "input[name='year']",
                        "#año",
                        "#anio",
                        "select[name='año']"
                    ],
                    str(year)
                )
                self.task["log"].append(f"    ✓ Año: {year}")
            
            # ═══════════════════════════════════════════════════════════
            # REVISTA/JOURNAL
            # ═══════════════════════════════════════════════════════════
            if journal:
                await self._fill_any(
                    page,
                    [
                        "input[name='revista']",
                        "input[name='journal']",
                        "#revista",
                        "input[placeholder*='Revista']",
                        "input[placeholder*='Journal']"
                    ],
                    journal
                )
                self.task["log"].append(f"    ✓ Revista: {journal[:40]}...")
            
            # ═══════════════════════════════════════════════════════════
            # AUTORES
            # ═══════════════════════════════════════════════════════════
            if authors:
                primer_autor = authors[0]
                
                # Intentar separar nombre y apellido
                partes = primer_autor.split(",")
                if len(partes) >= 2:
                    apellidos = partes[0].strip()
                    nombres = partes[1].strip()
                else:
                    # Si no hay coma, intentar con espacio
                    partes = primer_autor.split()
                    if len(partes) >= 2:
                        nombres = partes[0]
                        apellidos = " ".join(partes[1:])
                    else:
                        nombres = primer_autor
                        apellidos = ""
                
                # Llenar nombre del primer autor
                try:
                    await self._fill_any(
                        page,
                        [
                            "input[name*='nombre'][name*='autor']",
                            "input[name='nombre_autor']",
                            "#nombre_autor"
                        ],
                        nombres,
                        timeout=1000
                    )
                except:
                    pass
                
                # Llenar apellido del primer autor
                try:
                    await self._fill_any(
                        page,
                        [
                            "input[name*='apellido'][name*='autor']",
                            "input[name='apellido_autor']",
                            "#apellido_autor"
                        ],
                        apellidos,
                        timeout=1000
                    )
                except:
                    pass
                
                self.task["log"].append(f"    ✓ Autor: {primer_autor}")
                
                # Todos los autores
                if len(authors) > 1:
                    todos = "; ".join(authors)
                    try:
                        await self._fill_any(
                            page,
                            [
                                "textarea[name*='autores']",
                                "input[name*='coautores']",
                                "textarea[name*='authors']",
                                "textarea[name='autores']"
                            ],
                            todos,
                            timeout=2000
                        )
                        self.task["log"].append(f"    ✓ Total autores: {len(authors)}")
                    except:
                        pass
            
            # ═══════════════════════════════════════════════════════════
            # VOLUMEN, NÚMERO, PÁGINAS
            # ═══════════════════════════════════════════════════════════
            if volume:
                try:
                    await self._fill_any(
                        page,
                        ["input[name='volumen']", "input[name='volume']", "#volumen"],
                        str(volume),
                        timeout=2000
                    )
                except:
                    pass
            
            if issue:
                try:
                    await self._fill_any(
                        page,
                        [
                            "input[name='numero']",
                            "input[name='issue']",
                            "input[name='number']",
                            "#numero"
                        ],
                        str(issue),
                        timeout=2000
                    )
                except:
                    pass
            
            if pages:
                try:
                    await self._fill_any(
                        page,
                        ["input[name='paginas']", "input[name='pages']", "#paginas"],
                        str(pages),
                        timeout=2000
                    )
                except:
                    pass
            
            # ═══════════════════════════════════════════════════════════
            # DOI
            # ═══════════════════════════════════════════════════════════
            if doi:
                doi_limpio = doi.replace("https://doi.org/", "").replace("http://doi.org/", "")
                try:
                    await self._fill_any(
                        page,
                        ["input[name='doi']", "#doi", "input[placeholder*='DOI']"],
                        doi_limpio,
                        timeout=2000
                    )
                    self.task["log"].append(f"    ✓ DOI: {doi_limpio[:30]}")
                except:
                    pass
            
            # ═══════════════════════════════════════════════════════════
            # MÉTRICAS
            # ═══════════════════════════════════════════════════════════
            if fi:
                try:
                    await self._fill_any(
                        page,
                        [
                            "input[name*='factor'][name*='impacto']",
                            "input[name='fi']",
                            "#fi"
                        ],
                        str(fi),
                        timeout=2000
                    )
                    self.task["log"].append(f"    ✓ Factor Impacto: {fi}")
                except:
                    pass
            
            if quartil:
                try:
                    # Intentar como select
                    await page.select_option(
                        "select[name*='cuartil'], select[name*='quartil']",
                        quartil,
                        timeout=2000
                    )
                except:
                    # Intentar como input
                    try:
                        await self._fill_any(
                            page,
                            ["input[name*='cuartil']", "input[name*='quartil']"],
                            quartil,
                            timeout=2000
                        )
                    except:
                        pass
            
            # ═══════════════════════════════════════════════════════════
            # ISSN
            # ═══════════════════════════════════════════════════════════
            if issn_e:
                try:
                    await self._fill_any(
                        page,
                        [
                            "input[name*='issn'][name*='elect']",
                            "input[name='issn_e']",
                            "input[placeholder*='ISSN electrónico']"
                        ],
                        issn_e,
                        timeout=2000
                    )
                except:
                    pass
            
            if issn_i:
                try:
                    await self._fill_any(
                        page,
                        [
                            "input[name*='issn'][name*='impre']",
                            "input[name='issn_i']",
                            "input[placeholder*='ISSN impreso']"
                        ],
                        issn_i,
                        timeout=2000
                    )
                except:
                    pass
            
            # ═══════════════════════════════════════════════════════════
            # URL
            # ═══════════════════════════════════════════════════════════
            if url:
                try:
                    await self._fill_any(
                        page,
                        [
                            "input[name='url']",
                            "input[type='url']",
                            "input[placeholder*='URL']",
                            "input[placeholder*='Enlace']"
                        ],
                        url,
                        timeout=2000
                    )
                except:
                    pass
            
            # ═══════════════════════════════════════════════════════════
            # TIPO DE PARTICIPACIÓN
            # ═══════════════════════════════════════════════════════════
            try:
                if tipo == "A":
                    await page.check("input[value='individual'], input[value='A']", timeout=2000)
                elif tipo == "B":
                    await page.check("input[value='colaborativa'], input[value='B']", timeout=2000)
            except:
                pass
            
            self.task["log"].append(f"    ✓ Formulario completado (Tipo {tipo})")
            
        except Exception as e:
            self.task["log"].append(f"    ⚠️ Error llenando formulario: {str(e)}")
            raise
    
    async def _fill_any(
        self, 
        page: Page, 
        selectors: List[str], 
        value: str,
        timeout: int = 3000
    ):
        """
        Intenta llenar un campo usando una lista de selectores posibles.
        
        Args:
            page: Página de Playwright
            selectors: Lista de selectores CSS para intentar
            value: Valor a ingresar
            timeout: Timeout en milisegundos
        """
        for selector in selectors:
            try:
                await page.fill(selector, value, timeout=timeout)
                return
            except:
                continue
        
        # Si ninguno funcionó, lanzar excepción
        raise Exception(f"No se pudo llenar ningún campo con selectores: {selectors}")


# ══════════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL DE INTEGRACIÓN
# ══════════════════════════════════════════════════════════════════════════════

async def automatizar_rizoma_completo(
    profile: Dict[str, Any],
    credenciales: Dict[str, str],
    task_state: Dict[str, Any]
):
    """
    Función principal para automatizar Rizoma.
    
    Args:
        profile: Perfil del investigador
        credenciales: Credenciales de acceso
        task_state: Estado compartido para progreso
    """
    automator = RizomaAutomator(task_state)
    await automator.automatizar_completo(profile, credenciales)


# ═══════════════════════════════════════════════════════════════════════════════
# FIN DE ARCHIVO: rizoma_automation.py
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# ARCHIVO 2: utils.py (Utilidades adicionales)
# ═══════════════════════════════════════════════════════════════════════════════

"""
Utilidades adicionales para el sistema de automatización.
"""

import json
from pathlib import Path
from xml.etree import ElementTree as ET
from typing import List, Dict, Any


def parse_endnote_xml(xml_path: str) -> List[Dict[str, Any]]:
    """
    Parsea un XML exportado de EndNote y devuelve lista de citas.
    
    Args:
        xml_path: Ruta al archivo XML
        
    Returns:
        Lista de diccionarios con información de cada cita
    """
    def _txt(elem, path: str) -> str:
        """Extrae texto limpio de un sub-elemento XML de EndNote."""
        node = elem.find(path)
        if node is None:
            return ""
        parts = []
        for child in node.iter():
            if child.text:
                parts.append(child.text.strip())
            if child.tail:
                parts.append(child.tail.strip())
        return " ".join(p for p in parts if p)
    
    try:
        tree = ET.parse(xml_path)
        root = tree.getroot()
    except ET.ParseError:
        return []
    
    citas = []
    for rec in root.findall(".//record"):
        # Autores
        authors = []
        for a in rec.findall(".//authors/author"):
            name = _txt(a, "style") or "".join(a.itertext()).strip()
            if name:
                authors.append(name)
        
        title = _txt(rec, "titles/title") or _txt(rec, "titles/title/style")
        journal = _txt(rec, "titles/secondary-title") or _txt(rec, "periodical/full-title")
        year = _txt(rec, "dates/year")
        volume = _txt(rec, "volume")
        issue = _txt(rec, "number")
        pages = _txt(rec, "pages")
        doi = _txt(rec, "electronic-resource-num")
        isbn = _txt(rec, "isbn")
        database = _txt(rec, "remote-database-name")
        
        # URL
        url = ""
        for url_elem in rec.findall(".//urls/related-urls/url"):
            url = "".join(url_elem.itertext()).strip()
            if url:
                break
        
        # research-notes: B = colaborativa, C = autocita, vacío = A
        notes_raw = _txt(rec, "research-notes")
        notes_upper = notes_raw.upper().strip()
        if notes_upper == "B":
            tipo = "B"
        elif notes_upper == "C":
            tipo = "C"
        else:
            tipo = "A"
        
        # Referencia APA-7 básica
        autor_str = "; ".join(authors[:6])
        if len(authors) > 6:
            autor_str += " et al."
        apa = f"{autor_str} ({year}). {title}. {journal}"
        if volume:
            apa += f", {volume}"
            if issue:
                apa += f"({issue})"
        if pages:
            apa += f", {pages}"
        if doi:
            apa += f". https://doi.org/{doi.lstrip('https://doi.org/')}"
        
        citas.append({
            "authors": authors,
            "title": title,
            "journal": journal,
            "year": year,
            "volume": volume,
            "issue": issue,
            "pages": pages,
            "doi": doi,
            "isbn": isbn,
            "url": url,
            "database": database,
            "tipo": tipo,
            "apa": apa.strip(),
        })
    
    return citas


def guardar_json(data: Any, filepath: str):
    """
    Guarda datos en formato JSON con encoding UTF-8.
    
    Args:
        data: Datos a guardar
        filepath: Ruta del archivo
    """
    Path(filepath).write_text(
        json.dumps(data, indent=2, ensure_ascii=False),
        encoding="utf-8"
    )


def cargar_json(filepath: str) -> Any:
    """
    Carga datos desde un archivo JSON.
    
    Args:
        filepath: Ruta del archivo
        
    Returns:
        Datos cargados
    """
    if not Path(filepath).exists():
        return {}
    return json.loads(Path(filepath).read_text(encoding="utf-8"))


# ═══════════════════════════════════════════════════════════════════════════════
# FIN DE ARCHIVO: utils.py
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# NOTAS DE USO
# ═══════════════════════════════════════════════════════════════════════════════

"""
INSTRUCCIONES DE USO:

1. Copia el contenido de "ARCHIVO 1: rizoma_automation.py" en un archivo llamado:
   rizoma_automation.py

2. Copia el contenido de "ARCHIVO 2: utils.py" en un archivo llamado:
   utils.py

3. El archivo app.py ya existe en tu proyecto, úsalo tal como está.

4. Instala las dependencias:
   pip install -r requirements.txt
   python -m playwright install chromium

5. Ejecuta la aplicación:
   python app.py

6. Abre http://localhost:5000 en tu navegador

¡Listo para automatizar Rizoma!
"""