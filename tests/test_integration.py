"""Tests de integración para detector y router."""

from core.detector_ia import detectar_tipo_con_ia
from core.router import resolver


class TestDetectorIntegracion:
	def test_detector_pert(self):
		tipo = detectar_tipo_con_ia("Actividades: A (3h), B (precede A, 2h)")
		assert tipo == "pert"

	def test_detector_colas(self):
		tipo = detectar_tipo_con_ia("Tasa de llegada lambda = 10 y tasa de servicio mu = 12")
		assert tipo == "colas"

	def test_detector_eoq(self):
		texto = "Demanda anual 1000, costo de pedido 50, costo de mantenimiento 2"
		tipo = detectar_tipo_con_ia(texto)
		assert tipo == "eoq"


class TestRouterIntegracion:
	def test_router_resuelve_pert(self):
		resultado = resolver("Actividades: A (Analisis, 3h), B (Informe, precede A, 2h)")
		assert isinstance(resultado, str)

	def test_router_resuelve_colas(self):
		resultado = resolver("Tasa de llegada lambda = 10, tasa de servicio mu = 12")
		assert isinstance(resultado, str)
		assert "colas" in resultado.lower() or "m/m/1" in resultado.lower()

	def test_router_resuelve_lp(self):
		texto = "Maximizar Z = 3x + 2y sujeto a x + y <= 4, x <= 2, x >= 0, y >= 0"
		resultado = resolver(texto)
		assert isinstance(resultado, str)
