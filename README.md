# AssistMe

AssistMe es un proyecto diseñado para gestionar inventarios, generar reportes y procesar pedidos de clientes para una cafetería.

## Requisitos

- Python 3.8 o superior
- pip

## Instalación

1. **Clona el repositorio:**

   git@gitlab.com:jausitech1/asisstme.git
   cd AssistMe

2. **Crea un entorno virtual:**

    python -m venv venv

3. **Activa el entorno virtual:**

    En Windows:

        .\venv\Scripts\activate
    En macOS/Linux:

        source venv/bin/activate
        
4. **Instala las dependencias:**

    pip install -r requirements.txt

## Configuración

1. **Configura las variables de entorno:**

Crea un archivo .env en la raíz del proyecto y añade las siguientes variables:

env:

DATABASE_URI=mysql+pymysql://root:Passw0rd@localhost/probandoflask

## Antes de hacer las migraciones

1. **Ejecutar comando en terminal:**

set FLASK_APP=[FOLDER_PROYECTO]\src_init_.py

## Como hacer las migraciones

1. **Inicializa el directorio de migraciones (si aún no está hecho):**

Si es la primera vez que trabajas con migraciones, necesitas inicializar el directorio de migraciones:

    flask --app src db init

Esto creará una carpeta llamada migrations en la raíz del proyecto que contiene archivos de configuración para las migraciones.

2. **Crea una nueva migración:**

Después de hacer cambios en los modelos de tu base de datos, debes crear una nueva migración para reflejar esos cambios. Usa el siguiente comando para generar un archivo de migración:

    flask --app src db migrate -m "Descripción de los cambios en los modelos"

Reemplaza "Descripción de los cambios en los modelos" con una breve descripción de los cambios realizados en los modelos.

3. **Aplica la migración a la base de datos:**

Una vez que hayas creado una migración, aplícala a la base de datos para que los cambios sean efectivos:

    flask --app src db upgrade

4. **Verifica el estado de las migraciones:**

Puedes verificar el estado actual de las migraciones con el siguiente comando:

    flask --app src db check

5. **Revisa el historial de migraciones:**

Para ver el historial de migraciones aplicadas y disponibles, usa:

    flask --app src db history

6. **Deshazte de una migración (opcional):**

Si necesitas revertir una migración, puedes usar:

    flask --app src db downgrade

Esto deshará la última migración aplicada.




## Para Actualizar dependencias
    pip freeze > requirements.txt
#   L a F o u r m i - c h a t b o t  
 