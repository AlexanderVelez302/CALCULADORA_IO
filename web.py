import html
from io import BytesIO

from flask import Flask, Response, jsonify, render_template, request
from ai.embeddings import buscar_contexto_libro
from core.router import resolver

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Preformatted


def _generar_pdf_bytes(pregunta, resultado, contexto_libro):
    buffer = BytesIO()
    documento = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        rightMargin=2 * cm,
        leftMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
    )

    estilos = getSampleStyleSheet()
    titulo = estilos["Title"]
    subtitulo = estilos["Heading2"]
    normal = estilos["BodyText"]
    bloque = ParagraphStyle(
        "Bloque",
        parent=normal,
        fontName="Courier",
        fontSize=9.5,
        leading=12,
        spaceBefore=6,
        spaceAfter=10,
    )

    historia = []
    historia.append(Paragraph("Calculadora IO", titulo))
    historia.append(Spacer(1, 0.4 * cm))
    historia.append(Paragraph("Exportación de resultado", subtitulo))
    historia.append(Spacer(1, 0.2 * cm))

    if pregunta:
        historia.append(Paragraph("Enunciado", subtitulo))
        historia.append(Preformatted(html.escape(pregunta), bloque))

    if resultado:
        historia.append(Paragraph("Resultado", subtitulo))
        historia.append(Preformatted(html.escape(resultado), bloque))

    if contexto_libro:
        historia.append(Paragraph("Contexto del libro", subtitulo))
        historia.append(Preformatted(html.escape(contexto_libro), bloque))

    documento.build(historia)
    pdf = buffer.getvalue()
    buffer.close()
    return pdf


def create_app():
    app = Flask(__name__)

    @app.route('/', methods=['GET', 'POST'])
    def index():
        resultado = None
        contexto_libro = None
        pregunta = ''
        if request.method == 'POST':
            pregunta = request.form.get('pregunta', '')
            resultado = resolver(pregunta)
            contexto_libro = buscar_contexto_libro(pregunta)
        return render_template('index.html', resultado=resultado, contexto_libro=contexto_libro, pregunta=pregunta)

    @app.route('/exportar-pdf', methods=['POST'])
    def exportar_pdf():
        data = request.get_json(silent=True) or {}
        pregunta = data.get('pregunta', '')
        resultado = data.get('resultado', '')
        contexto_libro = data.get('contexto_libro', '')

        pdf_bytes = _generar_pdf_bytes(pregunta, resultado, contexto_libro)
        return Response(
            pdf_bytes,
            mimetype='application/pdf',
            headers={'Content-Disposition': 'attachment; filename=resultado_calculadora_io.pdf'},
        )

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='127.0.0.1', port=5000, debug=True)
