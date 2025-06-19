import pandas as pd
import numpy as np
from dateutil.parser import parse
import os

# Directorios
RAW_DIR = 'data/raw'
DIM_DIR = 'data/dimensions'
PROC_DIR = 'data/processed'
os.makedirs(PROC_DIR, exist_ok=True)

# Carga de datos
ventas = pd.read_csv(f'{RAW_DIR}/ventas_raw.csv')
dim_sucursal = pd.read_csv(f'{DIM_DIR}/dim_sucursal.csv')
dim_cliente = pd.read_csv(f'{DIM_DIR}/dim_cliente.csv')
dim_vehiculo = pd.read_csv(f'{DIM_DIR}/dim_vehiculo.csv')
dim_tiempo = pd.read_csv(f'{DIM_DIR}/dim_tiempo.csv')

# 1. Manejo de valores nulos
ventas['Monto_Alquiler'].fillna(ventas['Monto_Alquiler'].median(), inplace=True)
ventas['Descuento'].fillna(0, inplace=True)

# 2. Normalización de fechas
def parse_date(date_str):
    try:
        return parse(date_str).strftime('%Y-%m-%d')
    except:
        return np.nan

ventas['Fecha_Alquiler'] = ventas['Fecha_Alquiler'].apply(parse_date)
ventas.dropna(subset=['Fecha_Alquiler'], inplace=True)

# 3. Eliminación de duplicados
ventas.drop_duplicates(subset=['ID_Alquiler'], keep='first', inplace=True)

# 4. Validación de IDs
ventas = ventas[ventas['ID_Sucursal'].isin(dim_sucursal['ID_Sucursal'])]
ventas = ventas[ventas['ID_Cliente'].isin(dim_cliente['ID_Cliente'])]
ventas = ventas[ventas['ID_Vehiculo'].isin(dim_vehiculo['ID_Vehiculo'])]

# 5. Corrección de valores inválidos
ventas['Duracion_Dias'] = ventas['Duracion_Dias'].clip(lower=1)
ventas['Descuento'] = ventas['Descuento'].clip(lower=0)
ventas['Monto_Alquiler'] = ventas['Monto_Alquiler'].clip(lower=0)

# 6. Agregación por sucursal
ventas['Monto_Final'] = ventas['Monto_Alquiler'] - ventas['Descuento']
ventas_por_sucursal = ventas.groupby('ID_Sucursal').agg({
    'ID_Alquiler': 'count',
    'Monto_Final': ['sum', 'mean']
}).reset_index()
ventas_por_sucursal.columns = ['ID_Sucursal', 'Total_Alquileres', 'Monto_Total', 'Monto_Promedio']

# 7. Unir con dim_sucursal
ventas_por_sucursal = ventas_por_sucursal.merge(
    dim_sucursal[['ID_Sucursal', 'Nombre_Sucursal', 'Ciudad']],
    on='ID_Sucursal',
    how='left'
)

# 8. Guardar resultado
ventas_por_sucursal.to_csv(f'{PROC_DIR}/ventas_por_sucursal.csv', index=False)
print("Preprocesamiento completado. Datos guardados en data/processed/ventas_por_sucursal.csv")