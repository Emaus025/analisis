# Rent4you Data Warehouse Repository  

Este repositorio contiene datos y scripts para procesar información de ventas del Data Warehouse de Rent4you, empresa mexicana de alquiler de vehículos.  
El análisis se enfoca en el rendimiento de ventas por sucursal en estas ciudades:  
- Ciudad de México  
- Monterrey  
- Mérida  
- Guadalajara  
- Puebla  

## Estructura del repositorio  
- data/raw/: Datos originales (ventas_raw.csv con registros de alquileres simulados)  
- data/processed/: Datos procesados (ventas_por_sucursal.csv con métricas por sucursal)  
- data/dimensions/: Tablas dimensionales:  
  - dim_sucursal.csv  
  - dim_cliente.csv  
  - dim_vehiculo.csv  
  - dim_tiempo.csv  
- scripts/: Códigos Python:  
  - preprocess_ventas.py: Procesa los datos crudos  
  - test_ventas.py: Valida la calidad de los datos  
- results.txt: Resultados de pruebas  

## Requisitos  
- Python 3.8 o superior  
- Dependencias:  
```  
pip install pandas numpy python-dateutil  
```  

## Instalación  
1. Clonar el repositorio:  
```  
git clone https://github.com/ariadnalpz/rent4you-dw-repository.git  
cd rent4you-dw-repository  
```  

2. Instalar dependencias:  
```  
pip install pandas numpy python-dateutil  
```  

## Uso  
1. Colocar los archivos CSV en data/raw y data/dimensions  
2. Procesar los datos:  
```  
python scripts/preprocess_ventas.py  
```  
3. Verificar calidad:  
```  
python scripts/test_ventas.py  
```  

Los datos procesados están listos para análisis en herramientas como Tableau, Power BI o Excel.
