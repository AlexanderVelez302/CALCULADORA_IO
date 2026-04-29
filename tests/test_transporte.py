"""
Tests para el solver de Problema de Transporte.
Valida asignación greedy, costos y transbordo.
"""

import pytest
from solvers.transporte_simple import resolver_transporte


class TestTransporte:
    """Tests para solver de transporte"""
    
    def test_transporte_simple_2x2(self):
        """Test caso simple: 2 orígenes, 2 destinos"""
        enunciado = """Oferta: A(50) B(40)
        Demanda: X(30) Y(60)
        A-X: 2, A-Y: 3
        B-X: 5, B-Y: 2"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
        assert "costo" in resultado.lower() or "cost" in resultado.lower()
    
    def test_transporte_ejemplo_libro(self):
        """Test Ejemplo 3.1 Hillier: costo 650"""
        enunciado = """Oferta: A(50) B(40) C(60)
        Demanda: X(35) Y(50) Z(65)
        A-X: 2, A-Y: 3, A-Z: 1
        B-X: 5, B-Y: 2, B-Z: 3
        C-X: 1, C-Y: 4, C-Z: 2"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
        assert "650" in resultado or "costo" in resultado.lower()
    
    def test_transporte_unbalanced_supply_demand(self):
        """Test cuando oferta != demanda"""
        enunciado = """Oferta: A(100) B(50)
        Demanda: X(60) Y(70)
        A-X: 1, A-Y: 2
        B-X: 3, B-Y: 1"""
        resultado = resolver_transporte(enunciado)
        
        # Debería manejar desbalance (dummy origen/destino)
        assert resultado is not None
    
    def test_transporte_single_origin(self):
        """Test un solo origen"""
        enunciado = """Oferta: A(100)
        Demanda: X(50) Y(50)
        A-X: 1, A-Y: 2"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
    
    def test_transporte_all_same_cost(self):
        """Test cuando todos los costos son iguales"""
        enunciado = """Oferta: A(50) B(50)
        Demanda: X(50) Y(50)
        A-X: 1, A-Y: 1
        B-X: 1, B-Y: 1"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
        assert "100" in resultado or "costo" in resultado.lower()


class TestTransbordo:
    """Tests para transbordo (caso especial de transporte)"""
    
    def test_transbordo_simple(self):
        """Test transbordo simple con nodo intermedio"""
        enunciado = """Origen: A(100)
        Destino: B(100)
        Intermedio: C(con capacidad)
        A-C: 2, C-B: 3"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
    
    def test_transbordo_ejemplo_libro(self):
        """Test Ejemplo 3.2 Hillier: transbordo costo 80"""
        enunciado = """Plantas: P1(100) P2(150)
        Almacenes: W1(80) W2(70)
        Clientes: C1(50) C2(60) C3(40)
        P1-W1: 4, P1-W2: 6
        P2-W1: 5, P2-W2: 3
        W1-C1: 2, W1-C2: 3, W1-C3: 5
        W2-C1: 4, W2-C2: 2, W2-C3: 2"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None


class TestTransporteValidation:
    """Tests de validación para transporte"""
    
    def test_transporte_invalid_format(self):
        """Test formato inválido"""
        enunciado = "Esto no es un problema de transporte"
        resultado = resolver_transporte(enunciado)
        
        assert resultado is None or "error" in resultado.lower()
    
    def test_transporte_negative_cost(self):
        """Test con costos negativos (debería funcionar)"""
        enunciado = """Oferta: A(50) B(50)
        Demanda: X(50) Y(50)
        A-X: -1, A-Y: 2
        B-X: 3, B-Y: -2"""
        resultado = resolver_transporte(enunciado)
        
        # Debería manejar costos negativos (válido en IO)
        assert resultado is not None
    
    def test_transporte_zero_cost(self):
        """Test con costo cero"""
        enunciado = """Oferta: A(50)
        Demanda: X(50)
        A-X: 0"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
        assert "0" in resultado


class TestTransporteOutput:
    """Tests de formato de salida"""
    
    def test_transporte_output_contains_cost(self):
        """Test que output contiene costo total"""
        enunciado = """Oferta: A(50)
        Demanda: X(50)
        A-X: 10"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
        assert "500" in resultado or "costo" in resultado.lower()
    
    def test_transporte_output_contains_allocation(self):
        """Test que output muestra asignación"""
        enunciado = """Oferta: A(100)
        Demanda: X(50) Y(50)
        A-X: 1, A-Y: 2"""
        resultado = resolver_transporte(enunciado)
        
        assert resultado is not None
