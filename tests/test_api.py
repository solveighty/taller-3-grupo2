"""Pruebas automatizadas de la API (Taller 3)."""

import os
import sys

from fastapi.testclient import TestClient

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.main import app  # noqa: E402

cliente = TestClient(app)


def obtener_token() -> str:
    respuesta = cliente.post(
        "/api/v1/token",
        data={"username": "analista", "password": "Andina2026!"},
    )
    assert respuesta.status_code == 200
    return respuesta.json()["access_token"]


def test_sin_token_es_rechazado():
    """Un endpoint protegido sin token debe responder 401."""
    respuesta = cliente.get("/api/v1/productos")
    assert respuesta.status_code == 401


def test_token_invalido_es_rechazado():
    """Un token con firma incorrecta debe responder 401."""
    respuesta = cliente.get(
        "/api/v1/productos",
        headers={"Authorization": "Bearer token.falso.invalido"},
    )
    assert respuesta.status_code == 401


def test_token_valido_permite_consultar():
    """Con un token válido el listado responde 200 y devuelve productos."""
    token = obtener_token()
    respuesta = cliente.get(
        "/api/v1/productos",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert respuesta.status_code == 200
    assert len(respuesta.json()) == 3


def test_recurso_inexistente_devuelve_404():
    """Consultar un SKU que no existe debe responder 404."""
    token = obtener_token()
    respuesta = cliente.get(
        "/api/v1/productos/NO-EXISTE",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert respuesta.status_code == 404
    assert respuesta.json()["detail"] == "Producto no encontrado"


def test_pedido_existente_responde_200():
    """La consulta de un pedido existente devuelve su estado."""
    token = obtener_token()
    respuesta = cliente.get(
        "/api/v1/pedidos/1001",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert respuesta.status_code == 200
    assert respuesta.json()["estado"] == "en camino"


def test_credenciales_incorrectas_no_entregan_token():
    """Credenciales inválidas en /token deben responder 401."""
    respuesta = cliente.post(
        "/api/v1/token",
        data={"username": "analista", "password": "incorrecta"},
    )
    assert respuesta.status_code == 401
