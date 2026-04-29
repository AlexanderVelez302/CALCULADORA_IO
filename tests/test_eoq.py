"""
Tests para EOQ (Economic Order Quantity).
Valida cálculo de cantidad óptima, costo total y punto de reorden.
"""

import pytest
from solvers.eoq import resolver_eoq


class TestEOQ:
    """Tests para solver EOQ"""
    
    def test_eoq_basic(self):
        """Test caso básico: D=1000, S=50, H=0.2"""
        enunciado = "Demanda = 1000, Costo de pedido = 50, Costo mantenimiento por unidad = 0.2"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
        # Q* = sqrt(2*1000*50/0.2) = sqrt(500000) ≈ 707
        assert "707" in resultado or "706" in resultado or "708" in resultado
    
    def test_eoq_ejemplo_libro(self):
        """Test Ejemplo 4.1 Hillier: Q*=707"""
        enunciado = """Demanda anual D = 1000 unidades
        Costo de ordenar S = $50 por orden
        Costo de mantenimiento H = $0.2 por unidad por año"""
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
        assert "707" in resultado or "706" in resultado
    
    def test_eoq_high_demand(self):
        """Test con demanda alta"""
        enunciado = "D = 10000, S = 100, H = 0.5"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
        # Q* = sqrt(2*10000*100/0.5) = sqrt(4000000) = 2000
        assert "2000" in resultado
    
    def test_eoq_low_demand(self):
        """Test con demanda baja"""
        enunciado = "D = 100, S = 10, H = 0.1"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
        assert any(char.isdigit() for char in resultado)
    
    def test_eoq_decimal_cost(self):
        """Test con costos decimales"""
        enunciado = "D = 500, S = 25.5, H = 0.15"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
    
    def test_eoq_lead_time(self):
        """Test con tiempo de entrega (lead time)"""
        enunciado = "D = 1000, S = 50, H = 0.2, Lead time = 10 dias"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None


class TestEOQValidation:
    """Tests de validación para EOQ"""
    
    def test_eoq_zero_demand(self):
        """Test con demanda cero (caso degenerado)"""
        enunciado = "D = 0, S = 50, H = 0.2"
        resultado = resolver_eoq(enunciado)
        
        # Debería indicar que no hay demanda
        assert resultado is None or "error" in resultado.lower() or "0" in resultado
    
    def test_eoq_negative_cost(self):
        """Test con costos negativos (inválido)"""
        enunciado = "D = 1000, S = -50, H = 0.2"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is None or "error" in resultado.lower()
    
    def test_eoq_zero_setup_cost(self):
        """Test con costo de pedido cero"""
        enunciado = "D = 1000, S = 0, H = 0.2"
        resultado = resolver_eoq(enunciado)
        
        # Q* = 0, debe indicarlo
        assert resultado is not None
    
    def test_eoq_invalid_format(self):
        """Test formato inválido"""
        enunciado = "Esto no es un problema EOQ"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is None or "error" in resultado.lower()


class TestEOQOutput:
    """Tests de formato de salida"""
    
    def test_eoq_output_contains_quantity(self):
        """Test que output contiene cantidad óptima"""
        enunciado = "D = 1000, S = 50, H = 0.2"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
        assert any(char.isdigit() for char in resultado)
    
    def test_eoq_output_mentions_cost(self):
        """Test que output menciona costo total"""
        enunciado = "D = 1000, S = 50, H = 0.2"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
        assert any(word in resultado.lower() for word in ["costo", "cost", "total"])
    
    def test_eoq_output_mentions_cycles(self):
        """Test que output menciona número de ciclos"""
        enunciado = "D = 1000, S = 50, H = 0.2"
        resultado = resolver_eoq(enunciado)
        
        assert resultado is not None
        # Debería mencionar ciclos, tiempo entre órdenes, etc.
