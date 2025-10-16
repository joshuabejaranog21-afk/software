# Agenda API - Spring Boot

API REST para gestión de agenda de personas desarrollada con Spring Boot 3.x y MySQL.

## Requisitos

- Java 17 o superior
- Maven 3.6+
- MySQL 5.7+ o MySQL 8.0+
- Base de datos `agenda_db` configurada con usuario `agenda_user`

## Configuración de la Base de Datos

Asegúrate de tener la base de datos MySQL configurada:

```sql
CREATE DATABASE agenda_db;
CREATE USER 'agenda_user'@'localhost' IDENTIFIED BY 'password123';
GRANT ALL PRIVILEGES ON agenda_db.* TO 'agenda_user'@'localhost';
FLUSH PRIVILEGES;
```

La tabla `personas` debe existir en la base de datos con la siguiente estructura:

```sql
CREATE TABLE personas (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    telefono VARCHAR(20),
    direccion TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

## Cómo ejecutar

1. Navegar al directorio del proyecto:
```bash
cd C:\Users\bejar\software\agenda-api
```

2. Compilar el proyecto:
```bash
mvn clean compile
```

3. Ejecutar la aplicación:
```bash
mvn spring-boot:run
```

La aplicación estará disponible en: `http://localhost:8080`

## Endpoints de la API

### Crear Persona
**POST** `/api/personas`

```json
{
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan@email.com",
  "telefono": "+123456789",
  "direccion": "Calle 123, Ciudad"
}
```

**Respuesta exitosa (201):**
```json
{
  "id": 1,
  "nombre": "Juan",
  "apellido": "Pérez",
  "email": "juan@email.com",
  "telefono": "+123456789",
  "direccion": "Calle 123, Ciudad",
  "createdAt": "2025-01-16T10:30:00",
  "updatedAt": "2025-01-16T10:30:00"
}
```

### Listar Todas las Personas
**GET** `/api/personas`

**Respuesta (200):**
```json
[
  {
    "id": 1,
    "nombre": "Juan",
    "apellido": "Pérez",
    "email": "juan@email.com",
    "telefono": "+123456789",
    "direccion": "Calle 123, Ciudad",
    "createdAt": "2025-01-16T10:30:00",
    "updatedAt": "2025-01-16T10:30:00"
  }
]
```

### Obtener Persona por ID
**GET** `/api/personas/{id}`

**Respuesta (200):** Persona encontrada
**Respuesta (404):** Persona no encontrada

### Actualizar Persona
**PUT** `/api/personas/{id}`

```json
{
  "nombre": "Juan Carlos",
  "apellido": "Pérez García",
  "email": "juan.carlos@email.com",
  "telefono": "+987654321",
  "direccion": "Nueva Dirección 456"
}
```

**Respuesta (200):** Persona actualizada
**Respuesta (404):** Persona no encontrada
**Respuesta (400):** Email ya existe en otra persona

### Eliminar Persona
**DELETE** `/api/personas/{id}`

**Respuesta (204):** Eliminada exitosamente
**Respuesta (404):** Persona no encontrada

## Ejemplos con cURL

### Crear una persona:
```bash
curl -X POST http://localhost:8080/api/personas \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María",
    "apellido": "García",
    "email": "maria@email.com",
    "telefono": "+555123456",
    "direccion": "Avenida Principal 789"
  }'
```

### Listar todas las personas:
```bash
curl http://localhost:8080/api/personas
```

### Obtener una persona por ID:
```bash
curl http://localhost:8080/api/personas/1
```

### Actualizar una persona:
```bash
curl -X PUT http://localhost:8080/api/personas/1 \
  -H "Content-Type: application/json" \
  -d '{
    "nombre": "María Elena",
    "apellido": "García López",
    "email": "maria.elena@email.com",
    "telefono": "+555999888",
    "direccion": "Nueva dirección actualizada"
  }'
```

### Eliminar una persona:
```bash
curl -X DELETE http://localhost:8080/api/personas/1
```

## Estructura del Proyecto

```
src/
└── main/
    ├── java/
    │   └── com/
    │       └── agenda/
    │           └── api/
    │               ├── AgendaApiApplication.java (clase principal)
    │               ├── model/
    │               │   └── Persona.java
    │               ├── repository/
    │               │   └── PersonaRepository.java
    │               └── controller/
    │                   └── PersonaController.java
    └── resources/
        └── application.properties
```

## Características Implementadas

- ✅ CRUD completo para entidad Persona
- ✅ Validaciones de entrada (email único, campos obligatorios)
- ✅ Manejo de errores HTTP apropiados
- ✅ Conexión a MySQL existente
- ✅ Timestamps automáticos (created_at, updated_at)
- ✅ Logs SQL para debugging
- ✅ Arquitectura limpia con separación de responsabilidades

## Notas Técnicas

- La aplicación usa `hibernate.ddl-auto=none` para no modificar la estructura de la base de datos existente
- Los timestamps se manejan automáticamente con `@CreationTimestamp` y `@UpdateTimestamp`
- Se incluye validación de email duplicado tanto en creación como en actualización
- Los logs SQL están habilitados para facilitar el debugging durante desarrollo