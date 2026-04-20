# Lead Management API

API robusta desarrollada con FastAPI para la gestión integral de Leads (prospectos), incluyendo análisis de datos mediante IA, estadísticas detalladas y soporte para Soft Delete.

## 🚀 Características

- **Arquitectura Limpia**: Separación de responsabilidades (Routers, Schemas, Models, Services).
- **Gestión de Leads**: CRUD completo con validaciones estrictas de Pydantic.
- **Análisis con IA**: Generación de resúmenes ejecutivos usando OpenAI (con soporte de mock).
- **Soft Delete**: Los registros no se borran físicamente, permitiendo auditoría.
- **Estadísticas**: Endpoint dedicado para métricas de negocio.
- **Seguridad**: Autenticación mediante **API Key** (header `X-API-Key`).
- **Rate Limiting**: Protección contra abusos limitando peticiones por IP.
- **Documentación**: Swagger interactivo integrado.

## 🛠️ Tecnologías Usadas

- **Python 3.10+**
- **FastAPI**: Framework web de alto rendimiento.
- **SQLAlchemy**: ORM para gestión de base de datos.
- **SlowAPI**: Implementación de Rate Limiting.
- **MySQL / SQLite**: Compatible con múltiples motores.
- **OpenAI**: Integración de inteligencia artificial.
- **Pydantic**: Validación de datos y esquemas.

## 📋 Requisitos Previos

- Python 3.10 o superior.
- MySQL Server (opcional, configurado por defecto en `.env`).

## 🔧 Instalación y Configuración

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/arizaguaca/prueba-tecnica-omc.git
   cd prueba-tecnica-omc
   ```

2. **Crear y activar entorno virtual:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar variables de entorno:**
   Copia el archivo `.env.example` a `.env` y ajusta tus credenciales:
   ```bash
   cp .env.example .env
   ```

## 🗄️ Esquema de la Base de Datos

La tabla principal `leads` tiene la siguiente estructura:

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | UUID (String 36) | Identificador único universal. |
| `nombre` | VARCHAR(255) | Nombre del prospecto (mín. 2 caracteres). |
| `email` | VARCHAR(255) | Correo electrónico único. |
| `telefono` | VARCHAR(50) | Número de contacto. |
| `fuente` | ENUM | instagram, facebook, landing_page, referido, otro. |
| `producto_interes` | VARCHAR(255) | Producto de interés del lead. |
| `presupuesto` | FLOAT | Presupuesto estimado. |
| `created_at` | DATETIME | Fecha de creación. |
| `updated_at` | DATETIME | Fecha de última actualización. |
| `deleted_at` | DATETIME | Fecha de borrado lógico (Soft Delete). |

## 🚀 Ejecución

### 1. Inicializar la Base de Datos
El proyecto está configurado para crear las tablas automáticamente al iniciar la aplicación mediante SQLAlchemy (`Base.metadata.create_all`).

### 2. Poblar con datos de prueba (Seed)
Ejecuta el script de seed para insertar 10 leads aleatorios usando Faker:
```bash
python scripts/seed.py
```

### 3. Correr la API
Inicia el servidor de desarrollo:
```bash
python -m app.main
```
O usando uvicorn directamente:
```bash
uvicorn app.main:app --reload
```

## 🧪 Pruebas (Testing)

El proyecto incluye una suite de pruebas automatizadas con `pytest`. Para ejecutarlas:

```bash
./venv/bin/pytest tests/test_leads.py
```
*Las pruebas utilizan una base de datos SQLite en memoria para no afectar los datos reales.*

## 📖 Documentación

Una vez iniciada la aplicación, puedes acceder a la documentación interactiva:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## ⚡ Ejemplos de Uso (cURL)

### 1. Crear un Lead
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/leads/' \
  -H 'X-API-Key: omc_secret_key_123' \
  -H 'Content-Type: application/json' \
  -d '{
  "nombre": "Juan Perez",
  "email": "juan.perez@example.com",
  "telefono": "+573001234567",
  "fuente": "instagram",
  "producto_interes": "Consultoría Tech",
  "presupuesto": 1500.0
}'
```

### 2. Listado con Paginación y Filtros
```bash
curl -X 'GET' \
  -H 'X-API-Key: omc_secret_key_123' \
  'http://localhost:8000/api/v1/leads/?page=1&limit=10&fuente=facebook'
```

### 3. Obtener Estadísticas
```bash
curl -X 'GET' \
  -H 'X-API-Key: omc_secret_key_123' \
  'http://localhost:8000/api/v1/leads/stats'
```

### 4. Actualizar un Lead (PATCH)
```bash
curl -X 'PATCH' \
  'http://localhost:8000/api/v1/leads/<ID>' \
  -H 'X-API-Key: omc_secret_key_123' \
  -H 'Content-Type: application/json' \
  -d '{"presupuesto": 2500.0}'
```

### 5. Borrado Lógico (DELETE)
```bash
curl -X 'DELETE' \
  -H 'X-API-Key: omc_secret_key_123' \
  'http://localhost:8000/api/v1/leads/<ID>'
```

### 7. Webhook (Simulando Typeform)
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/leads/webhook' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_id": "Lt679p92",
  "event_type": "form_response",
  "form_response": {
    "answers": [
      { "type": "text", "text": "Cliente Webhook", "field": { "ref": "nombre" } },
      { "type": "email", "email": "webhook.user@example.com", "field": { "ref": "email" } },
      { "type": "number", "number": 1200, "field": { "ref": "presupuesto" } }
    ]
  }
}'
```

## 🤖 Endpoint de IA
Para usar el endpoint `POST /leads/ai/summary`, asegúrate de tener una `OPENAI_API_KEY` válida en tu archivo `.env`. Si no se proporciona, la API devolverá una respuesta **Mock** predefinida para demostración.

## 🌐 Despliegue en Railway

La API se encuentra desplegada y operativa en la siguiente URL:
**[https://prueba-tecnica-omc-production.up.railway.app](https://prueba-tecnica-omc-production.up.railway.app)**

- **Documentación Swagger**: [https://prueba-tecnica-omc-production.up.railway.app/docs](https://prueba-tecnica-omc-production.up.railway.app/docs)
- **Base API URL**: `https://prueba-tecnica-omc-production.up.railway.app/api/v1`

## 🚀 Ejemplos de Uso en Producción (Railway)

### 1. Obtener Estadísticas (Producción)
```bash
curl -X 'GET' \
  'https://prueba-tecnica-omc-production.up.railway.app/api/v1/leads/stats' \
  -H 'X-API-Key: omc_secret_key_123'
```

### 2. Crear un Lead (Producción)
```bash
curl -X 'POST' \
  'https://prueba-tecnica-omc-production.up.railway.app/api/v1/leads/' \
  -H 'X-API-Key: omc_secret_key_123' \
  -H 'Content-Type: application/json' \
  -d '{
  "nombre": "Victor Railway",
  "email": "victor.railway@example.com",
  "fuente": "landing_page",
  "presupuesto": 3000.0
}'
```

### 3. Resumen con IA (Producción)
```bash
curl -X 'POST' \
  'https://prueba-tecnica-omc-production.up.railway.app/api/v1/leads/ai/summary' \
  -H 'X-API-Key: omc_secret_key_123'
```

### 4. Listado con Filtros (Producción)
```bash
curl -X 'GET' \
  'https://prueba-tecnica-omc-production.up.railway.app/api/v1/leads/?fuente=facebook' \
  -H 'X-API-Key: omc_secret_key_123'
```

### 5. Actualizar Lead (Producción)
```bash
curl -X 'PATCH' \
  'https://prueba-tecnica-omc-production.up.railway.app/api/v1/leads/<ID>' \
  -H 'X-API-Key: omc_secret_key_123' \
  -H 'Content-Type: application/json' \
  -d '{"presupuesto": 5000.0}'
```

### 6. Eliminar Lead - Soft Delete (Producción)
```bash
curl -X 'DELETE' \
  'https://prueba-tecnica-omc-production.up.railway.app/api/v1/leads/<ID>' \
  -H 'X-API-Key: omc_secret_key_123'
```

### 7. Webhook Typeform (Producción)
```bash
curl -X 'POST' \
  'https://prueba-tecnica-omc-production.up.railway.app/api/v1/leads/webhook' \
  -H 'Content-Type: application/json' \
  -d '{
  "event_id": "pro_123",
  "event_type": "form_response",
  "form_response": {
    "answers": [
      { "type": "text", "text": "Lead Railway", "field": { "ref": "nombre" } },
      { "type": "email", "email": "prod@example.com", "field": { "ref": "email" } }
    ]
  }
}'
```

---
Desarrollado como prueba técnica para OMC.