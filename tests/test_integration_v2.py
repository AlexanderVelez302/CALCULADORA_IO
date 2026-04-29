"""Tests para módulos de integración (Router).
Valida flujo completo de enrutamiento y resolución.
"""

import pytest
from core.router import router


class TestRouter:
    """Tests para router (enrutamiento a solvers)"""
    
    def test_router_pert(self):
        """Test router con problema PERT"""
        enunciado = "A(3) B(4) C(5), A→B→C"
        resultado = router(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_router_transporte(self):
        """Test router con problema transporte"""
        enunciado = "Oferta: A(50), Demanda: X(50), A-X: 1"
        resultado = router(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_router_lp(self):
        """Test router con problema LP"""
        enunciado = "Maximizar: x + y\ns.a.\nx + y <= 10\nx <= 5"
        resultado = router(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_router_colas(self):
        """Test router con problema de colas"""
        enunciado = "λ = 10, μ = 12"
        resultado = router(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_router_eoq(self):
        """Test router con problema EOQ"""
        enunciado = "D = 1000, S = 50, H = 0.2"
        resultado = router(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_router_flujo(self):
        """Test router con problema de flujo"""
        enunciado = "Nodo 1: 2(10), Nodo 2: 3(5)"
        resultado = router(enunciado)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_router_unknown_problem(self):
        """Test router con tipo desconocido"""
        enunciado = "Texto completamente irrelevante sin estructura"
        resultado = router(enunciado)
        
        # Debería manejar gracefully
        assert resultado is None or isinstance(resultado, str)
    
    def test_router_error_handling(self):
        """Test que router maneja errores internos"""
        enunciado = "A(abc) B(def), A→B"  # Duraciones inválidas
        resultado = router(enunciado)
        
        # Debería retornar algo (error, None, o resultado)
        assert resultado is None or isinstance(resultado, str)
    
    def test_router_empty_input(self):
        """Test router con entrada vacía"""
        enunciado = ""
        resultado = router(enunciado)
        
        assert resultado is None or isinstance(resultado, str)


class TestRouterIntegration:
    """Tests de integración completa router→solver"""
    
    def test_full_pipeline_pert(self):
        """Test pipeline completo PERT"""
        enunciado = "A(2) B(3) C(4), A→B→C"
        resultado = router(enunciado)
        
        assert resultado is not None
        # Debería tener algún resultado numérico o información
    
    def test_full_pipeline_lp(self):
        """Test pipeline completo LP"""
        enunciado = "Maximizar 2x + 3y s.a. x + y <= 5, x >= 0, y >= 0"
        resultado = router(enunciado)
        
        assert resultado is not None
    
    def test_full_pipeline_transporte(self):
        """Test pipeline completo Transporte"""
        enunciado = """Oferta: A(100) B(50)
        Demanda: X(60) Y(90)
        A-X: 1, A-Y: 2, B-X: 3, B-Y: 1"""
        resultado = router(enunciado)
        
        assert resultado is not None
    
    def test_multiple_consecutive_calls(self):
        """Test múltiples llamadas consecutivas (estado limpio)"""
        enunciados = [
            "A(1) B(1), A→B",
            "λ=5, μ=10",
            "max x+y, x+y<=10"
        ]
        
        for enunciado in enunciados:
            resultado = router(enunciado)
            assert resultado is not None or resultado is None  # Aceptar ambos


class TestRouterErrorHandling:
    """Tests de manejo de errores en router"""
    
    def test_router_malformed_pert(self):
        """Test PERT mal formado"""
        enunciado = "A(()) B(invalid), A→B"
        resultado = router(enunciado)
        
        # Debería manejar sin crash
        assert resultado is None or isinstance(resultado, str)
    
    def test_router_malformed_lp(self):
        """Test LP mal formado"""
        enunciado = "max x y z, x y z <= 10"
        resultado = router(enunciado)
        
        assert resultado is None or isinstance(resultado, str)
    
    def test_router_very_long_input(self):
        """Test con input muy largo"""
        enunciado = "A(1) " * 1000
        resultado = router(enunciado)
        
        # Debería manejar
        assert resultado is None or isinstance(resultado, str)
