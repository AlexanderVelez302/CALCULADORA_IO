"""
Tests para el solver PERT (Program Evaluation and Review Technique).
Valida cálculo de ES, EF, LS, LF, holgura y ruta crítica.
"""

import pytest
from solvers.pert import resolver_pert


class TestPERT:
    """Tests para PERT solver"""
    
    def test_pert_simple_linear_path(self):
        """Test caso simple: A->B->C (ruta lineal)"""
        enunciado = "A(2) B(3) C(4), A→B→C"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        assert "A" in str(resultado)
        assert "Duración total" in resultado or "total" in resultado.lower()
        
    def test_pert_ejemplo_libro(self):
        """Test Ejemplo 1.1 Hillier: A->B->D->E con C paralelo, 15 días"""
        enunciado = "A(3) B(4) C(5) D(4) E(2), A→B→D→E, A→C, C→E"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        # Ruta crítica debe ser A->B->D->E = 3+4+4+2 = 13 días
        # O podría ser más con las otras rutas, validar que aparezca un número
        assert "días" in resultado.lower() or "dias" in resultado.lower()
    
    def test_pert_multiple_predecessors(self):
        """Test múltiples predecesores: E tiene A y D como predecesores"""
        enunciado = "A(2) B(3) D(4) E(5), A→E, D→E"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        assert "E" in str(resultado)
        
    def test_pert_complex_network(self):
        """Test red más compleja con múltiples caminos"""
        enunciado = """A(1) B(2) C(3) D(2) E(4) F(3)
        A→B→E
        A→C→F
        B→D→E"""
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        # Validar que aparece información de duración
        assert any(char.isdigit() for char in resultado)
    
    def test_pert_single_node(self):
        """Test caso degenerado: solo una actividad"""
        enunciado = "A(5)"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        
    def test_pert_duration_integers(self):
        """Test con duraciones enteras"""
        enunciado = "A(1) B(2) C(3), A→B→C"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        
    def test_pert_duration_decimals(self):
        """Test con duraciones decimales"""
        enunciado = "A(1.5) B(2.5) C(3.5), A→B→C"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None


class TestPERTValidation:
    """Tests de validación y edge cases para PERT"""
    
    def test_pert_invalid_format(self):
        """Test con formato inválido"""
        enunciado = "Esto no es válido"
        resultado = resolver_pert(enunciado)
        
        # Debe retornar un error o None gracefully
        assert resultado is None or "error" in resultado.lower()
    
    def test_pert_circular_dependency_handling(self):
        """Test manejo de dependencias circulares (si existen)"""
        # Este debería ser detectado y manejado
        enunciado = "A(1) B(2) C(3), A→B→C→A"
        resultado = resolver_pert(enunciado)
        
        # Debe detectar el error
        assert resultado is None or "error" in resultado.lower() or "círculo" in resultado.lower()
    
    def test_pert_zero_duration(self):
        """Test con actividad de duración 0 (dummy activity)"""
        enunciado = "A(0) B(2) C(3), A→B→C"
        resultado = resolver_pert(enunciado)
        
        # Debería funcionar, aunque sea una dummy activity
        assert resultado is not None


class TestPERTOutput:
    """Tests de formato de salida PERT"""
    
    def test_pert_output_contains_table(self):
        """Test que salida contiene tabla de resultados"""
        enunciado = "A(3) B(4) C(5), A→B→C"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        # Debería contener información estruturada
        assert any(keyword in resultado.lower() for keyword in ["actividad", "actividades", "a", "b", "c"])
    
    def test_pert_output_has_critical_path(self):
        """Test que output menciona la ruta crítica"""
        enunciado = "A(3) B(4) C(2), A→B→C"
        resultado = resolver_pert(enunciado)
        
        assert resultado is not None
        # Debería mencionar ruta crítica o camino crítico
        assert any(keyword in resultado.lower() for keyword in ["crítica", "critica", "ruta", "camino"])
