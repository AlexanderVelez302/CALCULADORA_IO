Interfaz Web local para Calculadora IO

Documentación principal del proyecto:
- [DOCUMENTACION.md](DOCUMENTACION.md)

Requisitos:
- Python 3.11+ (venv configurado como en el proyecto)
- Dependencias en `requirements.txt` (ejecutar `pip install -r requirements.txt`)

Ejecutar localmente:

```bash
python web.py
```

Abrir en el navegador:

http://127.0.0.1:5000

Notas:
- La app envía el enunciado al router (`core.router.resolver`) y muestra el resultado.
- También muestra contexto recuperado del libro de Hillier en un panel separado.
- El historial de consultas se guarda en el navegador con `localStorage`.
- Incluye tarjetas de inicio por tipo de problema, selector de ejemplos, copia del resultado, exportación/importación de historial, exportación a TXT y exportación real de PDF desde el servidor.
- No expone claves ni servicios externos; todo corre localmente.
