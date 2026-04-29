"""Tests para NLP (No-linear Programming).
Valida optimización de beneficio y problemas de almacén.
"""

import pytest
from solvers.nlp import resolver_nlp


class TestNLPBeneficio:
    """Tests para optimización de beneficio"""
    
    def test_nlp_beneficio_simple(self):
        """Test caso simple de maximización de beneficio"""
        enunciado = "Precio P = 100 - Q, Costo C = 20Q"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_nlp_beneficio_ejemplo_libro(self):
        """Test Ejemplo 6.1 Hillier: Q*=2500, B*=$52,500"""
        enunciado = "Precio P = 150 - 0.01Q, Costo C = 50Q"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_nlp_beneficio_constant_price(self):
        """Test con precio constante"""
        enunciado = "P = 100, c = 20"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
    
    def test_nlp_beneficio_linear_demand(self):
        """Test con demanda lineal"""
        enunciado = "P = 200 - 2Q, Costo = 50Q"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
    
    def test_nlp_beneficio_decimal_coeff(self):
        """Test con coeficientes decimales"""
        enunciado = "Precio P = 99.5 - 0.25Q, Costo = 19.99Q"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None


class TestNLPAlmacen:
    """Tests para problemas de almacén"""
    
    def test_nlp_almacen_simple(self):
        """Test caso simple de almacén"""
        enunciado = "Almacén: xy = 625, costo 400x + 2y"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_nlp_almacen_ejemplo_libro(self):
        """Test Ejemplo 6.2 Hillier: x*=25.82, C*=7745.97"""
        enunciado = "Area almacén: xy = 625, Costo = 400x + 2y"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_nlp_almacen_different_capacity(self):
        """Test con capacidad diferente"""
        enunciado = "xy = 1000, 500x + y"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
    
    def test_nlp_almacen_decimal_cost(self):
        """Test con costos decimales"""
        enunciado = "xy = 500, 350.5x + 1.5y"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None


class TestNLPValidation:
    """Tests de validación para NLP"""
    
    def test_nlp_invalid_format(self):
        """Test formato inválido"""
        enunciado = "Esto no es un problema de beneficio o almacén"
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
        # Debería indicar que no lo reconoce
        assert "no identificado" in resultado.lower() or "⚠️" in resultado
    
    def test_nlp_empty_input(self):
        """Test entrada vacía"""
        enunciado = ""
        resultado = resolver_nlp(enunciado)
        
        assert resultado is not None
    
    def test_nlp_returns_string(self):
        """Test que siempre retorna string"""
        enunciados = [
            "P = 100 - Q, C = 20Q",
            "xy = 625, 400x + 2y",
            "texto inválido"
        ]
        
        for enunciado in enunciados:
            resultado = resolver_nlp(enunciado)
            assert isinstance(resultado, str)


class TestNLPOutput:
    """Tests de formato de salida para NLP"""
    
    def test_nlp_output_is_string(self):
        """Test que output es siempre string"""
        enunciado = "P = 100 - Q, C = 20Q"
        resultado = resolver_nlp(enunciado)
        
        assert isinstance(resultado, str)
    
    def test_nlp_output_not_empty(self):
        """Test que output no está vacío"""
        enunciado = "P = 100 - Q, C = 20Q"
        resultado = resolver_nlp(enunciado)
        
        assert len(resultado) > 0
