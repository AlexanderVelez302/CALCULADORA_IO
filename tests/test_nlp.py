"""Tests para NLP (programación no lineal)."""

from solvers.nlp import resolver_nlp


class TestNLP:
	def test_nlp_beneficio_valido(self):
		texto = "Precio P = 100 - 0.5Q. Costo total C = 20Q + 100. Maximizar beneficio"
		resultado = resolver_nlp(texto)

		assert isinstance(resultado, str)
		assert "beneficio" in resultado.lower() or "optimiz" in resultado.lower()

	def test_nlp_almacen_valido(self):
		texto = "Un almacén rectangular debe tener 1000 m^2. Costo frontal 100/m y otras 50/m"
		resultado = resolver_nlp(texto)

		assert isinstance(resultado, str)
		assert "almac" in resultado.lower() or "costo" in resultado.lower()

	def test_nlp_formato_no_reconocido(self):
		texto = "Este texto no describe un problema NLP"
		resultado = resolver_nlp(texto)

		assert isinstance(resultado, str)
		assert "no identificado" in resultado.lower() or "⚠️" in resultado
