# Aplicación Flask - Gestión de Canchas

Esta aplicación Flask proporciona una interfaz web para visualizar y gestionar todas las funcionalidades del sistema de canchas.

## Instalación

1. Instalar las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

1. Desde el directorio `apps`, ejecutar:
```bash
python app.py
```

2. Abrir el navegador en:
```
http://localhost:5000
```

## Funcionalidades

La aplicación incluye endpoints REST y una interfaz web para:

- **Clientes**: Ver, agregar, modificar y eliminar clientes
- **Canchas**: Ver, agregar, modificar y eliminar canchas
- **Reservas**: Ver, agregar, modificar y eliminar reservas
- **Pagos**: Ver y agregar pagos
- **Torneos**: Ver, agregar, modificar y eliminar torneos
- **Tipos de Cancha**: Ver y agregar tipos de cancha
- **Servicios**: Ver y agregar servicios
- **Métodos de Pago**: Ver y agregar métodos de pago

## Endpoints API

### Clientes
- `GET /api/clientes` - Obtener todos los clientes
- `POST /api/clientes` - Agregar un cliente
- `PUT /api/clientes/<dni>` - Modificar un cliente
- `DELETE /api/clientes/<dni>` - Eliminar un cliente

### Canchas
- `GET /api/canchas` - Obtener todas las canchas
- `POST /api/canchas` - Agregar una cancha
- `PUT /api/canchas/<nro_cancha>` - Modificar una cancha
- `DELETE /api/canchas/<nro_cancha>` - Eliminar una cancha

### Reservas
- `GET /api/reservas` - Obtener todas las reservas
- `POST /api/reservas` - Agregar una reserva
- `PUT /api/reservas/<nro_reserva>` - Modificar una reserva
- `DELETE /api/reservas/<nro_reserva>` - Eliminar una reserva

### Pagos
- `GET /api/pagos` - Obtener todos los pagos
- `POST /api/pagos` - Agregar un pago

### Torneos
- `GET /api/torneos` - Obtener todos los torneos
- `POST /api/torneos` - Agregar un torneo
- `PUT /api/torneos/<id>` - Modificar un torneo
- `DELETE /api/torneos/<id>` - Eliminar un torneo

### Tipos de Cancha
- `GET /api/tipos-cancha` - Obtener todos los tipos de cancha
- `POST /api/tipos-cancha` - Agregar un tipo de cancha

### Servicios
- `GET /api/servicios` - Obtener todos los servicios
- `POST /api/servicios` - Agregar un servicio

### Métodos de Pago
- `GET /api/metodos-pago` - Obtener todos los métodos de pago
- `POST /api/metodos-pago` - Agregar un método de pago

## Notas

- La base de datos se inicializa automáticamente al iniciar la aplicación
- La interfaz web es responsive y funciona en dispositivos móviles
- Todos los datos se muestran en tablas interactivas con opciones para agregar y eliminar

