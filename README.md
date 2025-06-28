# Repositorio de Data Warehouse para Rent4Tel  

Este repositorio contiene datos y scripts para procesar información de alquileres de teléfonos del Data Warehouse de Rent4Tel, empresa mexicana de alquiler de dispositivos móviles.  

## Estructura actualizada del repositorio  
- `data/raw/`: Datos originales (`alquileres_raw.csv` con registros de alquileres)  
- `data/processed/`: Datos procesados (`alquileres_por_sucursal.csv` con métricas)  
- `data/dimensions/`: Tablas dimensionales actualizadas:  
  - `dim_sucursal.csv` (9 sucursales en principales ciudades)  
  - `dim_cliente.csv` (10 clientes con datos demográficos)  
  - `dim_telefono.csv` (9 modelos de teléfonos)  
  - `dim_tiempo.csv`  

- `scripts/`:  
  - `preprocess_alquileres.py`: Transformación de datos  
  - `test_alquileres.py`: Validación de calidad  
- `results.txt`: Reporte de pruebas  

## Ciudades con cobertura  
- Ciudad de México  
- Monterrey  
- Guadalajara  
- Puebla  
- Cancún  
- Querétaro  
- Tijuana  
- León  
- Toluca  

## Requisitos técnicos  
- **Python 3.8+**  
- **Dependencias**:  
```bash  
pip install pandas numpy python-dateutil  
```  

## Configuración inicial  
1. Clonar repositorio:  
```bash  
git clone https://github.com/ariadnalpz/rent4you-dw-repository.git  
cd rent4you-dw-repository  
```  

2. Instalar dependencias:  
```bash  
pip install -r requirements.txt  
```  

## Flujo de trabajo  
1. Colocar archivos CSV en sus respectivas carpetas  
2. Procesar datos:  
```bash  
python scripts/preprocess_alquileres.py  
```  
3. Validar calidad:  
```bash  
python scripts/test_alquileres.py  
```  

Los datos procesados pueden analizarse en:  
- Tableau/Power BI  
- Excel/Google Sheets  
- Jupyter Notebooks  

## Notas importantes  
- Todos los archivos CSV deben incluir encabezados de columnas  
- Las fechas deben estar en formato YYYY-MM-DD  
- Los IDs deben ser consistentes entre tablas relacionadas  
