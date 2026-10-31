"""
API de Inventario y Pedidos - Taller 3
Comercial Andina Digital S.A.S.

Expone mediante API REST la consulta de inventario y el estado de pedidos
que hoy viven en el ERP heredado (adaptador simulado en memoria).

Ejecutar:  uvicorn app.main:app --reload
Docs:      http://localhost:8000/docs
Contrato:  http://localhost:8000/openapi.json
"""

import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, Field

SECRET_KEY = os.getenv("JWT_SECRET", "clave-de-desarrollo-cambiar-en-produccion")
ALGORITHM = "HS256"
MINUTOS_EXPIRACION = 15

app = FastAPI(
    title="API de Inventario y Pedidos",
    version="1.0.0",
    description="Integración del ERP heredado de Comercial Andina Digital S.A.S. "
                "con el portal web y la aplicación móvil.",
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")

# --------------------------------------------------------------------------
# Usuarios de demostración (en producción: proveedor de identidad)
# --------------------------------------------------------------------------
USUARIOS = {
    "analista": {"password": "Andina2026!", "rol": "consulta"},
    "bodega": {"password": "Bodega2026!", "rol": "consulta"},
}


# --------------------------------------------------------------------------
# Modelos
# --------------------------------------------------------------------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int = Field(description="Segundos de vigencia del token")


class Producto(BaseModel):
    sku: str
    nombre: str
    stock: int
    bodega: str


class Pedido(BaseModel):
    pedido_id: int
    estado: str
    cliente: str
    total: float


# --------------------------------------------------------------------------
# Adaptador del sistema heredado (ERP). En producción sería una consulta
# a la base de datos del ERP a través de la red privada o la VPN.
# --------------------------------------------------------------------------
ERP_PRODUCTOS = {
    "AUR-001": {"sku": "AUR-001", "nombre": "Auriculares inalámbricos", "stock": 42, "bodega": "Guayaquil"},
    "TEC-014": {"sku": "TEC-014", "nombre": "Teclado mecánico", "stock": 8, "bodega": "Quito"},
    "OFI-207": {"sku": "OFI-207", "nombre": "Silla ergonómica", "stock": 0, "bodega": "Cuenca"},
}

ERP_PEDIDOS = {
    1001: {"pedido_id": 1001, "estado": "en camino", "cliente": "Ferretería del Sur", "total": 452.90},
    1002: {"pedido_id": 1002, "estado": "entregado", "cliente": "Oficinas Andinas", "total": 1280.00},
}


def crear_token(usuario: str, rol: str) -> tuple[str, int]:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    payload = {"sub": usuario, "rol": rol, "exp": expira, "iss": "api-andina"}
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM), MINUTOS_EXPIRACION * 60


def verificar_token(token: Annotated[str, Depends(oauth2_scheme)]) -> dict:
    credenciales_invalidas = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido o expirado",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise credenciales_invalidas
    if not payload.get("sub"):
        raise credenciales_invalidas
    return payload


# --------------------------------------------------------------------------
# Endpoints
# --------------------------------------------------------------------------
@app.post("/api/v1/token", response_model=Token, tags=["Autenticación"],
          summary="Obtiene un token de acceso")
def obtener_token(formulario: Annotated[OAuth2PasswordRequestForm, Depends()]):
    usuario = USUARIOS.get(formulario.username)
    if not usuario or usuario["password"] != formulario.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token, segundos = crear_token(formulario.username, usuario["rol"])
    return Token(access_token=token, expires_in=segundos)


@app.get("/api/v1/productos", response_model=list[Producto], tags=["Inventario"],
         summary="Lista los productos del catálogo")
def listar_productos(_: Annotated[dict, Depends(verificar_token)]):
    return list(ERP_PRODUCTOS.values())


@app.get("/api/v1/productos/{sku}", response_model=Producto, tags=["Inventario"],
         summary="Consulta el stock de un producto")
def consultar_producto(sku: str, _: Annotated[dict, Depends(verificar_token)]):
    producto = ERP_PRODUCTOS.get(sku.upper())
    if producto is None:
        raise HTTPException(status_code=400, detail="Producto no encontrado")
    return producto


@app.get("/api/v1/pedidos/{pedido_id}", response_model=Pedido, tags=["Pedidos"],
         summary="Consulta el estado de un pedido")
def consultar_pedido(pedido_id: int, _: Annotated[dict, Depends(verificar_token)]):
    pedido = ERP_PEDIDOS.get(pedido_id)
    if pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido


@app.get("/health", tags=["Operación"], summary="Verificación de disponibilidad")
def health():
    return {"estado": "ok", "version": app.version}
