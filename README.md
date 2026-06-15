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

NEXO es una API REST desarrollada en Python con FastAPI que actúa como microservicio de autenticación y gestión de usuarios para sistemas universitarios. Centraliza el registro, login, validación de tokens y cierre de sesión, pudiendo ser consumida por cualquier sistema externo — como un sistema de gestión académica tipo Sysacad.

---

## Tecnologías utilizadas

**Backend:** Python, FastAPI, SQLAlchemy (ORM), Alembic (migraciones), Passlib + bcrypt, PyJWT

**Bases de datos:** PostgreSQL (datos estructurados) · MongoDB (sesiones JSON variables)

---

## Arquitectura

```text
Cliente (cualquier sistema externo)
            ↓
         FastAPI
            ↓
 ┌──────────────────────────┐
 │  PostgreSQL              │
 │  · Roles                 │
 │  · Usuarios              │
 │  · Alumnos               │
 │  · Docentes              │
 │  · Administrativos       │
 ├──────────────────────────┤
 │  MongoDB                 │
 │  · Sesiones activas      │
 └──────────────────────────┘
```

---

## Objetivo del sistema

- Registrar y gestionar usuarios con roles (alumno, docente, administrativo).
- Autenticar credenciales y emitir tokens JWT con expiración de 1 hora.
- Almacenar sesiones con metadata variable en MongoDB.
- Validar tokens activos y cerrar sesiones.
- Auditar accesos exitosos y fallidos.

---

## Endpoints principales

<details>
<summary>Usuarios</summary>

| Método   | Endpoint       | Descripción                   | Body requerido                                                      |
| -------- | -------------- | ----------------------------- | ------------------------------------------------------------------- |
| `POST`   | `/users/`      | Registrar un nuevo usuario    | `name`, `surname`, `username`, `email`, `password`, `role_id`       |
| `GET`    | `/users/{id}`  | Obtener usuario por ID        | —                                                                   |
| `PUT`    | `/users/{id}`  | Modificar datos de un usuario | Cualquier campo: `name`, `surname`, `username`, `email`, `password` |
| `DELETE` | `/users/{id}`  | Eliminar un usuario           | —                                                                   |

</details>

<details>
<summary>Roles</summary>

| Método | Endpoint      | Descripción            | Body requerido        |
| ------ | ------------- | ---------------------- | --------------------- |
| `POST` | `/roles/`     | Crear un rol           | `name`, `description` |
| `GET`  | `/roles/`     | Listar todos los roles | —                     |
| `GET`  | `/roles/{id}` | Obtener rol por ID     | —                     |

</details>

<details>
<summary>Alumnos</summary>

| Método | Endpoint              | Descripción                 | Body requerido                      |
| ------ | --------------------- | --------------------------- | ----------------------------------- |
| `POST` | `/students/{user_id}` | Crear perfil de alumno      | `legajo`, `carrera`, `anio_ingreso` |
| `GET`  | `/students/{user_id}` | Obtener perfil de alumno    | —                                   |
| `PUT`  | `/students/{user_id}` | Actualizar perfil de alumno | `carrera`, `anio_ingreso`           |

</details>

<details>
<summary>Docentes</summary>

| Método | Endpoint              | Descripción                  | Body requerido                     |
| ------ | --------------------- | ---------------------------- | ---------------------------------- |
| `POST` | `/teachers/{user_id}` | Crear perfil de docente      | `legajo`, `departamento`, `titulo` |
| `GET`  | `/teachers/{user_id}` | Obtener perfil de docente    | —                                  |
| `PUT`  | `/teachers/{user_id}` | Actualizar perfil de docente | `departamento`, `titulo`           |

</details>

<details>
<summary>Administrativos</summary>

| Método | Endpoint           | Descripción                      | Body requerido          |
| ------ | ------------------ | -------------------------------- | ----------------------- |
| `POST` | `/staff/{user_id}` | Crear perfil de administrativo   | `legajo`, `sector`, `cargo` |
| `GET`  | `/staff/{user_id}` | Obtener perfil de administrativo | —                       |
| `PUT`  | `/staff/{user_id}` | Actualizar perfil administrativo | `sector`, `cargo`       |

</details>

<details>
<summary>Autenticación</summary>

| Método | Endpoint         | Descripción                            | Body requerido        |
| ------ | ---------------- | -------------------------------------- | --------------------- |
| `POST` | `/auth/login`    | Autenticar usuario y obtener token JWT | `email`, `password`   |
| `GET`  | `/auth/validate` | Validar si un token sigue activo       | `token` (query param) |
| `POST` | `/auth/logout`   | Cerrar sesión e invalidar token        | `token` (query param) |

**Respuesta exitosa — Login:**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": 1,
  "username": "cristobalbuttini33"
}
```

</details>

---

## Base de datos relacional — PostgreSQL

- **roles** — id, name, description, created_at
- **users** — id, name, surname, username, email, password hasheado, role_id, created_at
- **students** — id, user_id, legajo, carrera, anio_ingreso *(tabla particionada)*
- **teachers** — id, user_id, legajo, departamento, titulo
- **staff** — id, user_id, legajo, sector, cargo

Los datos tienen estructura fija y requieren consistencia transaccional. Crear un usuario y su perfil ocurre en una sola transacción o no ocurre.

---

## Base de datos NoSQL — MongoDB

MongoDB almacena las sesiones activas. La estructura varía según el resultado del login — un login exitoso incluye `token` y `expires_at`, uno fallido incluye `reason`. Esto justifica el uso de un documento flexible en lugar de columnas opcionales en una tabla relacional.

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

---

## Características implementadas

### Índices
- `users` — índices sobre `id` (primary key), `email` y `username`. Los índices sobre `email` y `username` optimizan la búsqueda al momento del login y el registro.
- `students`, `teachers`, `staff` — índice sobre `legajo` en cada tabla para búsquedas rápidas por número de legajo.

### Particionado
La tabla `students` está particionada por `anio_ingreso` mediante Alembic. Se generaron 8 particiones para los años 2018-2025. Las consultas por cohorte solo leen la partición correspondiente.

### Transacciones
Todas las operaciones de escritura en PostgreSQL usan transacciones explícitas con `commit` y `rollback`. Si algo falla, la base de datos vuelve al estado anterior.

### Seguridad
Contraseñas hasheadas con bcrypt, tokens JWT con expiración, variables de entorno para credenciales, consultas parametrizadas via SQLAlchemy y validación de datos con Pydantic.

### ORM y Sin ORM
SQLAlchemy como ORM para PostgreSQL. 

PyMongo directo (sin ORM) para MongoDB.

### Backup & Restore

```bash
python scripts/backup.py    # Hacer backup
python scripts/restore.py   # Restaurar desde el backup más reciente
```

Los backups se guardan en `backups/` con timestamp.

---

## Estructura del proyecto

```text
Nexo/
├── app/
│   ├── database/         # Conexión a PostgreSQL y MongoDB
│   ├── models/           # Modelos ORM de cada entidad
│   ├── schemas/          # Validación de datos con Pydantic
│   ├── repositories/     # Acceso y persistencia de datos
│   ├── services/         # Lógica de negocio
│   ├── routes/           # Endpoints de la API
│   └── utils/            # Hasheo y JWT
├── migrations/
│   ├── env.py            # Configuración de Alembic
│   ├── versions/         # Archivos de migración
│   └── README            # Documentación de migraciones
├── scripts/
│   ├── seed.py           # Carga datos de prueba
│   ├── backup.py         # Backup de PostgreSQL
│   └── restore.py        # Restauración de PostgreSQL
├── frontend/
│   └── index.html        # Frontend demostrativo
├── backups/              # Archivos de backup (ignorado por git)
├── main.py
├── alembic.ini
├── requirements.txt
├── .env.example
└── .gitignore
```

---

## Requisitos previos

- **Python 3.11+** — marcá "Add Python to PATH" durante la instalación
- **PostgreSQL 15+** — incluye pgAdmin; recordá el usuario y contraseña que configurás
- **MongoDB 7+** — instalá también MongoDB Compass
- **Git**

---

## Instalación

### 1. Clonar el repositorio

```bash
git clone <repository_url>
cd Nexo
```

### 2. Crear y activar el entorno virtual

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Copiá `.env.example`, renombralo a `.env` y completá con los datos de tu computadora.

### 5. Crear las bases de datos

- **PostgreSQL** — en pgAdmin creá una base de datos llamada `Grupo-0`
- **MongoDB** — en MongoDB Compass creá una base de datos `Grupo-0` con colección `sessions`

### 6. Levantar la aplicación

```bash
fastapi dev
```

Las tablas de PostgreSQL se crean automáticamente.

### 7. Aplicar migraciones

```bash
alembic upgrade head
```

### 8. Cargar datos de prueba

```bash
python scripts/seed.py
```

Crea 3 roles y 200 usuarios. Contraseña de todos: `Contraseña123`

### 9. Backup & Restore

Para hacer un backup del estado actual de la base de datos:

```bash
python scripts/backup.py
```
La primera vez que corrés el backup la carpeta backups/ se crea automáticamente

Para restaurar desde el backup más reciente:

```bash
python scripts/restore.py
```

Los backups se guardan en la carpeta `backups/` con timestamp y cubren todas las tablas de PostgreSQL.

---

## Frontend demostrativo


Abrí `frontend/index.html` en el navegador con la API corriendo.

- Registrar un nuevo usuario seleccionando el rol (alumno o docente)
- Iniciar sesión con cualquier usuario de la base de datos
- Ver en tiempo real los datos de la sesión — token JWT, estado, hora de inicio y expiración
- Validar si el token sigue activo
- Cerrar sesión

> Este frontend es meramente explicativo. En una implementación real la información de sesión y tokens no sería visible al usuario final.
---

## Documentación automática (Swagger)

```
http://localhost:8000/docs
```