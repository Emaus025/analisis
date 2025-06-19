# Rent4you Data Warehouse Repository

Este repositorio contiene datos y scripts para preprocesar ventas del Data Warehouse de Rent4you, una empresa de alquiler de vehículos en México.  
El enfoque está en analizar ventas por sucursal en las siguientes ciudades:  
- Ciudad de México  
- Monterrey  
- Mérida  
- Guadalajara  
- Puebla  

## Estructura
- `data/raw/`: Datos crudos simulados (`ventas_raw.csv` con registros de alquileres).  
- `data/processed/`: Datos preprocesados (`ventas_por_sucursal.csv` con métricas por sucursal).  
- `data/dimensions/`: Tablas dimensionales:
  - `dim_sucursal.csv`
  - `dim_cliente.csv`
  - `dim_vehiculo.csv`
  - `dim_tiempo.csv`  
- `scripts/`: Scripts de Python:
  - `preprocess_ventas.py`: Preprocesa los datos crudos.  
  - `test_ventas.py`: Valida la calidad de los datos procesados.  
- `results.txt`: Documentación de las pruebas realizadas.

## Requisitos
- **Python 3.8+**
- **Dependencias**:
  ```bash
  pip install pandas numpy python-dateutil

## Instalación

- `Clona el repositorio`:
  git clone https://github.com/ariadnalpz/rent4you-dw-repository.git
  cd rent4you-dw-repository

- `Instala las dependencias`:
  pip install pandas numpy python-dateutil

## Uso
Asegúrate de que los archivos CSV estén en las carpetas data/raw y data/dimensions.

- `Ejecuta el script de preprocesamiento`:
  python scripts/preprocess_ventas.py

Revisa los datos procesados en data/processed/ventas_por_sucursal.csv.

- `Ejecuta las pruebas de calidad`:
  python scripts/test_ventas.py

Abre los datos procesados en herramientas BI (Tableau, Power BI, Excel) para análisis.