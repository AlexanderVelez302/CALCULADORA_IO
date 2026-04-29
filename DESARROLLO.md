# Guía de Desarrollo - Calculadora IO

## Arquitectura General

```
Entrada → Detector → Router → Solver → Output
            ↓          ↓        ↓
         Heurística  Si/elif  Algoritmo
         + Groq      mapping   específico
```

---

## Módulos Principales

### 1. `core/detector_ia.py`

**Responsabilidad**: Detectar tipo de problema

**Función principal**:
```python
def detectar_tipo_con_ia(pregunta):
    """
    Detecta tipo de problema usando heurísticas + Groq fallback
    
    Returns:
        str: Tipo de problema ('pert', 'lp', 'flujo', etc.)
    """
```

**Heurísticas implementadas**:
- PERT: Busca patrones `A(num)` y flechas `→`
- LP: Busca `Maximizar/Minimizar`, `s.a.`, restricciones
- Transporte: Busca `Oferta`, `Demanda`, costos
- Flujo: Busca `Nodo`, capacidades entre paréntesis
- EOQ: Busca `Demanda`, `Costo pedido/mantenimiento`
- Colas: Busca `λ`, `μ` o tasas de llegada/servicio

**Extensión (agregar nuevo problema)**:
```python
def detectar_tipo_con_ia(pregunta):
    # ...
    
    # Tu nuevo tipo
    if "patrón_nuevo" in pregunta_lower:
        return "nuevo_tipo"
    
    # Si nada funciona, usar Groq
    return detectar_con_groq(pregunta)
```

### 2. `core/router.py`

**Responsabilidad**: Enrutar a solver apropiado

**Función principal**:
```python
def resolver(pregunta):
    """Detecta tipo y resuelve"""
    tipo = detectar_tipo_con_ia(pregunta)
    
    if tipo == "pert":
        return resolver_pert(pregunta)
    elif tipo == "lp":
        return resolver_lp(pregunta)
    # ... etc
```

**Para agregar nuevo solver**:
```python
def resolver(pregunta):
    tipo = detectar_tipo_con_ia(pregunta)
    
    # ... solvers existentes ...
    
    elif tipo == "mi_solver":
        return resolver_mi_tipo(pregunta)
    
    else:
        return "Tipo no identificado"
```

### 3. `solvers/` - Directorio de Solvers

Cada solver es un módulo Python con función `resolver_TIPO(texto)`

**Estructura típica**:
```python
# solvers/mi_solver.py

import re

def resolver_mi_tipo(texto):
    """
    Resuelve problema de tipo "mi_tipo"
    
    Args:
        texto (str): Descripción del problema
        
    Returns:
        str: Resultado formateado o mensaje de error
    """
    try:
        # 1. Parsear entrada
        datos = parsear_entrada(texto)
        
        # 2. Validar
        if not validar(datos):
            return "⚠️ Error en validación"
        
        # 3. Resolver
        resultado = algoritmo_especifico(datos)
        
        # 4. Formatear salida
        return formatear_resultado(resultado)
        
    except Exception as e:
        return f"⚠️ Error: {str(e)}"


def parsear_entrada(texto):
    """Extrae datos del texto"""
    # Usar regex, string split, etc.
    pass


def validar(datos):
    """Valida que datos sean válidos"""
    # Checks de lógica
    pass


def algoritmo_especifico(datos):
    """Implementa el algoritmo"""
    # Lógica principal
    pass


def formatear_resultado(resultado):
    """Formatea como tabla/texto legible"""
    # Crear output bonito
    pass
```

### 4. `ai/groq.py`

**Responsabilidad**: Integración con Groq API

```python
from groq import Groq

def explicar_con_groq(tipo_problema, resultado):
    """Genera explicación con IA"""
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    
    prompt = f"""
    Problema: {tipo_problema}
    Resultado: {resultado}
    
    Explica brevemente por qué este es el resultado óptimo.
    """
    
    chat = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="mixtral-8x7b-32768",
    )
    
    return chat.choices[0].message.content
```

### 5. `ai/embeddings.py`

**Responsabilidad**: Recuperar contexto del libro Hillier

```python
def obtener_contexto_hillier(query):
    """
    Busca información en PDF del libro
    
    Returns:
        str: Fragmentos relevantes del libro
    """
    # Cargar PDF
    # Hacer búsqueda por tokens
    # Retornar fragmentos más similares
    pass
```

---

## Agregar Nuevo Tipo de Problema

### Paso 1: Crear Solver

**Archivo**: `solvers/nombre_nuevo.py`

```python
# solvers/nombre_nuevo.py

def resolver_nombre_nuevo(texto):
    """Resuelve problemas de nombre_nuevo"""
    try:
        # Tu lógica aquí
        resultado = {"metrica1": 10, "metrica2": 20}
        return formatear(resultado)
    except:
        return None


def formatear(resultado):
    """Formatea para mostrar"""
    return f"Métrica 1: {resultado['metrica1']}\nMétrica 2: {resultado['metrica2']}"
```

### Paso 2: Registrar en Router

**Archivo**: `core/router.py`

```python
from solvers.nombre_nuevo import resolver_nombre_nuevo

def resolver(pregunta):
    tipo = detectar_tipo_con_ia(pregunta)
    
    # ... casos existentes ...
    
    elif tipo == "nombre_nuevo":
        return resolver_nombre_nuevo(pregunta)
```

### Paso 3: Agregar Detección

**Archivo**: `core/detector_ia.py`

```python
def detectar_tipo_con_ia(pregunta):
    # ... heurísticas existentes ...
    
    # Tu nueva heurística
    if "palabra_clave_1" in pregunta_lower and "palabra_clave_2" in pregunta_lower:
        return "nombre_nuevo"
    
    # Fallback a Groq
```

### Paso 4: Escribir Tests

**Archivo**: `tests/test_nombre_nuevo.py`

```python
import pytest
from solvers.nombre_nuevo import resolver_nombre_nuevo

class TestNombreNuevo:
    def test_caso_basico(self):
        resultado = resolver_nombre_nuevo("descripcion basica")
        assert resultado is not None
    
    def test_caso_ejemplo(self):
        resultado = resolver_nombre_nuevo("ejemplo del libro")
        assert "métrica" in resultado.lower()
```

**Ejecutar**:
```bash
pytest tests/test_nombre_nuevo.py -v
```

---

## Modificar Parsers Existentes

### Ejemplo: Mejorar Parser LP

**Archivo**: `solvers/lp.py`

Ubicar la función `parsear_restricciones()`:

```python
def parsear_restricciones(texto):
    """Extrae restricciones del formato"""
    # Busca líneas con: <=, >=, =
    # Extrae variable y coeficientes
    
    # PROBLEMA: No soporta desigualdades complejas tipo "2x + 3y - z >= 10"
    # SOLUCIÓN: Mejorar regex
    
    # Antes:
    # match = re.search(r'(\w+)\s*([<>=]+)\s*(\d+)', linea)
    
    # Después:
    pattern = r'([^<>=]+)\s*([<>=]+)\s*([^<>=]+)'
    # Ahora captura el lado completo izquierdo y derecho
```

---

## Refactoring y Mejoras

### 1. Agregar Cache

```python
from functools import lru_cache

@lru_cache(maxsize=100)
def detectar_tipo_con_ia(pregunta):
    """Con cache de últimos 100 problemas"""
    # ...
```

### 2. Agregar Logging

```python
import logging

logger = logging.getLogger(__name__)

def resolver_pert(texto):
    logger.info(f"Resolviendo PERT: {len(texto)} caracteres")
    try:
        # ...
    except Exception as e:
        logger.error(f"Error en PERT: {e}")
        return None
```

### 3. Agregar Tipado

```python
from typing import Dict, List, Optional

def resolver_transporte(
    texto: str,
    verbose: bool = False
) -> Optional[str]:
    """
    Args:
        texto: Descripción del problema
        verbose: Mostrar pasos intermedios
        
    Returns:
        Resultado o None si error
    """
    pass
```

---

## Testing

### Estructura de Tests

```
tests/
├── conftest.py           # Fixtures compartidas
├── test_pert.py         # Tests por solver
├── test_lp.py
├── test_flujo.py
├── test_web.py          # Tests de API
└── test_integration.py  # Tests end-to-end
```

### Escribir Test

```python
# tests/test_mi_solver.py

import pytest
from solvers.mi_solver import resolver_mi_tipo

class TestMiSolver:
    """Tests para mi_solver"""
    
    @pytest.fixture
    def problema_simple(self):
        """Fixture: problema de prueba"""
        return "descripción de problema simple"
    
    def test_caso_basico(self, problema_simple):
        """Test básico"""
        resultado = resolver_mi_tipo(problema_simple)
        
        assert resultado is not None
        assert isinstance(resultado, str)
    
    def test_valores_esperados(self):
        """Test con valores conocidos"""
        problema = "tu problema con resultado conocido"
        resultado = resolver_mi_tipo(problema)
        
        assert "valor_esperado" in resultado
    
    def test_error_handling(self):
        """Test que maneja errores"""
        resultado = resolver_mi_tipo("texto completamente inválido")
        
        # Debería retornar None o mensaje de error, no crash
        assert resultado is None or "error" in resultado.lower()
```

**Ejecutar**:
```bash
pytest tests/test_mi_solver.py -v
pytest tests/ --cov=solvers  # Ver cobertura
```

---

## API REST (Opcional)

Para crear una API dedicada:

```python
# api.py

from flask import Flask, request, jsonify
from core.router import resolver

app = Flask(__name__)

@app.route('/api/resolver', methods=['POST'])
def api_resolver():
    """
    POST /api/resolver
    
    Body:
    {
        "problema": "texto del problema"
    }
    
    Response:
    {
        "tipo": "pert",
        "resultado": "tabla..."
    }
    """
    datos = request.json
    problema = datos.get('problema', '')
    
    resultado = resolver(problema)
    
    return jsonify({
        "resultado": resultado,
        "timestamp": datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True)
```

**Usar**:
```bash
curl -X POST http://localhost:5000/api/resolver \
  -H "Content-Type: application/json" \
  -d '{"problema":"A(3) B(4), A→B"}'
```

---

## Debugging

### 1. Imprimir Variables Intermedias

```python
def resolver_pert(texto):
    # ...
    datos = parsear(texto)
    print(f"DEBUG: datos parseados = {datos}")  # ← Agregar debug
    
    resultado = calcular(datos)
    print(f"DEBUG: resultado intermedio = {resultado}")
    
    return formatear(resultado)
```

### 2. Usar Debugger

```bash
# Ejecutar con debugger
python -m pdb main.py

# En el código:
import pdb; pdb.set_trace()  # Pausa aquí
```

### 3. Tests para Debug

```python
def test_debug():
    """Test específico para debugging"""
    texto = "mi problema problemático"
    
    # Paso 1
    datos = parsear(texto)
    print(f"Datos: {datos}")
    assert datos is not None
    
    # Paso 2
    resultado = calcular(datos)
    print(f"Resultado: {resultado}")
    assert "esperado" in resultado
```

---

## Performance

### Profiling

```python
import cProfile
import pstats

def main():
    resolver("problema grande")

if __name__ == '__main__':
    profiler = cProfile.Profile()
    profiler.enable()
    
    main()
    
    profiler.disable()
    stats = pstats.Stats(profiler)
    stats.sort_stats('cumtime')
    stats.print_stats(10)  # Top 10 funciones
```

### Optimización

```python
# ANTES: Lento
def buscar(lista, valor):
    for x in lista:
        if x == valor:
            return x
    return None

# DESPUÉS: Rápido (usa conjunto)
def buscar(conjunto, valor):
    return valor in conjunto
```

---

## Documentación de Código

### Docstrings

```python
def resolver_mi_tipo(texto: str) -> Optional[str]:
    """
    Resuelve problema de tipo "mi_tipo".
    
    Soporta problemas con:
    - Variables continuas
    - Restricciones lineales
    - Función objetivo no-lineal
    
    Args:
        texto: Descripción natural del problema.
               Debe contener "palabra_clave" para detectarse.
    
    Returns:
        str: Tabla formateada con resultados.
             None si error en parsing.
    
    Raises:
        ValueError: Si restricciones son inconsistentes.
    
    Examples:
        >>> resolver_mi_tipo("problema simple")
        'Resultado: ...'
        
        >>> resolver_mi_tipo("problema complejo")
        'Resultado: ...'
    
    Notes:
        - Usa algoritmo X para optimización
        - Soporta hasta 100 variables
        - Complejidad O(n²)
    
    See Also:
        resolver_otro_tipo: Para problemas similares
    """
    pass
```

---

## Checklist para Contribuciones

- [ ] Código escrito y funcionando
- [ ] Tests escritos (cobertura > 80%)
- [ ] Documentación de función
- [ ] No hay hardcoding de valores
- [ ] Manejo de errores graceful
- [ ] Sigue convenciones del proyecto
- [ ] Tipos anotados (type hints)
- [ ] Funciona en Windows y Linux
- [ ] No hay imports no usados
- [ ] Commit message descriptivo

---

## Referencias

- **scipy.optimize**: [Documentación oficial](https://docs.scipy.org/doc/scipy/reference/optimize.html)
- **PuLP**: [PuLP documentation](https://coin-or.github.io/pulp/)
- **Groq API**: [Console Groq](https://console.groq.com/docs)
- **Hillier**: *Introduction to Operations Research*, 12ª edición

---

**Última actualización**: 2026-04-28
