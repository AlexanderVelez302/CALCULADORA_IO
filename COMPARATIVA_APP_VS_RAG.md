# Comparativa: App Calculadora IO vs Notebook RAG

## Objetivo

Este documento resume la diferencia entre:

- La aplicacion principal de este repositorio (solvers deterministas + web Flask)
- El notebook de ChatBot con RAG (PDF + embeddings + LLM + cache)

---

## 1) Diferencia principal de enfoque

### App Calculadora IO (este proyecto)

- Detecta el tipo de problema con heuristicas.
- Enruta a un solver especializado por categoria (PERT, transporte, EOQ, colas, LP, NLP, etc.).
- Calcula con formulas/algoritmos definidos.
- Entrega resultados reproducibles para el mismo input.

En resumen: es un motor de resolucion matematica orientado a precision y consistencia.

### Notebook RAG

- Carga el libro en PDF y lo fragmenta en chunks.
- Crea embeddings y recupera contexto semantico.
- Usa un LLM para redactar la respuesta.
- Guarda respuestas en cache (Supabase) para reuso.

En resumen: es un asistente conversacional orientado a explicacion flexible y preguntas abiertas.

---

## 2) Que gana y que pierde cada enfoque

### App Calculadora IO

Ventajas:
- Mayor control del metodo de solucion.
- Resultados mas estables en problemas estructurados.
- Mejor trazabilidad para evaluacion academica.
- Suite de pruebas automatizadas para evitar regresiones.

Limitaciones:
- Requiere que el enunciado se pueda mapear a formatos soportados.
- Menos flexible para preguntas teoricas totalmente abiertas.

### Notebook RAG

Ventajas:
- Muy flexible para preguntas en lenguaje natural.
- Puede explicar conceptos y contexto teorico con estilo conversacional.
- Buena experiencia para exploracion y tutorias.

Limitaciones:
- Puede variar respuestas entre ejecuciones.
- No siempre garantiza exactitud numerica como un solver dedicado.
- Depende de calidad de contexto recuperado y del modelo LLM.

---

## 3) En que casos usar cada uno

Usar la App Calculadora IO cuando:
- Necesitas resolver ejercicios de IO con resultado numerico verificable.
- Necesitas consistencia para pruebas, demos o evaluacion.
- Quieres exportar y validar resultados de forma repetible.

Usar Notebook RAG cuando:
- Quieres explicaciones conceptuales o apoyo teorico.
- Quieres un chat flexible para discutir metodos.
- Quieres recuperar rapidamente informacion del libro.

---

## 4) Recomendacion practica (modelo hibrido)

La estrategia recomendada es combinar ambos:

- Paso 1: detectar tipo de problema y resolver con solver determinista.
- Paso 2: usar RAG/LLM para explicar el resultado, no para reemplazar el calculo.

Asi se obtiene:
- Precision en el resultado
- Flexibilidad en la explicacion

---

## 5) Nota de seguridad

Si se usan notebooks o demos con APIs externas:

- No guardar claves directamente en el codigo.
- Cargar claves desde variables de entorno.
- Rotar claves si fueron compartidas accidentalmente.

---

## Conclusion

No son enfoques excluyentes.

- La App es el nucleo de calculo confiable.
- El RAG agrega valor en explicacion y contexto.

Usados juntos, forman una solucion mas completa para Investigacion de Operaciones.
