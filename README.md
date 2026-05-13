# CentralLog

---
### Grupo 0
```text
Aaron Reveco - 10208
Buttini Cristobal - 9976
Ricardo Sosa - 10255
```
---

# Descripción

CentralLog es una API REST desarrollada en Python utilizando FastAPI que permite recibir, almacenar y consultar logs provenientes de diferentes sistemas o servicios.

# Tecnologías utilizadas

## Backend

* Python
* FastAPI
* SQLAlchemy
* Alembic

## Bases de datos

* PostgreSQL (fase 1)
* MongoDB    (fase 2)

## Infraestructura

* Docker
* Docker Compose

---

# Arquitectura del proyecto

```text
Simulador de logs
        ↓
     FastAPI
        ↓
 ┌───────────────┐
 │ PostgreSQL    │
 │ MongoDB       │
 └───────────────┘
```

---

# Objetivo del sistema

El sistema permite:

* Centralizar eventos y logs.
* Registrar errores y auditorías.
* Consultar información histórica.
* Analizar actividad de servicios.
* Realizar búsquedas optimizadas.
* Gestionar grandes volúmenes de datos.
---

# Endpoints principales

| Método | Endpoint     | Descripción            |
| ------ | ------------ | ---------------------- |
| POST   | /logs        | Registrar un log       |
| GET    | /logs        | Obtener logs           |
| GET    | /logs/errors | Obtener errores        |
| GET    | /stats       | Estadísticas generales |

---

# Base de datos relacional

PostgreSQL se utiliza para:

* Usuarios
* Servicios
* Auditorías
* Metadatos

---

# Base de datos NoSQL

MongoDB se utiliza para:

* Almacenamiento flexible de logs
* Payloads variables
* Eventos masivos

## Justificación

Los logs poseen estructuras variables y un gran volumen de datos. MongoDB permite almacenar eventos flexibles sin necesidad de modificar constantemente el esquema relacional.


# Seguridad

El proyecto implementa:

* Variables de entorno
* Consultas parametrizadas
* ORM
* Validación de datos
* Manejo seguro de credenciales

---

# Backup & Restore

Se incluyen scripts para:

* Backup automático
* Restauración de la base de datos


---

# Estructura del proyecto

```text
app/
│
├── api/
├── models/
├── schemas/
├── repositories/
├── services/
├── database/
├── scripts/
│   ├── backup.sh
│   └── restore.sh
│
├── main.py
└── requirements.txt
```

---

# Instalación

## Clonar repositorio

```bash
git clone <repository_url>
```

---

## Crear entorno virtual

```bash
python -m venv venv
```

---

## Activar entorno virtual

### Windows

```bash
venv\Scripts\activate
```

---

## Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# Ejecutar aplicación

```bash
fastapi dev
uvicorn app.main:app --reload

```

---

# Swagger (frontend propio de FastApi)

Documentación automática:

```text
http://localhost:8000/docs
```
