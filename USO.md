# Guía de Uso - Calculadora IO

## Inicio Rápido

### Opción 1: Interfaz Web (Recomendado)

```bash
# Activar venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Iniciar servidor
python web.py

# Abrir navegador en http://localhost:5000
```

### Opción 2: Línea de Comandos

```bash
python main.py
# Ingresar problemas al prompt (escribir "FIN" para salir)
```

---

## Ejemplos por Tipo de Problema

### 1. PERT (Ruta Crítica)

**Ejemplo Simple:**
```
A(3) B(4) C(5) D(4) E(2), A→B→D→E, A→C, C→E
```

**Explicación:**
- A, B, C, D, E son actividades con duraciones en paréntesis
- A→B→D→E: A debe completarse antes de B, B antes de D, etc.
- A→C, C→E: Caminos alternativos

**Salida esperada:**
```
Actividad | ES EF LS LF Holgura
-----------------------------------
A | 0  3  2  5   2
B | 0  4  1  5   1
C | 0  5  0  5   0
D | 0  4  1  5   1
E | 0  2  3  5   3

Ruta crítica: C
Duración total: 5 días
```

**Interpretación:**
- **ES (Earliest Start)**: Momento más temprano de inicio
- **EF (Earliest Finish)**: Momento más temprano de fin
- **LS (Latest Start)**: Momento más tardío sin retrasarse
- **LF (Latest Finish)**: Momento más tardío de fin
- **Holgura**: Días que puede retrasarse sin afectar el proyecto
- **Ruta Crítica**: Actividades sin holgura (retrasarse = atraso del proyecto)

---

### 2. Flujo Máximo

**Ejemplo Simple:**
```
Nodo 1: 2(10) 3(10)
Nodo 2: 3(2) 4(4) 5(8)
Nodo 3: 4(9) 5(9)
Nodo 4: 5(10)
```

**Explicación:**
- Nodo 1 es la fuente
- Capacidades entre paréntesis
- El algoritmo encuentra el máximo flujo a los nodos finales

**Salida esperada:**
```
Flujo máximo: 15 unidades
Rutas:
1→2→4→5: 4 unidades
1→2→5: 4 unidades
1→3→4→5: 1 unidad
...
```

---

### 3. Problema de Transporte

**Ejemplo:**
```
Oferta: Fábrica_A(100) Fábrica_B(150)
Demanda: Almacén_1(80) Almacén_2(90) Almacén_3(80)
Fábrica_A a Almacén_1: 4
Fábrica_A a Almacén_2: 6
Fábrica_A a Almacén_3: 8
Fábrica_B a Almacén_1: 5
Fábrica_B a Almacén_2: 3
Fábrica_B a Almacén_3: 7
```

**Salida:**
```
Asignación óptima:
Fábrica_A → Almacén_1: 80 unidades @ $4 = $320
Fábrica_A → Almacén_2: 20 unidades @ $6 = $120
Fábrica_B → Almacén_2: 70 unidades @ $3 = $210
Fábrica_B → Almacén_3: 80 unidades @ $7 = $560

COSTO TOTAL: $1,210
```

---

### 4. EOQ (Cantidad Económica de Pedido)

**Ejemplo:**
```
Demanda anual D = 10000 unidades
Costo por pedido S = $100
Costo de mantenimiento H = $2 por unidad por año
```

**Salida:**
```
Cantidad óptima Q* = 1000 unidades
Costo total anual = $2000

Número de pedidos por año = 10
Tiempo entre pedidos = 36.5 días
Costo anual de ordenar = $1000
Costo anual de mantener = $1000
```

**Interpretación:**
- Q* = √(2DS/H)
- Hacer 10 pedidos anuales de 1000 unidades cada uno
- El equilibrio es entre costo de ordenar y costo de mantener inventario

---

### 5. Teoría de Colas (M/M/1)

**Ejemplo:**
```
Tasa de llegada λ = 10 clientes por hora
Tasa de servicio μ = 12 clientes por hora
```

**Salida:**
```
MÉTRICAS DE COLAS (Sistema M/M/1)

Factor de utilización (ρ) = 83.3%
Número promedio de clientes en el sistema (L) = 5
Número promedio en cola (Lq) = 4.17
Tiempo promedio en sistema (W) = 30 minutos
Tiempo promedio en cola (Wq) = 25 minutos
Probabilidad de que esté libre (P₀) = 16.7%
Probabilidad de n clientes (Pn):
  P₀ = 16.7%
  P₁ = 13.9%
  P₂ = 11.6%
  ...
```

**Interpretación:**
- Sistema está ocupado 83% del tiempo
- En promedio hay 5 clientes (dentro + cola)
- Espera promedio en cola = 25 minutos
- Si ρ > 1, el sistema colapsaría (más llegadas que capacidad de servicio)

---

### 6. Programación Lineal (LP)

**Ejemplo 1 - Maximización simple:**
```
Maximizar: 3x + 2y
s.a.
x + y <= 4
x <= 2
x >= 0, y >= 0
```

**Salida:**
```
Solución óptima encontrada
Z (máximo) = 8

Variables:
x = 2
y = 2

Restricciones activas:
- x + y = 4
- x = 2
```

**Ejemplo 2 - Variables enteras/binarias:**
```
Maximizar: 50x + 40y + 30z
s.a.
2x + 3y + z <= 10
x + y + 2z <= 8
x, y >= 0
z ∈ {0, 1}  # Variable binaria (0 o 1)
```

**Salida:**
```
Solución óptima
Z = 180

x = 4
y = 0
z = 1
```

---

### 7. Problemas No-Lineales

#### a) Optimización de Beneficio

**Ejemplo:**
```
Función de demanda: P = 100 - 0.5Q
Costo unitario: c = 20
Maximizar beneficio = (P - c) × Q
```

**Salida:**
```
Beneficio máximo encontrado

Cantidad óptima Q* = 80 unidades
Precio óptimo P* = 60 $/unidad
Beneficio máximo B* = $3,200

Análisis:
- Costo total = 1,600
- Ingreso = 4,800
- Beneficio neto = 3,200
```

#### b) Problema de Almacén

**Ejemplo:**
```
Restricción de capacidad: xy = 625
Costo de construcción: 400x
Costo de almacenamiento: 2y
Minimizar costo total = 400x + 2y
```

**Salida:**
```
Dimensiones óptimas encontradas

x (largo) = 25.82 metros
y (ancho) = 24.21 metros
Costo total = $7,745.97

Análisis:
- Costo construcción = $10,328
- Costo almacenamiento = $48.42
```

---

## Interfaz Web - Guía Completa

### Formulario Principal

```
┌─────────────────────────────────────┐
│ CALCULADORA DE IO                   │
│                                     │
│ [Área de texto para enunciado]      │
│ ┌─────────────────────────────────┐ │
│ │ Ingresa tu problema aquí:       │ │
│ │                                 │ │
│ │                                 │ │
│ └─────────────────────────────────┘ │
│                                     │
│  [RESOLVER]                         │
│                                     │
└─────────────────────────────────────┘
```

### Tarjetas de Acceso Rápido

Botones para cargar ejemplos predefinidos:
- 📈 PERT
- 🌊 Flujo
- 🚚 Transporte
- 📦 EOQ
- 👥 Colas
- ➗ LP
- 🔢 NLP

### Resultado

Después de hacer clic en RESOLVER:

```
┌─────────────────────────────────────┐
│ RESULTADO                           │
│                                     │
│ [Tabla con resultados]              │
│                                     │
│ [Explicación de IA (si aplica)]     │
│                                     │
│ [EXPORTAR PDF] [COPIAR TXT]         │
│                                     │
└─────────────────────────────────────┘
```

### Historial

- Ver todos los problemas resueltos
- Clickear para ver detalles
- Exportar todo como JSON
- Limpiar historial

---

## Tips y Trucos

### 1. Formatos Aceptados

```
# PERT - Variantes aceptadas:
A(3) → B(4) → C(5)     # Flechas Unicode
A(3) -> B(4) -> C(5)    # Flechas ASCII
A(3) B(4) C(5), A→B→C  # Combinado

# Transporte - Variantes:
A-X: 10                 # Guión
A→X: 10                 # Flecha
A_X: 10                 # Subguión (si funciona)
```

### 2. Unidades

El sistema **no asume unidades** por defecto:
- Especificar claramente: "10 unidades", "5 horas", "$100"
- Importante para explicación correcta

### 3. Problemas Grandes

Si tienes 50+ variables LP:
- Puede tardar más tiempo
- Usar descripción clara de restricciones
- Considerar descomponer en problemas menores

### 4. Precisión

- **Decimales**: Usar punto (.) no coma (,)
- **Números grandes**: 1000000, no 1,000,000
- **Resultados**: Redondeados a 2 decimales

---

## Errores Comunes y Soluciones

### ❌ "No se pudo detectar el tipo de problema"

**Causa**: Formato no reconocido, problema ambiguo o información incompleta

**Solución**:
```
MAL:  "necesito optimizar cosas"
BIEN: "Maximizar 3x + 2y s.a. x + y <= 10"

MAL:  "Nodo1(A) Nodo2(B) Nodo3(C)"
BIEN: "Nodo 1: 2(10) 3(5), Nodo 2: 3(4)"

MAL:  "Demanda diaria = 50 unid. Tiempo entrega = 4 días."
BIEN: "EOQ: Demanda anual 18,250 unidades, costo pedido $100, 
       costo mantener $2/unidad/año, tiempo entrega 4 días"
```

**Tip**: Si tienes demanda diaria y lead time, necesitas también:
- Costo de ordenar (por pedido)
- Costo de mantener (por unidad por año)
- Entonces el sistema calculará Q* (cantidad óptima) y ROP (punto de reorden)

### ❌ "La ruta crítica es incorrecta"

**Verificar**:
- Todas las dependencias están especificadas
- No hay ciclos (A→B→A es inválido)
- Formato es consistente

### ❌ "LP infactible o no acotado"

**Causas comunes**:
- Restricciones contradictorias
- Solución ilimitada

**Ejemplo infactible**:
```
max x + y
s.a.
x + y >= 10
x + y <= 5  # Contradicción
x >= 0
```

### ❌ "Colas no estable (λ ≥ μ)"

**Significado**: La demanda es igual o mayor que la capacidad

**Solución**:
- Aumentar μ (capacidad de servicio)
- Reducir λ (tasa de llegada)
- Agregar más servidores (requiere modelo M/M/c)

---

## Exportación de Resultados

### PDF
```
[EXPORTAR PDF]
↓
Descarga archivo PDF con:
- Tabla de resultados
- Explicación
- Timestamp
```

### TXT
```
[COPIAR TXT]
↓
Copia a portapapeles (Ctrl+V para pegar)
```

### JSON (Historial)
```
[EXPORTAR HISTORIAL]
↓
Descarga JSON con todos los problemas resueltos
```

---

## Casos de Uso Reales

### Caso 1: Planificación de Proyecto

```
Input: PERT de construcción de casa
Output: 
- Duración total: 6 meses
- Ruta crítica: Cimientos → Estructura → Techo
- Holguras de otras tareas

Decisión: ¿Empezar acabados antes de terminar techo? NO
```

### Caso 2: Optimización de Inventario

```
Input: EOQ para tienda
Output:
- Pedir 500 unidades cada 10 días
- Costo total: $2,000/mes

Decisión: Negociar descuentos por volumen (1000 u)
```

### Caso 3: Asignación de Recursos

```
Input: LP con máquinas, horas, ganancias
Output:
- Producir 200 x, 150 y
- Ganancia máxima: $5,000

Decisión: Implementar esta producción
```

---

## Keyboard Shortcuts

| Atajo | Función |
|-------|---------|
| `Ctrl + Enter` | Resolver (en textarea) |
| `Ctrl + C` | Copiar resultado |
| `Ctrl + L` | Limpiar historial |
| `Ctrl + Shift + E` | Exportar PDF |

---

## FAQ

**P: ¿Puedo usar variables con nombres largos en LP?**
A: Sí, pero simplificar: "produccion_A" → "x1"

**P: ¿Qué precisión tiene?**
A: Float de 64-bit. Para finanzas críticas, usar Decimal.

**P: ¿El historial se guarda?**
A: Sí, en localStorage del navegador. Persistente hasta limpiar.

**P: ¿Funciona offline?**
A: NO, requiere API Groq para explicaciones.

**P: ¿Límite de variables?**
A: LP: 100+, PERT: 50+, sin límites teóricos.

---

**Última actualización**: 2026-04-28
