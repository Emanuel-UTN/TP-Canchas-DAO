# TP-CANCHAS-DAO

Este proyecto es una aplicación Django destinada a la gestión de canchas y reservas. A continuación se presentan las instrucciones para configurar y ejecutar el proyecto.

## Requisitos

Asegúrate de tener instalado Python 3.x y pip. También necesitarás un entorno virtual para gestionar las dependencias del proyecto.

## Instalación

1. Clona el repositorio:

   ```
   git clone <URL_DEL_REPOSITORIO>
   cd TP-CANCHAS-DAO
   ```

2. Crea un entorno virtual:

   ```
   python -m venv venv
   ```

3. Activa el entorno virtual:

   - En Windows:

     ```
     venv\Scripts\activate
     ```

   - En macOS/Linux:

     ```
     source venv/bin/activate
     ```

4. Instala las dependencias:

   ```
   pip install -r requirements.txt
   ```

5. Configura las variables de entorno en el archivo `.env` según sea necesario.

## Migraciones

Ejecuta las migraciones para crear las tablas en la base de datos:

```
python manage.py migrate
```

## Ejecución

Inicia el servidor de desarrollo:

```
python manage.py runserver
```

Ahora puedes acceder a la aplicación en `http://127.0.0.1:8000/`.

## Estructura del Proyecto

- `manage.py`: Script principal para interactuar con el proyecto.
- `requirements.txt`: Lista de dependencias del proyecto.
- `.env`: Variables de entorno.
- `.gitignore`: Archivos y carpetas a ignorar por Git.
- `tp_canchas_dao/`: Contiene la configuración del proyecto Django.
- `apps/`: Contiene las aplicaciones de la lógica del negocio.
- `config/`: Contiene la configuración del servidor.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, abre un issue o envía un pull request para discutir cambios.

## Licencia

Este proyecto está bajo la Licencia MIT.