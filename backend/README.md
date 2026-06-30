# JWT Authentication API — Backend

API REST construida con **Python** y **FastAPI** que implementa autenticación mediante **JWT (JSON Web Tokens)**. Usa **passlib[bcrypt]** para el hashing de contraseñas y **python-jose** para la generación y verificación de tokens.

---

## Tecnologías

| Herramienta | Versión |
|---|---|
| Python | 3.11+ |
| FastAPI | ^0.111.0 |
| Uvicorn | ^0.29.0 |
| python-jose | ^3.3.0 |
| passlib[bcrypt] | ^1.7.4 |
| bcrypt | >=3.2,<4.0 |
| Poetry | gestor de dependencias |

> **Nota sobre bcrypt:** passlib 1.7.x no es compatible con bcrypt 4.x o superior, por eso se fija `bcrypt>=3.2,<4.0`.

---

## Endpoints

### `POST /token` — Login

Autentica al usuario y devuelve un access token (vigencia de **300 segundos**) y un refresh token.

**Request body (JSON):**
```json
{
  "username": "admin",
  "password": "admin123"
}
```

**Response:**
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

### `POST /token/refresh` — Refrescar token

Recibe un refresh token válido y devuelve un nuevo access token y refresh token.

**Request body (JSON):**
```json
{
  "refresh_token": "<refresh_jwt>"
}
```

**Response:**
```json
{
  "access_token": "<nuevo_jwt>",
  "refresh_token": "<nuevo_refresh_jwt>",
  "token_type": "bearer",
  "expires_in": 300
}
```

---

## Documentación interactiva

Cuando la aplicación esté en ejecución, accede a la documentación Swagger en:

```
http://localhost:8000/docs
```

---

## Variables de entorno

| Variable | Descripción | Valor por defecto |
|---|---|---|
| `SECRET_KEY` | Clave secreta para firmar los JWT. **Cámbiala en producción.** | `supersecretkey_change_in_production` |

---

## Ejecución con Docker (recomendado)

### Requisitos previos
- [Docker](https://docs.docker.com/get-docker/) instalado
- [Docker Compose](https://docs.docker.com/compose/install/) instalado

### Pasos

```bash
# Desde la carpeta backend/
cd backend

# Construir la imagen y levantar el contenedor
docker compose up --build
```

La API estará disponible en `http://localhost:8000`.

Para detener:
```bash
docker compose down
```

---

## Ejecución local con Poetry

### Requisitos previos
- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation) instalado

### Pasos

```bash
# Desde la carpeta backend/
cd backend

# Instalar dependencias
poetry install

# Iniciar el servidor de desarrollo
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

---

## Ejemplo de uso con curl

### 1. Obtener tokens

```bash
curl -X POST http://localhost:8000/token \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'
```

### 2. Refrescar el access token

```bash
curl -X POST http://localhost:8000/token/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "<refresh_token_obtenido_anteriormente>"}'
```

---

## Estructura del proyecto

```
backend/
├── app/
│   ├── __init__.py
│   ├── auth.py          # Lógica de JWT y hashing de contraseñas
│   ├── main.py          # Aplicación FastAPI y endpoints
│   └── models.py        # Modelos Pydantic (request/response)
├── docker-compose.yml
├── Dockerfile
├── pyproject.toml       # Configuración de Poetry
└── README.md
```
