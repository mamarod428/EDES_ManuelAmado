import pytest

# ==========================================
# LÓGICA DEL PROGRAMA (Funciones puras)
# ==========================================
def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    if b == 0:
        # Controlamos el error explícitamente, como recomiendan las buenas prácticas
        raise ValueError("No se puede dividir por cero")
    return a / b


# ==========================================
# PRUEBAS UNITARIAS (Formato pytest)
# ==========================================
def test_suma():
    assert suma(2, 3) == 5

def test_resta():
    assert resta(5, 2) == 3

def test_multiplicacion():
    assert multiplicacion(3, 4) == 12

def test_division():
    assert division(10, 2) == 5

def test_division_cero():
    # pytest.raises comprueba que efectivamente se lance la excepción correcta
    with pytest.raises(ValueError):
        division(10, 0)