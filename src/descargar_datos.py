"""
Script para descargar datos desde datos.gov.co usando Socrata,
unificar los periodos y guardar en un archivo CSV.
Los códigos se pueden pasar como argumentos:
    python descargar_datos.py 2020-1=a8xr-en99 2020-2=rnvb-vnyh
"""

import sys
import os
import pandas as pd
from sodapy import Socrata

LIMIT = 40000  # Límite de filas que se importarán
OUTPUT_DIR = "data"
OUTPUT_FILE = "datos.csv"

def parse_args(args):
    """
    Convierte los argumentos tipo '2020-1=a8xr-en99' en un diccionario.
    """
    codes = {}
    for arg in args:
        if "=" in arg:
            periodo, codigo = arg.split("=", 1)
            codes[periodo] = codigo
        else:
            print(f"⚠️  Argumento ignorado (formato inválido): {arg}")
    return codes

def descargar_datos(codes, limit=40000):
    print("Conectando a datos.gov.co ...")
    client = Socrata("www.datos.gov.co", None)

    datos = {}
    for periodo, codigo in codes.items():
        print(f"Descargando periodo {periodo} (código {codigo}) ...")
        results = client.get(codigo, limit=limit)
        df = pd.DataFrame.from_records(results)
        datos[periodo] = df
        print(f"  -> {len(df)} registros descargados.")
    return datos

def combinar_datos(datos_dict):
    print("Combinando los periodos...")
    columnas_comunes = set.intersection(*[set(df.columns) for df in datos_dict.values()])
    columnas_comunes = list(columnas_comunes)
    print(f"Columnas comunes encontradas: {columnas_comunes}")

    dataframes = []
    for periodo, df in datos_dict.items():
        df_filtrado = df[columnas_comunes].copy()
        df_filtrado["periodo"] = periodo
        dataframes.append(df_filtrado)

    archivo = pd.concat(dataframes, ignore_index=True)
    print(f"DataFrame final con {len(archivo)} filas y {len(archivo.columns)} columnas.")
    return archivo

def guardar_csv(df, output_dir, filename):
    os.makedirs(output_dir, exist_ok=True)
    ruta = os.path.join(output_dir, filename)
    df.to_csv(ruta, index=False)
    print(f"Datos guardados en {ruta}")
    return ruta

def main():
    print("=== Descarga de datos desde datos.gov.co ===\n")

    # Obtener argumentos de la línea de comandos
    args = sys.argv[1:]
    if not args:
        print("❌ No se especificaron códigos. Ejemplo de uso:")
        print("   python descargar_datos.py 2020-1=a8xr-en99 2020-2=rnvb-vnyh")
        sys.exit(1)

    codes = parse_args(args)
    if not codes:
        print("❌ No se encontraron códigos válidos. Finalizando.")
        sys.exit(1)

    # Descargar, combinar y guardar
    datos = descargar_datos(codes, LIMIT)
    archivo = combinar_datos(datos)
    guardar_csv(archivo, OUTPUT_DIR, OUTPUT_FILE)

    print("\nProceso completado exitosamente ✅")

if __name__ == "__main__":
    main()
