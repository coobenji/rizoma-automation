#!/usr/bin/env python3
"""
Script de Prueba - Componentes del Sistema de Automatización Rizoma
====================================================================

Este script te permite probar componentes individuales del sistema
sin necesidad de ejecutar la aplicación web completa.

Uso:
    python test_componentes.py [opcion]

Opciones:
    1. parsear_xml          - Prueba el parser de XMLs de EndNote
    2. generar_informe      - Genera un informe de ejemplo
    3. probar_login         - Prueba solo el login en Rizoma
    4. listar_xmls          - Lista todos los XMLs en la carpeta uploads
    5. ver_perfil           - Muestra el contenido de un perfil
"""

import sys
import json
import glob
import asyncio
from pathlib import Path
from pprint import pprint

# Importar funciones del proyecto
try:
    from app import parse_endnote_xml, generar_informe, load_profiles
    from rizoma_automation import RizomaAutomator
except ImportError as e:
    print(f"❌ Error importando módulos: {e}")
    print("\nAsegúrate de ejecutar este script desde el directorio del proyecto.")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════════
# FUNCIONES DE PRUEBA
# ═══════════════════════════════════════════════════════════════════

def prueba_parsear_xml():
    """Prueba el parser de XML de EndNote"""
    print("\n" + "="*70)
    print("PRUEBA: Parser de XML de EndNote")
    print("="*70 + "\n")
    
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        print("❌ No existe la carpeta 'uploads'")
        print("   Crea la carpeta y coloca tus archivos XML ahí.")
        return
    
    xml_files = list(uploads_dir.glob("*.xml"))
    
    if not xml_files:
        print("❌ No hay archivos XML en la carpeta 'uploads'")
        print("   Coloca al menos un archivo XML de EndNote ahí.")
        return
    
    print(f"📂 Encontrados {len(xml_files)} archivo(s) XML:\n")
    
    for xml_file in xml_files:
        print(f"\n📄 Procesando: {xml_file.name}")
        print("-" * 70)
        
        try:
            citas = parse_endnote_xml(str(xml_file))
            
            # Estadísticas
            total = len(citas)
            tipo_a = sum(1 for c in citas if c["tipo"] == "A")
            tipo_b = sum(1 for c in citas if c["tipo"] == "B")
            tipo_c = sum(1 for c in citas if c["tipo"] == "C")
            
            print(f"   Total de citas: {total}")
            print(f"   - Tipo A (Individual): {tipo_a}")
            print(f"   - Tipo B (Colaborativa): {tipo_b}")
            print(f"   - Tipo C (Autocita): {tipo_c}")
            
            # Mostrar primera cita como ejemplo
            if citas:
                print(f"\n   📝 Ejemplo de primera cita:")
                print(f"   {'─'*66}")
                primera = citas[0]
                print(f"   Autores: {', '.join(primera['authors'][:3])}")
                if len(primera['authors']) > 3:
                    print(f"            ... y {len(primera['authors']) - 3} más")
                print(f"   Título:  {primera['title'][:60]}...")
                print(f"   Revista: {primera['journal']}")
                print(f"   Año:     {primera['year']}")
                print(f"   DOI:     {primera['doi']}")
                print(f"   Tipo:    {primera['tipo']}")
                print(f"   {'─'*66}")
            
            print(f"\n   ✅ Archivo procesado correctamente\n")
            
        except Exception as e:
            print(f"   ❌ Error procesando archivo: {e}\n")


def prueba_generar_informe():
    """Genera un informe de prueba"""
    print("\n" + "="*70)
    print("PRUEBA: Generación de Informe")
    print("="*70 + "\n")
    
    profiles = load_profiles()
    
    if not profiles:
        print("❌ No hay perfiles creados")
        print("   Crea un perfil usando la aplicación web primero.")
        print("   Ejecuta: python app.py")
        return
    
    print(f"📊 Perfiles disponibles: {len(profiles)}\n")
    
    for idx, (pid, profile) in enumerate(profiles.items(), 1):
        print(f"{idx}. {profile.get('nombre', 'Sin nombre')} ({pid})")
    
    print("\nEscoge un perfil (número): ", end="")
    try:
        opcion = int(input().strip())
        pid = list(profiles.keys())[opcion - 1]
        profile = profiles[pid]
    except (ValueError, IndexError):
        print("❌ Opción inválida")
        return
    
    print(f"\n📝 Generando informe para: {profile.get('nombre', 'Sin nombre')}")
    print("-" * 70)
    
    # Generar informe UNAM
    print("\n🎓 Modalidad UNAM (todos los tipos):")
    informe_unam = generar_informe(profile, "UNAM")
    
    print(f"   Documentos procesados: {len(informe_unam['documentos'])}")
    print(f"   Total citas Tipo A: {informe_unam['total_a']}")
    print(f"   Total citas Tipo B: {informe_unam['total_b']}")
    print(f"   Total citas Tipo C: {informe_unam['total_c']}")
    print(f"   TOTAL: {informe_unam['total_general']}")
    
    # Generar informe SNI
    print("\n🔬 Modalidad SNI/SECIHTI (solo A y B):")
    informe_sni = generar_informe(profile, "SNI")
    
    print(f"   Documentos procesados: {len(informe_sni['documentos'])}")
    print(f"   Total citas Tipo A: {informe_sni['total_a']}")
    print(f"   Total citas Tipo B: {informe_sni['total_b']}")
    print(f"   TOTAL: {informe_sni['total_general']}")
    
    print("\n✅ Informes generados correctamente")
    print("\n💡 Tip: Usa la aplicación web para exportar a DOCX/PDF")


async def prueba_login_rizoma():
    """Prueba solo el login en Rizoma"""
    print("\n" + "="*70)
    print("PRUEBA: Login en Rizoma")
    print("="*70 + "\n")
    
    print("⚠️  Esta prueba abrirá un navegador real")
    print("    Solo probará el login, sin registrar artículos\n")
    
    usuario = input("Usuario de Rizoma: ").strip()
    password = input("Contraseña: ").strip()
    
    if not usuario or not password:
        print("\n❌ Debes proporcionar usuario y contraseña")
        return
    
    print("\n🚀 Iniciando prueba de login...")
    print("-" * 70)
    
    # Estado de tarea mock
    task_state = {
        "active": True,
        "log": [],
        "status": "running",
        "progress": 0,
        "total": 0
    }
    
    # Crear automatizador
    automator = RizomaAutomator(task_state)
    
    from playwright.async_api import async_playwright
    
    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=False,
            args=["--start-maximized"]
        )
        
        context = await browser.new_context(viewport=None)
        page = await context.new_page()
        
        try:
            # Intentar login
            exito = await automator._login(page, {"usuario": usuario, "password": password})
            
            # Mostrar log
            print("\n📋 LOG DE LA OPERACIÓN:")
            for msg in task_state["log"]:
                print(f"   {msg}")
            
            if exito:
                print("\n✅ LOGIN EXITOSO")
                print("\n⏸️  El navegador permanecerá abierto por 10 segundos")
                print("    Verifica manualmente que estés en tu dashboard")
                await asyncio.sleep(10)
            else:
                print("\n❌ LOGIN FALLÓ")
                print("\n💡 Posibles causas:")
                print("   - Credenciales incorrectas")
                print("   - Cambios en la página de login de Rizoma")
                print("   - Problemas de conectividad")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
        finally:
            await browser.close()


def listar_xmls():
    """Lista todos los XMLs en uploads"""
    print("\n" + "="*70)
    print("ARCHIVOS XML EN UPLOADS")
    print("="*70 + "\n")
    
    uploads_dir = Path("uploads")
    if not uploads_dir.exists():
        print("❌ No existe la carpeta 'uploads'")
        uploads_dir.mkdir()
        print("✅ Carpeta creada. Coloca tus XMLs ahí.")
        return
    
    xml_files = list(uploads_dir.glob("*.xml"))
    
    if not xml_files:
        print("📂 Carpeta vacía - no hay archivos XML")
        return
    
    print(f"📂 Total: {len(xml_files)} archivo(s)\n")
    
    for idx, xml_file in enumerate(xml_files, 1):
        print(f"{idx:2}. {xml_file.name}")
        print(f"    Tamaño: {xml_file.stat().st_size / 1024:.1f} KB")
        
        # Intentar parsear
        try:
            citas = parse_endnote_xml(str(xml_file))
            print(f"    Citas: {len(citas)} (A:{sum(1 for c in citas if c['tipo']=='A')}, "
                  f"B:{sum(1 for c in citas if c['tipo']=='B')}, "
                  f"C:{sum(1 for c in citas if c['tipo']=='C')})")
        except:
            print(f"    ⚠️  Error al parsear")
        
        print()


def ver_perfil():
    """Muestra el contenido de un perfil"""
    print("\n" + "="*70)
    print("VER PERFIL")
    print("="*70 + "\n")
    
    profiles = load_profiles()
    
    if not profiles:
        print("❌ No hay perfiles creados")
        return
    
    print(f"📊 Perfiles disponibles: {len(profiles)}\n")
    
    for idx, (pid, profile) in enumerate(profiles.items(), 1):
        nombre = profile.get("nombre", "Sin nombre")
        entidad = profile.get("entidad", "")
        pubs = len(profile.get("publicaciones", []))
        print(f"{idx}. {nombre}")
        print(f"   Entidad: {entidad}")
        print(f"   Publicaciones: {pubs}\n")
    
    print("Escoge un perfil (número): ", end="")
    try:
        opcion = int(input().strip())
        pid = list(profiles.keys())[opcion - 1]
        profile = profiles[pid]
    except (ValueError, IndexError):
        print("❌ Opción inválida")
        return
    
    print("\n" + "="*70)
    print(f"PERFIL: {profile.get('nombre', 'Sin nombre')}")
    print("="*70 + "\n")
    
    pprint(profile)


# ═══════════════════════════════════════════════════════════════════
# MENÚ PRINCIPAL
# ═══════════════════════════════════════════════════════════════════

def menu():
    """Muestra el menú de opciones"""
    print("\n" + "="*70)
    print("PRUEBAS DE COMPONENTES - Sistema de Automatización Rizoma")
    print("="*70)
    
    opciones = {
        "1": ("Parsear XML de EndNote", prueba_parsear_xml),
        "2": ("Generar Informe", prueba_generar_informe),
        "3": ("Probar Login en Rizoma", lambda: asyncio.run(prueba_login_rizoma())),
        "4": ("Listar XMLs en Uploads", listar_xmls),
        "5": ("Ver Perfil", ver_perfil),
        "0": ("Salir", None)
    }
    
    print("\nOpciones disponibles:\n")
    for key, (desc, _) in opciones.items():
        print(f"  {key}. {desc}")
    
    print("\nEscoge una opción: ", end="")
    opcion = input().strip()
    
    if opcion not in opciones:
        print("\n❌ Opción inválida")
        return
    
    if opcion == "0":
        print("\n👋 ¡Hasta luego!")
        sys.exit(0)
    
    _, funcion = opciones[opcion]
    if funcion:
        try:
            funcion()
        except KeyboardInterrupt:
            print("\n\n⚠️  Operación cancelada por el usuario")
        except Exception as e:
            print(f"\n❌ Error: {e}")
    
    input("\n\nPresiona ENTER para continuar...")


# ═══════════════════════════════════════════════════════════════════
# EJECUCIÓN
# ═══════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    # Si se pasa un argumento, ejecutar esa opción directamente
    if len(sys.argv) > 1:
        arg = sys.argv[1].lower()
        
        acciones = {
            "parsear_xml": prueba_parsear_xml,
            "generar_informe": prueba_generar_informe,
            "probar_login": lambda: asyncio.run(prueba_login_rizoma()),
            "listar_xmls": listar_xmls,
            "ver_perfil": ver_perfil
        }
        
        if arg in acciones:
            try:
                acciones[arg]()
            except KeyboardInterrupt:
                print("\n\n⚠️  Operación cancelada")
            except Exception as e:
                print(f"\n❌ Error: {e}")
        else:
            print(f"❌ Acción desconocida: {arg}")
            print(f"\nAcciones disponibles: {', '.join(acciones.keys())}")
    else:
        # Modo interactivo
        try:
            while True:
                menu()
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
