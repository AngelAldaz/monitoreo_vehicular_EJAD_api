#!/usr/bin/env python
"""
Script para poblar la base de datos con datos de prueba para vehículos,
marcas, modelos y descripciones.
"""
import os
import sys

# Agregar el directorio raíz al path para importar el paquete app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.scripts.insert_data import insert_data

if __name__ == "__main__":
    print("Iniciando inserción de datos en la base de datos...")
    insert_data()
    print("Proceso completado.") 