"""
Bronze Ingestor Pipeline
Diplomado Gestión de Datos 2026
Laura Alejandra Sepulveda 
Script para procesar archivos de la carpeta landing, clasificándolos
en bronze (contenido) o bad_data (vacíos).
"""

import logging
from pathlib import Path
import shutil
import sys

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger(__name__)

def procesar_archivos():
    """
    Procesa todos los archivos en la carpeta landing,
    moviéndolos a bronze o bad_data según su contenido.
    """
    base_path = Path.cwd()
    landing_path = base_path / "landing"
    bronze_path = base_path / "bronze"
    bad_data_path = base_path / "bad_data"
    
    for folder in [landing_path, bronze_path, bad_data_path]:
        if not folder.exists():
            logger.error(f"Error: La carpeta '{folder.name}' no existe")
            return
    
    procesados = 0
    rechazados = 0
    errores = 0
    
    # Iterar sobre todos los archivos en landing
    for archivo_path in landing_path.iterdir():
        if archivo_path.is_file():
            try:
                # Verificar si el archivo está vacío
                if archivo_path.stat().st_size > 0:
                    # Archivo con contenido -> mover a bronze
                    destino = bronze_path / archivo_path.name
                    shutil.move(str(archivo_path), str(destino))
                    logger.info(f"Procesado: {archivo_path.name} -> Bronze")
                    procesados += 1
                else:
                    # Archivo vacío -> mover a bad_data
                    destino = bad_data_path / archivo_path.name
                    shutil.move(str(archivo_path), str(destino))
                    logger.info(f"Rechazado: {archivo_path.name} -> Bad Data")
                    rechazados += 1
                    
            except Exception as e:
                # Manejar cualquier error sin detener el programa
                logger.error(f"Error procesando {archivo_path.name}: {str(e)}")
                errores += 1
                continue
    
    # Resumen final
    logger.info("\n" + "="*50)
    logger.info("RESUMEN DE PROCESAMIENTO:")
    logger.info(f"Archivos procesados (Bronze): {procesados}")
    logger.info(f"Archivos rechazados (Bad Data): {rechazados}")
    logger.info(f"Errores encontrados: {errores}")
    logger.info(f"Total archivos en landing: {len(list(landing_path.iterdir()))}")
    logger.info("="*50)
    
    # Verificar si landing quedó vacía
    archivos_restantes = [f for f in landing_path.iterdir() if f.is_file()]
    if not archivos_restantes:
        logger.info("✓ Carpeta landing quedó vacía")
    else:
        logger.warning(f"⚠  Aún hay {len(archivos_restantes)} archivos en landing")

if __name__ == "__main__":
    logger.info("Iniciando Bronze Ingestor Pipeline...")
    logger.info("="*50)
    procesar_archivos()
    logger.info("\nProceso completado!")