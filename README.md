# API de Inventario y Pedidos

API REST desarrollada con FastAPI para exponer la consulta de inventario y el estado
de pedidos del ERP heredado de **Comercial Andina Digital S.A.S.**

## Requisitos

- Python 3.11 o superior
- Dependencias de `requirements.txt`

## Ejecución

```bash
pip install -r requirements.txt
uvicorn app.main:app --reload
```

- Documentación interactiva: http://localhost:8000/docs
- Contrato OpenAPI: http://localhost:8000/openapi.json

## Autenticación

1. Solicitar el token en `POST /api/v1/token` con usuario `analista` y contraseña `Andina2026!`.
2. Enviar el token en cada solicitud: `Authorization: Bearer <token>`.
3. El token expira a los 15 minutos; si no es válido, la API responde 401.

## Pruebas

```bash
pytest -v
```

## Endpoints

| Método | Ruta | Descripción | Protegido |
|---|---|---|---|
| POST | /api/v1/token | Obtiene un token JWT | No |
| GET | /api/v1/productos | Lista el catálogo | Sí |
| GET | /api/v1/productos/{sku} | Consulta el stock de un producto | Sí |
| GET | /api/v1/pedidos/{pedido_id} | Consulta el estado de un pedido | Sí |
| GET | /health | Disponibilidad del servicio | No |

## Integración continua

El archivo `.github/workflows/ci.yml` ejecuta las pruebas en cada push y en cada
pull request mediante GitHub Actions.
