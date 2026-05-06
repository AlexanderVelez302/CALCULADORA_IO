# Calculadora de Investigación Operativa

## Descripción General

**Calculadora IO** es una aplicación completa para resolver problemas clásicos de Investigación Operativa utilizando heurísticas y algoritmos especializados, con soporte para explicaciones basadas en IA y acceso a recursos del libro *Introduction to Operations Research* de Hillier.

### Características Principales

- ✅ **8+ Tipos de Problemas Soportados**
  - PERT/CPM (ruta crítica)
  - Flujo Máximo (Ford-Fulkerson/Edmonds-Karp)
  - Transporte & Transbordo (greedy + Dijkstra)
  - EOQ (cantidad económica de pedido)
  - Colas M/M/1 (teoría de colas)
  - Programación Lineal (N variables, mixta)
  - Problemas no-lineales (beneficio, almacén)
  - Problemas de Asignación (opcional)

- 🎯 **Detección Automática** de tipo de problema (heurísticas + Groq LLM)
- 🧠 **Explicaciones con IA** (Groq) para problemas complejos
- 📚 **Integración Hillier** - Acceso a contexto del libro de texto
- 🌐 **Interfaz Web** moderna (Flask + Bootstrap + localStorage)
- 📊 **Exportación** a PDF, TXT, JSON
- ✏️ **Historial local** (persistencia con localStorage)
- ⚡ **Validación en tiempo real** con indicador de carga
- 🔁 **Compatibilidad de formatos** en varios solvers y tests alineados con el parser real

### Estado de validación

- ✅ Suite de pruebas actual: **102 tests passing**
- ✅ Compatibilidad añadida para integraciones antiguas del router
- ✅ Solvers y web validados con entradas reales de uso

---

## Inicio Rápido

### 1. Instalación

```bash
# Clonar o descargar el proyecto
cd CALCULADORA_IO

# Crear entorno virtual
python -m venv venv

# Activar venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configurar Variables de Entorno

Crear archivo `.env` en raíz del proyecto:

```env
GROQ_API_KEY=tu_clave_groq_aqui
```

(Obtener clave en [Groq Console](https://console.groq.com))

### 3. Ejecutar

**Interfaz Web:**
```bash
python web.py
# Acceder a http://localhost:5000
```

**Línea de Comandos:**
```bash
python main.py
# Ingresar problemas al prompt
```

---

## Estructura del Proyecto

```
CALCULADORA_IO/
├── COMPARATIVA_APP_VS_RAG.md  # Diferencias App determinista vs Notebook RAG
├── main.py                    # Entrada console
├── web.py                     # Servidor Flask
├── requirements.txt           # Dependencias
├── .env                       # Variables de entorno (crear)
│
├── core/                      # Núcleo lógico
│   ├── detector_ia.py        # Detector de tipo de problema
│   ├── router.py             # Enrutamiento a solvers
│   ├── parser_lp.py          # Parser para LP
│   ├── pert_parser.py        # Parser para PERT
│   └── detector.py           # Detectores heurísticos
│
├── solvers/                   # Solvers especializados
│   ├── pert.py               # PERT/CPM
│   ├── flujo.py              # Flujo máximo
│   ├── transporte_simple.py  # Transporte & Transbordo
│   ├── eoq.py                # EOQ
│   ├── colas.py              # Colas M/M/1
│   ├── lp.py                 # Programación lineal (PuLP)
│   ├── nlp.py                # Problemas no-lineales
│   └── asignacion.py         # Problemas de asignación
│
├── ai/                        # Integración IA
│   ├── groq.py               # Cliente Groq
│   └── embeddings.py         # Recuperación Hillier
│
├── templates/                 # Templates Jinja2
│   └── index.html            # Página principal
│
├── static/                    # Recursos estáticos
│   └── styles/
│       └── main.css          # Estilos CSS
│
├── tests/                     # Suite de tests
│   ├── conftest.py           # Fixtures pytest
│   ├── test_pert.py
│   ├── test_flujo.py
│   ├── test_transporte.py
│   ├── test_eoq.py
│   ├── test_colas.py
│   ├── test_nlp.py
│   ├── test_web.py
│   └── test_integration.py
│
├── data/                      # Datos (PDFs, bases de datos)
├── config/                    # Configuración
│   └── settings.py
└── utils/                     # Utilidades
    └── parser.py
```

---

## Tipos de Problemas Soportados

### 1. PERT (Program Evaluation and Review Technique)

Calcula rutas críticas, tiempos más tempranos (ES/EF) y más tardíos (LS/LF).

**Formato:**
```
A(duración) B(duración) ..., A→B→C, ...
```

**Formato narrativo (también soportado):**
```
Actividad A (4d). Actividad B (3d) depende de A. Actividad C (2d) depende de A. Actividad D (5d) depende de B y C.
```

**Ejemplo:**
```
A(3) B(4) C(5) D(4) E(2), A→B→D→E, A→C, C→E
```

### 2. Flujo Máximo

Encuentra el flujo máximo desde fuente a destino en una red.

**Formato:**
```
Nodo 1: 2(capacidad) 3(capacidad), ...
```

**Ejemplo:**
```
Nodo 1: 2(10) 3(10)
Nodo 2: 3(2) 4(4)
Nodo 3: 4(9)
```

### 3. Problema de Transporte

Asigna oferta a demanda minimizando costo.

**Formato:**
```
Oferta: A(cantidad) B(cantidad), Demanda: X(cantidad) Y(cantidad), A-X: costo, ...
```

**Ejemplo:**
```
Oferta: A(50) B(40) C(60)
Demanda: X(35) Y(50) Z(65)
A-X: 2, A-Y: 3, A-Z: 1
B-X: 5, B-Y: 2, B-Z: 3
C-X: 1, C-Y: 4, C-Z: 2
```

**Formato narrativo (también soportado):**
```
Planta 1 ofrece 20, Planta 2 ofrece 30. Cliente 1 demanda 25, Cliente 2 demanda 25. Costos: P1-C1=2, P1-C2=4, P2-C1=3, P2-C2=1.
```

### 4. EOQ (Economic Order Quantity)

Calcula cantidad óptima de pedido.

**Formato:**
```
Demanda = D, Costo de pedido = S, Costo mantenimiento = H
```

**Ejemplo:**
```
Demanda anual = 1000, Costo de pedido = 50, Costo de mantenimiento = 0.2
```

### 5. Colas M/M/1

Analiza sistemas de colas de un servidor.

**Formato:**
```
Tasa de llegada λ = valor, Tasa de servicio μ = valor
```

**Ejemplo:**
```
λ = 10 clientes/hora, μ = 12 clientes/hora
```

### 6. Programación Lineal (LP)

Resuelve problemas de optimización lineal con N variables.

**Formato:**
```
Maximizar/Minimizar: expresión
s.a.
restricción1
restricción2
...
```

**Ejemplo:**
```
Maximizar: 3x + 2y
s.a.
x + y <= 4
x <= 2
x >= 0, y >= 0
```

### 7. Problemas No-Lineales

**a) Beneficio:**
```
Precio P = a - bQ, Costo C = cQ + d
```

**b) Almacén:**
```
xy = K, Costo = ax + by
```

---

## Uso de la Interfaz Web

### Formulario Principal

1. **Ingresar problema** en el área de texto
2. **Hacer clic en "Resolver"**
3. **Ver resultado** con tabla de datos
4. **Exportar** como PDF, TXT o guardar en historial

### Tarjetas de Acceso Rápido

Botones para acceder rápidamente a ejemplos de cada tipo de problema.

### Historial

- **Ver historial** de problemas resueltos
- **Limpiar historial** (también limpia localStorage)
- **Exportar historial** como JSON

### Exportación

- **PDF** - Descarga PDF con resultado formateado
- **TXT** - Copia texto al portapapeles
- **JSON** - Exporta todo el historial

---

## Arquitectura y Flujo

```
┌─────────────────────────────────────────────────────────────┐
│                    ENTRADA DE USUARIO                       │
│            (Console o Web - Interfaz HTML+JS)               │
└────────────────────────┬────────────────────────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │  DETECTOR_IA         │
              │ ┌────────────────┐   │
              │ │ Heurísticas    │   │ ◄── Primero intenta patrones
              │ ├────────────────┤   │     regex rápidos
              │ │ Fallback Groq  │   │ ◄── Si falla, usa LLM
              │ └────────────────┘   │
              └──────────┬───────────┘
                         │
         ┌───────────────┼───────────────┐
         │  PROBLEMA CLASIFICADO         │
         │ (pert, flujo, transporte,...) │
         └───────────────┬───────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │      ROUTER          │
              │                      │
              │  if tipo == 'pert':  │
              │    → resolver_pert() │
              │  elif tipo == 'lp':  │
              │    → resolver_lp()   │
              │  ...                 │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │    SOLVER            │
              │                      │
              │ Algoritmo específico │
              │ para el problema     │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │ EXPLICACIÓN (IA)     │
              │                      │
              │ Groq con contexto    │
              │ Hillier (opcional)   │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   FORMATO OUTPUT     │
              │                      │
              │ Tabla + Explicación  │
              │ + Recomendaciones    │
              └──────────┬───────────┘
                         │
                         ▼
        ┌────────────────┴────────────────┐
        │                                 │
        ▼                                 ▼
   Retorna a Usuario              Historial localStorage
```

---

## Funciones Principales

### Router Principal
```python
from core.router import resolver

resultado = resolver("A(3) B(4) C(5), A→B→C")
print(resultado)
```

### Solvers Directos
```python
from solvers.pert import resolver_pert
from solvers.lp import resolver_lp

pert_resultado = resolver_pert("A(3) B(4), A→B")
lp_resultado = resolver_lp("max 3x + 2y, x + y <= 4")
```

### Detector
```python
from core.detector_ia import detectar_tipo_con_ia

tipo = detectar_tipo_con_ia("A(3) B(4), A→B")
# Retorna: "pert"
```

---

## Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|-----------|-----------|---------|
| **Runtime** | Python | 3.13.2 |
| **Web** | Flask | 2.3.3 |
| **Optimización** | PuLP | 3.3.0 |
| **Análisis** | scipy, numpy, pandas | Latest |
| **IA** | Groq API | 0.37.1 |
| **Templating** | Jinja2 | - |
| **Frontend** | Bootstrap | 5.3.2 |
| **PDFs** | reportlab, pypdf | 4.4.1, 6.10.2 |

---

## Testing

```bash
# Ejecutar todos los tests
pytest tests/

# Tests específicos
pytest tests/test_pert.py -v
pytest tests/test_lp.py -v
pytest tests/test_web.py -v

# Con cobertura
pytest tests/ --cov=solvers --cov=core
```

**Cobertura:**
- ✅ Tests unitarios por solver
- ✅ Tests de integración (detector → router → solver)
- ✅ Tests de API web
- ✅ Edge cases y error handling

---

## Troubleshooting

### Error: `ImportError: No module named 'groq'`
```bash
pip install groq
```

### Error: `GROQ_API_KEY not found`
```bash
# Crear archivo .env en raíz
echo "GROQ_API_KEY=tu_clave" > .env
```

### Puerto 5000 en uso
```bash
python web.py --port=5001
```

### Tests fallan por imports
```bash
# Asegurarse de estar en venv activado
pytest tests/
```

---

## Desarrollo Futuro

- [ ] Soporte para más tipos de problemas (programación dinámica)
- [ ] Cache de resultados
- [ ] API REST dedicada
- [ ] Visualización de redes (grafos)
- [ ] Validación de modelos matemáticos
- [ ] Multi-idioma (EN, ES, PT)
- [ ] Móvil (React Native)

---

## Licencia y Atribuciones

- **Base teórica**: *Introduction to Operations Research* - Hillier & Lieberman
- **Algoritmos**: Implementación original basada en clásicos de IO
- **IA**: Groq LLM para explicaciones y clasificación

---

## Contacto y Soporte

Para reportar bugs o sugerir features:

```bash
# Crear issue con detalles:
- Tipo de problema
- Input exacto
- Error o resultado inesperado
- Python version: python --version
```

---

## Notas Importantes

1. **Precisión Numérica**: Se utiliza aritmética flotante estándar (Python float). Para precisión crítica, considerar Decimal.
2. **Límites de Escalabilidad**: LP soporta 100+ variables; para redes muy grandes usar solver especializado.
3. **Costo API**: El detector Groq consume tokens. Considerar cache local para problemas frecuentes.

---

**Última actualización**: 2026-04-28  
**Versión**: 1.0.0 - Final Release
