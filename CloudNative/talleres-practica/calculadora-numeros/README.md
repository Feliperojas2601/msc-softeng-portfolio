# Calculadora de números

Para levantar el proyecto en su repositorio local, ejecute los siguientes pasos:

### 1. Instalar ambiente virtual:

En su terminal ejecute:
```
pip install virtualenv
```
Cuando la descarga finalize cree el ambiente virtual mediante:
```
virtualenv vnv
```
Esto creara en la carpeta local, archivos necesarios para aislar un ambiente de dependencias en Python, activelo mediante:
```
source vnv/bin/activate
```
Posteriormente baje las dependencias mediante:
```
pip install -r requirements.txt
```
### 2. Levantar la API:
En su terminal ejecute:
```
python3 -m flask run
``` 
### 3. Curl para sumar el dos números:
```
curl --location --request POST 'http://localhost:4000/suma' \
--header 'Content-Type: application/json' \
--data-raw '{    
    "num_1" : 2,
    "num_2": 3
}'

```
