"""
Configuración común para todos los tests.
Fixtures reutilizables y setup/teardown global.
"""

import pytest
import sys
from pathlib import Path

# Añadir el directorio raíz al path para importar módulos
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from solvers.pert import resolver_pert
from solvers.flujo import resolver_flujo
from solvers.transporte_simple import resolver_transporte
from solvers.eoq import resolver_eoq
from solvers.colas import resolver_colas
from solvers.lp import resolver_lp
from solvers.nlp import resolver_nlp


@pytest.fixture
def sample_pert_problem():
    """Problema PERT simple: A->B->D->E, 15 días"""
    return "A(3) B(4) C(5) D(4) E(2), A→B→D→E"


@pytest.fixture
def sample_flujo_problem():
    """Problema de flujo máximo simple"""
    return "Flujo máximo: Nodo 1: A(4) B(3), A: 2(5) 3(2), B: 2(2) 4(4), 2: 4(5), 3: 4(3)"


@pytest.fixture
def sample_transporte_problem():
    """Problema de transporte clásico"""
    return "Oferta: A(50) B(40) C(60), Demanda: X(35) Y(50) Z(65), A-X: 2, A-Y: 3, A-Z: 1, B-X: 5, B-Y: 2, B-Z: 3, C-X: 1, C-Y: 4, C-Z: 2"


@pytest.fixture
def sample_eoq_problem():
    """Problema EOQ simple"""
    return "Demanda anual = 1000, Costo de pedido = 50, Costo de mantenimiento = 0.2 por unidad"


@pytest.fixture
def sample_colas_problem():
    """Problema de colas M/M/1"""
    return "Tasa de llegada λ = 10 clientes/hora, Tasa de servicio μ = 12 clientes/hora"


@pytest.fixture
def sample_lp_problem():
    """Problema LP simple: maximizar 3x + 2y s.a. x + y <= 4, x <= 2"""
    return "Maximizar: 3x + 2y\ns.a.\nx + y <= 4\nx <= 2\nx >= 0, y >= 0"


@pytest.fixture
def sample_nlp_beneficio_problem():
    """Problema NLP beneficio: P = a - bQ, D = a - P"""
    return "Función de demanda: P = 100 - 0.5Q, Costo unitario c = 20"


@pytest.fixture
def sample_nlp_almacen_problem():
    """Problema NLP almacén: xy = K, minimizar costo"""
    return "Capacidad constante xy = 625, Costo de construcción = 400x, Costo de almacenamiento = 2y"


class MockResponse:
    """Mock para respuestas Groq/IA"""
    def __init__(self, content="Test response"):
        self.content = content


@pytest.fixture
def mock_groq(monkeypatch):
    """Mock para cliente Groq"""
    def mock_chat_completion(*args, **kwargs):
        return MockResponse("Test classification result")
    
    # Podría monkearpatchear aquí si es necesario
    return mock_chat_completion
