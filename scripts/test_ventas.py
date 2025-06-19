import pandas as pd
import os

# Directorios
PROC_DIR = 'data/processed'
DIM_DIR = 'data/dimensions'
RAW_DIR = 'data/raw'

# Cargar datos
ventas_por_sucursal = pd.read_csv(f'{PROC_DIR}/ventas_por_sucursal.csv')
dim_sucursal = pd.read_csv(f'{DIM_DIR}/dim_sucursal.csv')
dim_cliente = pd.read_csv(f'{DIM_DIR}/dim_cliente.csv')  # Línea agregada
raw_ventas = pd.read_csv(f'{RAW_DIR}/ventas_raw.csv')   # Línea movida al inicio

# Prueba 1: Verificar que no hay valores nulos
print("Prueba 1: Verificar valores nulos")
nulos = ventas_por_sucursal.isnull().sum()
print(nulos)
assert nulos.sum() == 0, "Hay valores nulos en el archivo procesado"

# Prueba 2: Verificar que los IDs de sucursal son válidos
print("\nPrueba 2: Verificar IDs de sucursal")
invalid_sucursales = ventas_por_sucursal[~ventas_por_sucursal['ID_Sucursal'].isin(dim_sucursal['ID_Sucursal'])]
print(f"Sucursales inválidas: {len(invalid_sucursales)}")
assert len(invalid_sucursales) == 0, "Hay sucursales inválidas"

# Prueba 3: Verificar que las métricas son positivas
print("\nPrueba 3: Verificar métricas positivas")
negative_metrics = ventas_por_sucursal[
    (ventas_por_sucursal['Total_Alquileres'] <= 0) |
    (ventas_por_sucursal['Monto_Total'] <= 0) |
    (ventas_por_sucursal['Monto_Promedio'] <= 0)
]
print(f"Métricas negativas: {len(negative_metrics)}")
assert len(negative_metrics) == 0, "Hay métricas negativas"

# Prueba 4: Verificar cobertura de sucursales
print("\nPrueba 4: Verificar cobertura de sucursales")
expected_sucursales = set(dim_sucursal['ID_Sucursal'])
actual_sucursales = set(ventas_por_sucursal['ID_Sucursal'])
missing_sucursales = expected_sucursales - actual_sucursales
print(f"Sucursales faltantes: {missing_sucursales}")

# Prueba 5: Verificar cálculo de métricas para SUC1
print("\nPrueba 5: Verificar métricas para SUC1")
raw_suc1 = raw_ventas[raw_ventas['ID_Sucursal'] == 'SUC1']
raw_suc1 = raw_suc1[raw_suc1['ID_Cliente'].isin(dim_cliente['ID_Cliente'])]
raw_suc1 = raw_suc1.drop_duplicates(subset=['ID_Alquiler'])
raw_suc1['Descuento'] = raw_suc1['Descuento'].clip(lower=0).fillna(0)
raw_suc1['Monto_Final'] = raw_suc1['Monto_Alquiler'] - raw_suc1['Descuento']
expected_total = raw_suc1['Monto_Final'].sum()
expected_count = len(raw_suc1)
expected_avg = expected_total / expected_count if expected_count > 0 else 0
processed_suc1 = ventas_por_sucursal[ventas_por_sucursal['ID_Sucursal'] == 'SUC1']
print(f"Esperado: Total={expected_total}, Count={expected_count}, Avg={expected_avg}")
print(f"Obtenido: Total={processed_suc1['Monto_Total'].iloc[0]}, Count={processed_suc1['Total_Alquileres'].iloc[0]}, Avg={processed_suc1['Monto_Promedio'].iloc[0]}")
assert abs(processed_suc1['Monto_Total'].iloc[0] - expected_total) < 0.01, "Monto total incorrecto para SUC1"

print("\nTodas las pruebas completadas exitosamente")