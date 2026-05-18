# API de Autenticacion y Sesiones de Usuario

---

### Grupo 0

```text
Aaron Reveco   - 10208
Buttini Cristobal - 9976
Ricardo Sosa   - 10255
```

---

## Descripción

API REST desarrollada en Python con FastAPI que permite gestionar la autenticación y sesiones de usuarios. Centraliza el registro, login, validación de tokens y cierre de sesión, pudiendo ser consumida por cualquier sistema externo que necesite autenticar usuarios.

---

## Tecnologías utilizadas

### Backend

- Python
- FastAPI
- SQLAlchemy (ORM)
- Passlib + bcrypt (hasheo de contraseñas)
- PyJWT (generación y validación de tokens)

### Bases de datos

- PostgreSQL — usuarios, roles y permisos (datos estructurados y críticos)
- MongoDB — sesiones activas y metadata variable por dispositivo

### Infraestructura


## Arquitectura del proyecto

```text
Cliente (cualquier sistema externo)
            ↓
         FastAPI
            ↓
 ┌──────────────────────────┐
 │  PostgreSQL              │
 │  · Usuarios              │
 │  · Roles                 │
 │  · Permisos              │
 ├──────────────────────────┤
 │  MongoDB                 │
 │  · Sesiones activas      │
 │  · Metadata de sesiones  │
 └──────────────────────────┘
```

---

## Objetivo del sistema

- Registrar y gestionar usuarios con roles.
- Autenticar credenciales y emitir tokens JWT.
- Almacenar sesiones con metadata variable por dispositivo (Mongo DB).
- Validar tokens activos y cerrar sesiones.
- Auditar accesos e intentos de autenticación.
- Separar datos estructurados (Postgres) de datos flexibles (MongoDB).

---

## Endpoints principales

| Método | Endpoint             | Descripción                              |
| ------ | -------------------- | ---------------------------------------- |
| POST   | /auth/register       | Registrar un nuevo usuario               |
| POST   | /auth/login          | Autenticar usuario y obtener token JWT   |
| GET    | /auth/validate       | Validar si un token sigue activo         |
| POST   | /auth/logout         | Cerrar sesión e invalidar token          |
| GET    | /users               | Listar usuarios (requiere rol admin)     |
| GET    | /users/{id}          | Obtener usuario por ID                   |
| GET    | /sessions            | Listar sesiones activas de un usuario    |

---

## Base de datos relacional — PostgreSQL

PostgreSQL almacena los datos estructurados y críticos del sistema:

- **users** — id, email, password hasheado, created_at
- **roles** — id, nombre (admin, user, moderator)
- **user_roles** — relación entre usuarios y roles

### Justificación

Los datos de usuarios y roles tienen estructura fija y requieren consistencia transaccional. Por ejemplo, crear un usuario y asignarle un rol debe ocurrir en una sola transacción o no ocurrir.

---

## Base de datos NoSQL — MongoDB

MongoDB almacena las sesiones activas con su metadata variable:

```json
{
  "session_id": "abc123xyz",
  "user_id": "42",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "created_at": "2026-05-17T10:30:00",
  "expires_at": "2026-05-17T11:30:00",
  "device": {
    "type": "mobile",
    "os": "Android 14",
    "browser": "Chrome 120",
    "app_version": "2.3.1"
  },
  "ip_address": "190.120.45.22",
  "location": {
    "country": "Argentina",
    "city": "Mendoza"
  },
  "is_active": true
}
```

### Justificación

Cada sesión puede tener campos completamente distintos según el origen (web, mobile, API key, Smart TV). MongoDB permite almacenar esta estructura variable dado por el JSON

---

## Características implementadas

### Índices

- PostgreSQL: índice sobre `email` en la tabla `users` para búsquedas rápidas al login.
- MongoDB: índice sobre `user_id` y `expires_at` para consultas de sesiones activas.

### Particionado

- La tabla de sesiones históricas en PostgreSQL se particiona por rango de fechas (`created_at`), permitiendo archivar sesiones antiguas sin degradar el rendimiento.

### Transacciones

- El registro de un usuario y la asignación de su rol se ejecutan en una única transacción en PostgreSQL.

### Seguridad

- Contraseñas hasheadas con bcrypt.
- Tokens JWT con expiración.
- Variables de entorno para credenciales y claves secretas.
- Consultas parametrizadas via SQLAlchemy.
- Validación de datos de entrada con Pydantic.

### ORM y Sin ORM

- SQLAlchemy como ORM para PostgreSQL.
- PyMongo directo (sin ORM) para MongoDB, justificando el uso de cada enfoque.

### Backup & Restore

Scripts incluidos para backup y restauración de ambas bases:

```bash
# Backup
scripts/backup.sh

# Restore
scripts/restore.sh
```

---

## Estructura del proyecto

```text
app/
│
├── config/          # Configuración general 
├── database/        # Conexión a PostgreSQL y MongoDB
├── models/          # Modelos ORM (SQLAlchemy)
├── schemas/         # Validación de datos (Pydantic)
├── repositories/    # Acceso y persistencia de datos
├── services/        # Lógica de negocio
├── routes/          # Endpoints de la API
└── utils/           # JWT, hasheo, helpers

scripts/
├── backup.sh        # Backup de PostgreSQL y MongoDB
└── restore.sh       # Restauración de ambas bases

main.py              # Punto de entrada
requirements.txt
.env.example

```

---

## Instalación

### Clonar repositorio

```bash
git clone <repository_url>
```

### Crear entorno virtual

```bash
python -m venv venv
```

### Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

### Instalar dependencias

```bash
pip install -r requirements.txt
```

### Configurar variables de entorno

```bash
cp .env.example .env
# Editar .env con tus credenciales
```

---

## Ejecutar aplicación

```bash
uvicorn app.main:app --reload
fastapi dev
```

---

## Documentación automática (Swagger)

FastAPI genera documentación interactiva automáticamente:

```
http://localhost:8000/docs
```