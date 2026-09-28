# Empezar corriendo una imagen de python 
FROM --platform=linux/amd64 python:3.8-alpine

# Copiar requerimientos para ejecutar el programa
COPY ./requirements.txt /app/requirements.txt

# Cambiar de directorio de trabajo a donde esta el ejectuable del API
WORKDIR /app

# Instalar requerimientos de la app
RUN pip install -r requirements.txt

# Copiar el contenido del directorio actual en la imagen de docker
COPY . /app

# Agregar variable de entorno con el nombre del estudiante
ENV user_name Estudiante

# Variable de entorno para escribir en txt dentro de la contenedora el resultado
# Por defecto esta en false (No escribe txt en la contenedora)
ENV write_result not_show

# Configurar el contenedor para correr en una manera ejectuble
ENTRYPOINT [ "python" ]

# Archivo principal donde corre el API
CMD ["view.py" ]