"""Tests para endpoints web Flask."""

import json

import pytest

import web


@pytest.fixture
def client(monkeypatch):
	monkeypatch.setattr(web, "resolver", lambda _pregunta: "Resultado de prueba")
	monkeypatch.setattr(web, "buscar_contexto_libro", lambda _pregunta: "Contexto de prueba")

	app = web.create_app()
	app.config["TESTING"] = True
	with app.test_client() as test_client:
		yield test_client


class TestWeb:
	def test_get_index(self, client):
		response = client.get("/")
		assert response.status_code == 200
		assert b"form" in response.data.lower()

	def test_post_index(self, client):
		response = client.post("/", data={"pregunta": "Pregunta de prueba"})
		assert response.status_code == 200
		assert b"resultado" in response.data.lower() or b"prueba" in response.data.lower()

	def test_exportar_pdf(self, client):
		payload = {
			"pregunta": "Pregunta",
			"resultado": "Resultado",
			"contexto_libro": "Contexto",
		}
		response = client.post("/exportar-pdf", data=json.dumps(payload), content_type="application/json")

		assert response.status_code == 200
		assert "application/pdf" in response.content_type.lower()
		assert len(response.data) > 0
