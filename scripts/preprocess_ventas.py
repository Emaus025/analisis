import pandas as pd
import numpy as np
from dateutil.parser import parse
import os

# Directorios
RAW_DIR = 'data/raw'
DIM_DIR = 'data/dimensions'
PROC_DIR = 'data/processed'
os.makedirs(PROC_DIR, exist_ok=True)

# Carga de datos con verificación de columnas
try:
    ventas = pd.read_csv(f'{RAW_DIR}/ventas_raw.csv')
    dim_sucursal = pd.read_csv(f'{DIM_DIR}/dim_sucursal.csv')
    dim_cliente = pd.read_csv(f'{DIM_DIR}/dim_cliente.csv')
    dim_telefono = pd.read_csv(f'{DIM_DIR}/dim_telefono.csv')
    dim_tiempo = pd.read_csv(f'{DIM_DIR}/dim_tiempo.csv')
    
    # Verificar columnas necesarias
    required_ventas_cols = ['ID_Alquiler', 'ID_Sucursal', 'ID_Cliente', 'ID_Telefono', 
                           'Fecha_Alquiler', 'Duracion_Dias', 'Monto_Alquiler', 'Descuento']
    if not all(col in ventas.columns for col in required_ventas_cols):
        missing = [col for col in required_ventas_cols if col not in ventas.columns]
        raise ValueError(f'Columnas faltantes en ventas_raw.csv: {missing}')

except Exception as e:
    print(f"Error cargando datos: {str(e)}")
    exit(1)

# 1. Manejo de valores nulos (versión compatible con pandas 3.0)
ventas = ventas.assign(
    Monto_Alquiler=ventas['Monto_Alquiler'].fillna(ventas['Monto_Alquiler'].median()),
    Descuento=ventas['Descuento'].fillna(0)
)

# 2. Normalización de fechas
def parse_date(date_str):
    try:
        return parse(date_str).strftime('%Y-%m-%d')
    except:
        return np.nan

ventas = ventas.assign(Fecha_Alquiler=ventas['Fecha_Alquiler'].apply(parse_date))
ventas = ventas.dropna(subset=['Fecha_Alquiler'])

# 3. Eliminación de duplicados
ventas = ventas.drop_duplicates(subset=['ID_Alquiler'], keep='first')

# 4. Validación de IDs
ventas = ventas[
    ventas['ID_Sucursal'].isin(dim_sucursal['ID_Sucursal']) &
    ventas['ID_Cliente'].isin(dim_cliente['ID_Cliente']) &
    ventas['ID_Telefono'].isin(dim_telefono['ID_Telefono'])
]

# 5. Corrección de valores inválidos
ventas = ventas.assign(
    Duracion_Dias=ventas['Duracion_Dias'].clip(lower=1),
    Descuento=ventas['Descuento'].clip(lower=0),
    Monto_Alquiler=ventas['Monto_Alquiler'].clip(lower=0)
)

# 6. Agregación por sucursal
ventas = ventas.assign(Monto_Final=ventas['Monto_Alquiler'] - ventas['Descuento'])
ventas_por_sucursal = ventas.groupby('ID_Sucursal').agg(
    Total_Alquileres=('ID_Alquiler', 'count'),
    Monto_Total=('Monto_Final', 'sum'),
    Monto_Promedio=('Monto_Final', 'mean')
).reset_index()

# 7. Unir con dim_sucursal
ventas_por_sucursal = ventas_por_sucursal.merge(
    dim_sucursal[['ID_Sucursal', 'Nombre_Sucursal', 'Ciudad']],
    on='ID_Sucursal',
    how='left'
)

# 8. Guardar resultado
ventas_por_sucursal.to_csv(f'{PROC_DIR}/ventas_por_sucursal.csv', index=False)
print("Preprocesamiento completado. Datos guardados en data/processed/ventas_por_sucursal.csv")