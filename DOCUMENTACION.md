# Documentación del proyecto Calculadora IO

## 1. Resumen general

Este proyecto es una calculadora de Investigación de Operaciones que recibe enunciados en lenguaje natural, detecta el tipo de problema y los resuelve con un solver especializado.

La versión actual ya cubre problemas de:

- PERT / CPM
- Flujo máximo en redes
- Transporte y transbordo
- EOQ e inventarios
- Colas M/M/1
- Programación lineal
- Programación no lineal
- Asignación

Además, integra:

- un router central para decidir qué solver usar
- un detector con heurísticas y fallback con IA
- consulta de contexto del libro de Hillier
- una interfaz de consola
- una interfaz web local con Flask

## 2. Estado actual del sistema

### Lo que ya está funcionando

- Entrada por consola en `main.py`
- Interfaz web local en `web.py`
- Clasificación automática del tipo de problema en `core/detector_ia.py`
- Enrutamiento en `core/router.py`
- Explicaciones generadas con IA en `ai/groq.py`
- Contexto del libro en `ai/embeddings.py`
- Solvers especializados en `solvers/`
- Interfaz web con:
  - tarjetas de acceso rápido por tipo de problema
  - selector de ejemplos
  - panel de contexto del libro
  - historial local en `localStorage`
  - exportación e importación de historial
  - copiar resultado
  - exportar TXT
  - exportación real de PDF generada en servidor

### Lo que todavía está pendiente

- Menú TUI más avanzado en terminal
- GUI de escritorio con Tkinter
- Un paquete formal de tests para todos los módulos
- Posible refinamiento de algunas heurísticas de clasificación

## 3. Flujo de ejecución

El flujo general es este:

1. El usuario escribe un problema.
2. `core/detector_ia.py` detecta el tipo de problema.
3. `core/router.py` envía el texto al solver correcto.
4. El solver devuelve el resultado matemático.
5. `ai/groq.py` genera una explicación adicional.
6. La respuesta final se muestra en consola o en la interfaz web.

En la interfaz web, además:

- `ai/embeddings.py` busca fragmentos relevantes del libro de Hillier.
- El resultado y el contexto se muestran en paneles separados.

## 4. Estructura de carpetas

### `main.py`

Punto de entrada por consola. Pide el problema línea por línea hasta que el usuario escriba `FIN`.

### `web.py`

Arranca la aplicación Flask local. Recibe el problema por formulario y lo envía al router.

### `core/`

#### `core/detector_ia.py`

Clasifica el problema.

- Usa reglas rápidas para casos conocidos
- Usa IA como fallback
- Reconoce tipos como `lp`, `nlp`, `eoq`, `colas`, `pert`, `flujo`, `transporte` y `asignacion`

#### `core/router.py`

Coordina todo el sistema.

- llama al detector
- selecciona el solver
- controla errores
- agrega la explicación final

### `ai/`

#### `ai/embeddings.py`

Carga fragmentos del libro de Hillier y busca contexto relevante para el problema.

#### `ai/groq.py`

Genera explicaciones textuales de los resultados usando Groq, salvo en casos estructurados como PERT donde se usa una explicación determinista.

### `solvers/`

#### `solvers/pert.py`

Resuelve ruta crítica con cálculo de ES, EF, LS, LF y holguras.

#### `solvers/flujo.py`

Resuelve flujo máximo con Ford-Fulkerson / Edmonds-Karp.

#### `solvers/transporte_simple.py`

Resuelve transporte y transbordo.

#### `solvers/eoq.py`

Resuelve EOQ y cálculo de costos asociados.

#### `solvers/colas.py`

Resuelve colas M/M/1 y calcula métricas como ρ, L, Lq, W, Wq y P0.

#### `solvers/lp.py`

Resuelve programación lineal y lineal entera con PuLP/CBC.

- admite variables continuas, enteras y binarias
- detecta formulaciones mixtas
- soporta `<=`, `>=` y `=`
- maneja variables con nombres como `x_1`, `x_2`, etc.

#### `solvers/nlp.py`

Resuelve programación no lineal para dos casos principales:

- optimización de beneficio
- minimización de costo de almacén

#### `solvers/asignacion.py`

Resuelve problemas de asignación.

### `templates/`

#### `templates/index.html`

Plantilla HTML de la interfaz web local.

Incluye:

- formulario principal
- ejemplos rápidos por tipo de problema
- panel de contexto del libro
- historial local
- exportación/importación de historial
- acciones de copiar/exportar/imprimir

## 5. Cómo ejecutar

### Consola

```bash
python main.py
```

### Web local

```bash
python web.py
```

Luego abrir:

```text
http://127.0.0.1:5000
```

### Validación de LP

```bash
python test_lp.py
```

## 6. Dependencias principales

Las dependencias más importantes son:

- `Flask` para la interfaz web local
- `PuLP` para programación lineal entera y continua
- `SciPy` para cálculos numéricos y optimización en algunos solvers
- `NumPy` para operaciones numéricas
- `pypdf` para lectura del libro de Hillier
- `python-dotenv` para variables de entorno
- `groq` y `langchain-groq` para explicaciones y clasificación con IA

## 7. Decisiones de diseño

### Router central

Se eligió un router único para evitar que cada interfaz tenga lógica duplicada.

### Parsers flexibles

Los problemas de IO suelen escribirse con notación muy variable. Por eso los solvers usan expresiones regulares flexibles para aceptar diferentes formatos.

### Explicación separada del cálculo

Se separó el cálculo matemático de la explicación textual para que:

- el solver sea determinista
- la explicación pueda cambiar sin romper el cálculo
- PERT y otros casos estructurados no dependan de una redacción de IA

### Web local

La interfaz web se ejecuta localmente, sin exponer claves ni depender de un backend remoto para el uso normal.

## 8. Estado funcional resumido

### Ya resuelto

- lectura de enunciados de tipo IO
- detección automática de tipo de problema
- múltiples solvers especializados
- interfaz web local con contexto y resultados
- exportación e importación de historial
- soporte de LP más robusto y con variables mixtas

### Pendiente si quieres seguir creciendo el proyecto

- TUI con navegación por teclado
- GUI de escritorio con Tkinter
- empaquetado para distribución
- tests para todos los solvers
- mejora visual final de la web

## 9. Recomendación práctica

Si el proyecto se va a mostrar o entregar, la mejor base actual es:

1. usar la web local como interfaz principal
2. conservar `main.py` como modo rápido de consola
3. añadir TUI o GUI solo si realmente hace falta para la presentación o el uso final

## 10. Nota final

El proyecto ya no es una calculadora simple. En este momento funciona más como una plataforma local de resolución de problemas de Investigación de Operaciones, con detección automática, solvers especializados, explicación y una interfaz web lista para uso local.
