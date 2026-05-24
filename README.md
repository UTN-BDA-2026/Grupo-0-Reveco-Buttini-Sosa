# NEXO

---

### Grupo 0

```text
Aaron Reveco      - 10208
Buttini Cristobal - 9976
Ricardo Sosa      - 10255
```

---

## Descripción

API desarrollada en Python con FastAPI que permite gestionar la autenticación y sesiones de usuarios. Centraliza el registro, login, validación de tokens y cierre de sesión, pudiendo ser consumida por cualquier sistema externo que necesite autenticar usuarios.

---

## Tecnologías utilizadas

### Backend

- Python
- FastAPI
- SQLAlchemy (ORM)
- Passlib + bcrypt (hasheo de contraseñas)
- PyJWT (generación y validación de tokens)

### Bases de datos

- PostgreSQL — usuarios (datos estructurados y críticos)
- MongoDB — sesiones activas (JSON variables)

---

## Arquitectura del proyecto

```text
Cliente (cualquier sistema externo)
            ↓
         FastAPI
            ↓
 ┌──────────────────────────┐
 │  PostgreSQL              │
 │  · Usuarios              │
 ├──────────────────────────┤
 │  MongoDB                 │
 │  · Sesiones activas      │
 │  · Metadata de sesiones  │
 └──────────────────────────┘
```

---

## Objetivo del sistema

- Registrar y gestionar usuarios.
- Autenticar credenciales y emitir tokens JWT.
- Almacenar sesiones con metadata variable por dispositivo en MongoDB.
- Validar tokens activos y cerrar sesiones.
- Auditar accesos e intentos de autenticación.
- Separar datos estructurados (Postgres) de datos flexibles (MongoDB).

---

## Endpoints principales

### Usuarios

| Método   | Endpoint       | Descripción                              | Body requerido                                              |
| -------- | -------------- | ---------------------------------------- | ----------------------------------------------------------- |
| `POST`   | `/users/`      | Registrar un nuevo usuario               | `name`, `surname`, `username`, `email`, `password`          |
| `GET`    | `/users/{id}`  | Obtener usuario por ID                   | —                                                           |
| `PUT`    | `/users/{id}`  | Modificar datos de un usuario            | Cualquier campo: `name`, `surname`, `username`, `email`, `password` |
| `DELETE` | `/users/{id}`  | Eliminar un usuario                      | —                                                           |

### Autenticación

| Método | Endpoint         | Descripción                              | Body requerido             |
| ------ | ---------------- | ---------------------------------------- | -------------------------- |
| `POST` | `/auth/login`    | Autenticar usuario y obtener token JWT   | `email`, `password`        |
| `GET`  | `/auth/validate` | Validar si un token sigue activo         | `token` (query param)      |
| `POST` | `/auth/logout`   | Cerrar sesión e invalidar token          | `token` (query param)      |

### Ejemplo de respuesta exitosa — Login

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "cristobalbuttini33"
}
```

### Ejemplo de respuesta — Sesión fallida

```json
{
  "detail": "Credenciales incorrectas"
}
```

---

## Base de datos relacional — PostgreSQL

PostgreSQL almacena los datos estructurados y críticos del sistema:

- **users** — id, name, surname, username, email, password hasheado, created_at

### Justificación

Los datos de usuarios tienen estructura fija y requieren consistencia transaccional.

---

## Base de datos NoSQL — MongoDB

MongoDB almacena las sesiones activas con su metadata variable:

```json
{
  "user_id": 42,
  "username": "cristobalbuttini33",
  "status": "success",
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "created_at": "2026-05-17T10:30:00",
  "expires_at": "2026-05-17T11:30:00",
  "ip_address": "190.120.45.22",
  "is_active": true
}
```

### Justificación

Cada sesión puede tener campos completamente distintos según el resultado del login. Un login exitoso tiene `token` y `expires_at`, uno fallido tiene `reason`. MongoDB permite almacenar esta estructura variable sin necesidad de columnas opcionales en una tabla relacional.

---

## Características implementadas


### Índices

- Índice sobre `email` en la tabla `users` — optimiza la búsqueda al momento del login.
- Índice sobre `username` en la tabla `users` — optimiza la validación de duplicados al registrarse.

### Transacciones

- Todas las operaciones de escritura en PostgreSQL (`create`, `update`, `delete`) se ejecutan dentro de una transacción explícita con `commit` y `rollback`. Si algo falla a mitad del proceso, la base de datos vuelve al estado anterior.

### Seguridad

- Contraseñas hasheadas con bcrypt — nunca se almacena texto plano.
- Tokens JWT con expiración de 1 hora.
- Variables de entorno para credenciales y claves secretas.
- Consultas parametrizadas via SQLAlchemy.
- Validación de datos de entrada con Pydantic.

### ORM y Sin ORM

- SQLAlchemy como ORM para PostgreSQL — mapea los modelos Python a tablas relacionales.
- PyMongo directo (sin ORM) para MongoDB — acceso flexible a documentos JSON sin esquema fijo.

### Backup & Restore

Scripts incluidos para backup y restauración de PostgreSQL sin dependencias externas:

```bash
# Hacer backup
python scripts/backup.py

# Restaurar desde el backup más reciente
python scripts/restore.py
```

Los backups se guardan en la carpeta `backups/` con timestamp:

```
backups/
└── postgres_20260524_120000.json
```

---

## Estructura del proyecto

```text
Nexo/
│
├── app/
│   ├── database/
│   │   ├── database.py       # Conexión y sesión PostgreSQL
│   │   └── mongo.py          # Conexión MongoDB
│   │
│   ├── models/
│   │   └── user.py           # Modelo ORM de la tabla users
│   │
│   ├── schemas/
│   │   └── user.py           # Validación de datos con Pydantic
│   │
│   ├── repositories/
│   │   ├── user.py           # CRUD de usuarios en PostgreSQL
│   │   └── session.py        # Gestión de sesiones en MongoDB
│   │
│   ├── services/
│   │   ├── user.py           # Lógica de negocio de usuarios
│   │   └── auth.py           # Lógica de autenticación
│   │
│   ├── routes/
│   │   ├── user.py           # Endpoints de usuarios
│   │   └── auth.py           # Endpoints de autenticación
│   │
│   └── utils/
│       ├── hash.py           # Hasheo y verificación de contraseñas
│       └── jwt.py            # Generación y validación de tokens JWT
│
├── scripts/
│   ├── seed.py               # Carga 200 usuarios de prueba
│   ├── backup.py             # Backup de PostgreSQL
│   └── restore.py            # Restauración de PostgreSQL
│
├── backups/                  # Archivos de backup (ignorado por git)
├── main.py                   # Punto de entrada de la aplicación
├── requirements.txt          # Dependencias del proyecto
├── .env                      # Variables de entorno (ignorado por git)
└── .env.example              # Plantilla de variables de entorno
```

---

## Requisitos previos

Antes de correr la aplicación necesitás tener instalado en tu computadora:

### 1. Python 3.11 o superior

Versión 3.11 o superior. 

### 2. PostgreSQL 15 o superior


- Usuario (`postgres` por defecto) y la contraseña que configurás
- El puerto por defecto es `5432`

### 3. MongoDB 7 o superior
- Version 8.3.2
- MongoDB Compass 


### 4. Git


---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository_url>
cd Nexo
```

### 2. Crear el entorno virtual

```bash
python -m venv venv
```

### 3. Activar el entorno virtual

```bash
venv\Scripts\activate
```

### 4. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5. Configurar variables de entorno

Copiá el archivo `.env.example`, renombralo a `.env` y completá cada variable con los datos de tu computadora.

### 6. Crear la base de datos en PostgreSQL

Abrí pgAdmin o cualquier cliente de PostgreSQL y creá una base de datos llamada `Grupo-0`.

### 7. Crear la base de datos en MongoDB

Abrí MongoDB Compass y creá una base de datos llamada `Grupo-0` con una colección llamada `sessions`.

### 8. Levantar la aplicación

```bash
fastapi dev
```

Las tablas de PostgreSQL se crean automáticamente al levantar la app.

### 9. Cargar usuarios de prueba

```bash
python scripts/seed.py
```

Esto crea 200 usuarios de prueba. Todos tienen la misma contraseña: `Password123`

---

## Ejecutar la aplicación

```bash
fastapi dev
```

---

## Documentación automática (Swagger)

FastAPI genera documentación interactiva automáticamente:

```
http://localhost:8000/docs
```
