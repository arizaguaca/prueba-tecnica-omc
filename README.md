# Lead Management API

API robusta desarrollada con FastAPI para la gestión integral de Leads (prospectos), incluyendo análisis de datos mediante IA, estadísticas detalladas y soporte para Soft Delete.

## 🚀 Características

- **Arquitectura Limpia**: Separación de responsabilidades (Routers, Schemas, Models, Services).
- **Gestión de Leads**: CRUD completo con validaciones estrictas de Pydantic.
- **Análisis con IA**: Generación de resúmenes ejecutivos usando OpenAI (con soporte de mock).
- **Soft Delete**: Los registros no se borran físicamente, permitiendo auditoría.
- **Estadísticas**: Endpoint dedicado para métricas de negocio.
- **Documentación**: Swagger interactivo integrado.

## 🛠️ Tecnologías Usadas

- **Python 3.10+**
- **FastAPI**: Framework web de alto rendimiento.
- **SQLAlchemy**: ORM para gestión de base de datos.
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

## 📖 Documentación

Una vez iniciada la aplicación, puedes acceder a la documentación interactiva:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## ⚡ Ejemplos de Uso (cURL)

### 1. Crear un Lead
```bash
curl -X 'POST' \
  'http://localhost:8000/api/v1/leads/' \
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
curl -X 'GET' 'http://localhost:8000/api/v1/leads/?page=1&limit=10&fuente=facebook'
```

### 3. Obtener Estadísticas
```bash
curl -X 'GET' 'http://localhost:8000/api/v1/leads/stats'
```

### 4. Actualizar un Lead (PATCH)
```bash
curl -X 'PATCH' \
  'http://localhost:8000/api/v1/leads/<ID>' \
  -H 'Content-Type: application/json' \
  -d '{"presupuesto": 2500.0}'
```

### 5. Borrado Lógico (DELETE)
```bash
curl -X 'DELETE' 'http://localhost:8000/api/v1/leads/<ID>'
```

### 6. Resumen con IA
```bash
curl -X 'POST' 'http://localhost:8000/api/v1/leads/ai/summary'
```

## 🤖 Endpoint de IA
Para usar el endpoint `POST /leads/ai/summary`, asegúrate de tener una `OPENAI_API_KEY` válida en tu archivo `.env`. Si no se proporciona, la API devolverá una respuesta **Mock** predefinida para demostración.

---
Desarrollado como prueba técnica para OMC.