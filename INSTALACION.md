# Guía de Instalación - Calculadora IO

## Prerrequisitos

- **Python 3.14+** instalado y en PATH
- **pip** (gestor de paquetes)
- **Git** (opcional, para clonar)
- **Una API key de Groq** (gratis en [console.groq.com](https://console.groq.com))

---

## Instalación Paso a Paso

### 1. Descargar el Proyecto

**Opción A - Clonar con Git:**
```bash
git clone https://github.com/tu-repo/CALCULADORA_IO.git
cd CALCULADORA_IO
```

**Opción B - Descargar ZIP:**
```bash
# Descargar desde GitHub → Code → Download ZIP
# Extraer a carpeta deseada
cd CALCULADORA_IO
```

### 2. Crear Entorno Virtual

```bash
# Windows
python -m venv venv

# Linux/Mac
python3 -m venv venv
```

**¿Por qué virtual env?**
- Aísla dependencias del proyecto
- Evita conflictos con otros proyectos Python
- Facilita reproducibilidad

### 3. Activar Entorno Virtual

**Windows (PowerShell):**
```powershell
venv\Scripts\Activate.ps1
```

**Windows (CMD):**
```cmd
venv\Scripts\activate.bat
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

**Verificar activación:**
```bash
# Deberías ver "(venv)" al inicio de la línea
(venv) $ _
```

### 4. Instalar Dependencias

```bash
pip install -r requirements.txt
```

**¿Qué se instala?**
```
groq==0.37.1              # API Groq para IA
langchain-groq==1.1.2     # Integración LangChain
flask==2.3.3              # Servidor web
scipy==1.17.1             # Optimización matemática
numpy==2.4.4              # Álgebra lineal
pandas==2.2.3             # Análisis de datos
pulp==3.3.0               # Programación lineal
reportlab==4.4.1          # Generación PDF
pypdf==6.10.2             # Lectura PDF
python-dotenv==1.0.0      # Variables de entorno
pytest==9.0.3             # Testing (opcional)
```

### 5. Obtener API Key de Groq

1. Ir a [console.groq.com](https://console.groq.com)
2. Crear cuenta o login
3. Navegar a **API Keys**
4. Crear nueva key
5. Copiar clave (aparece una sola vez)

**⚠️ Importante:**
- Guardar en lugar seguro
- NO compartir públicamente
- Si se expone, regenerar inmediatamente

### 6. Configurar Variables de Entorno

**Crear archivo `.env` en raíz del proyecto:**

```bash
# Windows PowerShell
@"
GROQ_API_KEY=tu_clave_aqui
"@ | Out-File -Encoding UTF8 .env

# Linux/Mac
echo "GROQ_API_KEY=tu_clave_aqui" > .env
```

**O editar manualmente:**
```
# .env (archivo de texto)
GROQ_API_KEY=gsk_xxxxxxxxxxxxx
```

**Verificar configuración:**
```bash
# Python debería cargar la key
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('✓ Key cargada' if os.getenv('GROQ_API_KEY') else '✗ Key no encontrada')"
```

### 7. Verificar Instalación

```bash
# Probar imports
python -c "import flask, groq, pulp, scipy; print('✓ Todas las dependencias OK')"

# Probar solver simple
python -c "from solvers.pert import resolver_pert; r = resolver_pert('A(2) B(3), A→B'); print(r if r else '✗ Error')"

# Probar web
python web.py
# Debería mostrar: "Running on http://localhost:5000"
```

> Nota: el entorno virtual del proyecto fue regenerado con Python 3.14 para alinearlo con el intérprete disponible actualmente en la máquina.

---

## Estructura de Carpetas Después de Instalación

```
CALCULADORA_IO/
├── venv/                      # ← Entorno virtual
│   ├── Scripts/               # (Windows)
│   ├── bin/                   # (Linux/Mac)
│   └── lib/                   # Packages instalados
├── .env                       # ← Tu API key (no versionar)
├── .gitignore                 # ← Ignora venv/ y .env
├── requirements.txt           # ← Lista de dependencias
├── README.md
├── main.py
├── web.py
├── solvers/
├── core/
├── ai/
├── templates/
├── static/
├── tests/
└── [otros archivos...]
```

---

## Actualizar Dependencias

```bash
# Upgrade pip
pip install --upgrade pip

# Actualizar todas las dependencias
pip install --upgrade -r requirements.txt

# Ver versiones instaladas
pip list
```

---

## Problemas Comunes

### ❌ Error: "Python not found"
```bash
# Verificar instalación
python --version

# Si no funciona, usar python3
python3 --version

# Añadir a PATH (Windows):
# 1. Ir a "Editar variables de entorno"
# 2. Buscar Python en C:\Users\[usuario]\AppData\Local\Programs\Python\
```

### ❌ Error: "No module named 'groq'"
```bash
# Asegurarse de tener venv activado
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Reinstalar
pip install groq
```

### ❌ Error: "GROQ_API_KEY not found"
```bash
# Verificar que .env existe en raíz
ls .env              # Linux/Mac
dir .env             # Windows

# Asegurar que el .env tiene el formato correcto
cat .env             # Debería mostrar: GROQ_API_KEY=gsk_...
```

### ❌ Error: "Port 5000 already in use"
```bash
# Usar puerto alternativo
python web.py --port=5001
# O matar proceso:
# Linux: lsof -ti:5000 | xargs kill -9
# Windows: netstat -ano | findstr :5000
```

### ❌ Error al ejecutar tests
```bash
# Asegurar pytest instalado
pip install pytest

# Ejecutar desde raíz del proyecto
cd /ruta/a/CALCULADORA_IO
pytest tests/
```

---

## Desarrollo (Opcional)

### Instalar en Modo Editable

```bash
# Permite editar código y cambios se reflejan inmediatamente
pip install -e .
```

### Dependencias de Desarrollo

```bash
# Instalar herramientas adicionales
pip install pytest pytest-cov black flake8 mypy

# Ver cobertura de tests
pytest --cov=solvers tests/
```

---

## Verificación Final

Ejecutar este script para validar la instalación completa:

```bash
# verify_installation.py
import sys
import importlib

modules = [
    'flask', 'groq', 'pulp', 'scipy', 
    'numpy', 'pandas', 'reportlab', 'pypdf'
]

print("Verificando instalación...")
print(f"Python {sys.version}")
print()

missing = []
for mod in modules:
    try:
        importlib.import_module(mod)
        print(f"✓ {mod}")
    except ImportError:
        print(f"✗ {mod}")
        missing.append(mod)

if missing:
    print(f"\nFalta instalar: {', '.join(missing)}")
    print("Ejecutar: pip install", " ".join(missing))
else:
    print("\n✓ ¡Instalación completa!")

# Probar API key
import os
from dotenv import load_dotenv
load_dotenv()
if os.getenv('GROQ_API_KEY'):
    print("✓ GROQ_API_KEY configurada")
else:
    print("✗ GROQ_API_KEY no encontrada en .env")
```

**Ejecutar:**
```bash
python verify_installation.py
```

---

## Próximos Pasos

1. ✅ Instalación completa
2. 📖 Leer [guía de uso](USO.md)
3. 🚀 Iniciar web: `python web.py`
4. 📝 Resolver problemas
5. 📊 Exportar resultados

---

## Soporte

Si tienes problemas:

1. **Verificar Python >= 3.13**: `python --version`
2. **Verificar venv activado**: Línea debe empezar con `(venv)`
3. **Reinstalar todo**:
   ```bash
   pip install --force-reinstall -r requirements.txt
   ```
4. **Crear issue** con:
   - Output completo del error
   - `python --version`
   - `pip list` (versiones instaladas)

---

**Última actualización**: 2026-04-28
