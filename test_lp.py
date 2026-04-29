"""
Test suite para el solver de Programación Lineal (LP).
Valida: parseo de variables, categorías (continuas/enteras/binarias), restricciones y resolución.
"""

from solvers.lp import resolver_lp


def test_lp_continuo_simple():
    """Test 1: LP continuo simple con 2 variables."""
    problema = """
    Max Z = 3x + 4y
    
    Restricciones:
    1. 2x + y <= 8
    2. x + 2y <= 7
    """
    resultado = resolver_lp(problema)
    assert "RESULTADO ÓPTIMO" in resultado
    assert "Z =" in resultado
    assert "Tipo de variables: continuous" in resultado
    print("✅ Test 1 (LP continuo simple): PASÓ")


def test_lp_entero():
    """Test 2: LP con variables enteras detectadas por contexto."""
    problema = """
    Maximizar Z = 50x_1 + 60x_2
    
    Restricciones:
    1. 2x_1 + x_2 <= 4 (Horas disponibles)
    2. x_1 + 2x_2 <= 3 (Máquinas disponibles)
    
    Variables: x_1, x_2 son unidades de producto.
    """
    resultado = resolver_lp(problema)
    assert "RESULTADO ÓPTIMO" in resultado
    assert "Tipo de variables: integer" in resultado
    print("✅ Test 2 (LP entero por contexto): PASÓ")


def test_lp_binario_explicito():
    """Test 3: LP con variables binarias explícitamente declaradas."""
    problema = """
    Max Z = 10x_1 + 15x_2 + 8x_3
    
    Variables: x_1 binaria, x_2 binaria, x_3 binaria
    
    Restricciones:
    1. 2x_1 + 3x_2 + x_3 <= 5
    2. x_1 + 2x_2 + 2x_3 <= 4
    """
    resultado = resolver_lp(problema)
    assert "RESULTADO ÓPTIMO" in resultado
    assert "Tipo de variables: binary" in resultado
    assert "x_1 =" in resultado
    assert "x_2 =" in resultado
    assert "x_3 =" in resultado
    print("✅ Test 3 (LP binario explícito): PASÓ")


def test_lp_mixto():
    """Test 4: LP con tipos mixtos (binaria, entera, continua)."""
    problema = """
    Max Z = 5x_1 + 3x_2 + 2x_3
    
    Variables: x_1 binaria, x_2 entera, x_3 continua.
    
    Restricciones:
    1. 2x_1 + x_2 + x_3 <= 5
    2. x_1 + 2x_2 + x_3 <= 6
    3. x_1 + x_2 + x_3 >= 2
    """
    resultado = resolver_lp(problema)
    assert "RESULTADO ÓPTIMO" in resultado
    assert "Tipo de variables: mixed" in resultado
    print("✅ Test 4 (LP mixto): PASÓ")


def test_lp_5variables():
    """Test 5: LP de 5 variables con restricciones >= y limitaciones."""
    problema = """
    Max Z = 12x_1 + 25x_2 + 55x_3 + 150x_4 + 20x_5
    
    Restricciones:
    1. 2x_1 + 5x_2 + 10x_3 + 28x_4 + 12x_5 <= 1000
    2. 1x_1 + 1x_2 + 2x_3 + 4x_4 + 2x_5 <= 120
    3. 300x_1 + 500x_2 + 1000x_3 + 2500x_4 + 600x_5 <= 60000
    4. x_1 + x_2 + x_3 + x_4 + x_5 >= 40
    
    Variables: equipos a comprar (unidades)
    """
    resultado = resolver_lp(problema)
    assert "RESULTADO ÓPTIMO" in resultado
    assert "Tipo de variables: integer" in resultado
    assert "Z =" in resultado
    print("✅ Test 5 (LP 5 variables): PASÓ")


def test_lp_minimizacion():
    """Test 6: LP de minimización."""
    problema = """
    Minimizar C = 2x + 3y
    
    Restricciones:
    1. x + y >= 4
    2. 2x + y >= 5
    """
    resultado = resolver_lp(problema)
    assert "RESULTADO ÓPTIMO" in resultado
    assert "Z =" in resultado
    print("✅ Test 6 (LP minimización): PASÓ")


def test_lp_restriccion_igualdad():
    """Test 7: LP con restricción de igualdad."""
    problema = """
    Max Z = 4x + 3y
    
    Restricciones:
    1. x + y = 5
    2. 2x + y <= 8
    """
    resultado = resolver_lp(problema)
    assert "RESULTADO ÓPTIMO" in resultado
    assert "Z =" in resultado
    print("✅ Test 7 (LP con igualdad): PASÓ")


if __name__ == "__main__":
    tests = [
        test_lp_continuo_simple,
        test_lp_entero,
        test_lp_binario_explicito,
        test_lp_mixto,
        test_lp_5variables,
        test_lp_minimizacion,
        test_lp_restriccion_igualdad,
    ]

    print("\n" + "=" * 60)
    print("EJECUTANDO TEST SUITE DE PROGRAMACIÓN LINEAL")
    print("=" * 60 + "\n")

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"❌ {test.__name__}: FALLÓ")
            print(f"   Error: {e}\n")
            failed += 1
        except Exception as e:
            print(f"❌ {test.__name__}: ERROR")
            print(f"   Excepción: {e}\n")
            failed += 1

    print("=" * 60)
    print(f"RESUMEN: {passed} pasados, {failed} fallidos")
    print("=" * 60 + "\n")

    if failed == 0:
        print("✅ Todos los tests pasaron!")
    else:
        print(f"❌ {failed} test(s) fallaron.")
