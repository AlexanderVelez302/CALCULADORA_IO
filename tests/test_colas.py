"""Tests para solver de Colas (M/M/1)."""

from solvers.colas import resolver_colas


class TestColas:
	def test_colas_basic(self):
		enunciado = "Tasa de llegada λ = 10, Tasa de servicio μ = 12"
		resultado = resolver_colas(enunciado)

		assert isinstance(resultado, str)
		assert "M/M/1" in resultado
		assert "83" in resultado or "0.83" in resultado

	def test_colas_decimal_rates(self):
		enunciado = "lambda = 3.5, mu = 4.2"
		resultado = resolver_colas(enunciado)

		assert isinstance(resultado, str)
		assert "clientes" in resultado.lower()

	def test_colas_unstable_system(self):
		enunciado = "λ = 12, μ = 10"
		resultado = resolver_colas(enunciado)

		assert isinstance(resultado, str)
		assert "inestable" in resultado.lower()

	def test_colas_invalid_format(self):
		enunciado = "Texto sin tasas"
		resultado = resolver_colas(enunciado)

		assert isinstance(resultado, str)
		assert "no se encontraron" in resultado.lower()
