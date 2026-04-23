import pytest
import json
from pathlib import Path
from unittest.mock import patch, mock_open

# Importo las funciones y clases de error desde nuestro módulo principal
from tienda import (
    obtener_producto,
    calcular_subtotal,
    aplicar_descuento,
    calcular_envio,
    calcular_total,
    consultar_estado_envio,
    guardar_pedido,
    cargar_pedido,
    ProductoNoDisponibleError,
    PedidoInvalidoError
)

# ==========================================
# 3. FIXTURES (Reutilización de datos)
# ==========================================
@pytest.fixture
def pedido_valido():
    """Fixture que proporciona un pedido básico correcto."""
    return [{"producto": "raton", "cantidad": 2}]

@pytest.fixture
def pedido_complejo():
    """Fixture con varios artículos para probar el cálculo final."""
    return [
        {"producto": "teclado", "cantidad": 1},  # 25.0
        {"producto": "usb", "cantidad": 3}       # 8.0 * 3 = 24.0 (Subtotal: 49.0)
    ]

# ==========================================
# 2 y 5. PRUEBAS UNITARIAS Y EXCEPCIONES
# ==========================================
def test_obtener_producto_existe():
    producto = obtener_producto("monitor")
    assert producto["precio"] == 120.0

def test_obtener_producto_no_existe():
    # Compruebo que lanza KeyError si el producto no está en catálogo
    with pytest.raises(KeyError):
        obtener_producto("silla")

def test_calcular_subtotal_ok(pedido_valido):
    # El ratón vale 15.0, pidiendo 2 el total debe ser 30.0
    assert calcular_subtotal(pedido_valido) == 30.0

def test_calcular_subtotal_vacio():
    with pytest.raises(PedidoInvalidoError):
        calcular_subtotal([])

def test_calcular_subtotal_cantidad_negativa():
    with pytest.raises(PedidoInvalidoError):
        calcular_subtotal([{"producto": "teclado", "cantidad": -1}])

def test_calcular_subtotal_sin_stock():
    with pytest.raises(ProductoNoDisponibleError):
        # El catálogo solo tiene 10 teclados
        calcular_subtotal([{"producto": "teclado", "cantidad": 15}])

# ==========================================
# 4. PARAMETRIZACIÓN
# ==========================================
@pytest.mark.parametrize("subtotal, es_vip, cupon, esperado", [
    (100.0, False, None, 100.0),          # Sin descuentos
    (100.0, True, None, 90.0),            # 10% por VIP
    (100.0, False, "PROMO5", 95.0),       # 5% por cupón
    (100.0, False, "PROMO10", 90.0),      # 10% por cupón
    (100.0, True, "PROMO10", 80.0),       # 10% VIP + 10% Cupón = 20% máximo
    (100.0, True, "CUPON_FALSO", 90.0),   # Cupón no válido, solo aplica el 10% VIP
])
def test_aplicar_descuento(subtotal, es_vip, cupon, esperado):
    assert aplicar_descuento(subtotal, es_vip=es_vip, cupon=cupon) == esperado

@pytest.mark.parametrize("subtotal, provincia, urgente, esperado", [
    (150.0, "Madrid", False, 0.0),      # Gratis (>100, península, no urgente)
    (50.0, "Valencia", False, 6.5),     # 6.50 (<100)
    (150.0, "Canarias", False, 8.0),    # 8.00 (Envío insular, aunque >100)
    (50.0, "Baleares", True, 19.5),     # 6.50 (<100) + 8.00 (islas) + 5.00 (urgente)
])
def test_calcular_envio(subtotal, provincia, urgente, esperado):
    assert calcular_envio(subtotal, provincia, urgente=urgente) == esperado

def test_calcular_total(pedido_complejo):
    # Subtotal: 49.0
    # VIP 10% -> 44.1
    # Envío (<100, península) -> 6.5
    # Total esperado: 44.1 + 6.5 = 50.6
    total = calcular_total(pedido_complejo, "Barcelona", es_vip=True)
    assert total == 50.6

# Pruebas del servicio simulado
def test_consultar_estado_envio_ok():
    respuesta = consultar_estado_envio("OK999")
    assert respuesta["estado"] == "en reparto"
    assert respuesta["incidencia"] is False

def test_consultar_estado_envio_error_api():
    with pytest.raises(ConnectionError):
        consultar_estado_envio("FALLO_SISTEMA")

# ==========================================
# 6. MOCKING (Opción B: Ficheros de E/S)
# ==========================================
@patch("builtins.open", new_callable=mock_open)
def test_guardar_pedido(mock_archivo):
    """Pruebo que guarda el JSON sin escribir realmente en el disco duro."""
    datos = {"id": 1, "producto": "monitor"}
    resultado = guardar_pedido("dummy.json", datos)
    
    assert resultado is True
    mock_archivo.assert_called_once_with(Path("dummy.json"), "w", encoding="utf-8")

@patch("builtins.open", new_callable=mock_open, read_data='{"id": 1, "estado": "ok"}')
def test_cargar_pedido(mock_archivo):
    """Simulo que el archivo existe y contiene un JSON válido."""
    resultado = cargar_pedido("dummy.json")
    
    assert resultado["estado"] == "ok"
    mock_archivo.assert_called_once_with(Path("dummy.json"), "r", encoding="utf-8")