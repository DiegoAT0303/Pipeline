# Se eliminó 'import os' que no se usaba (soluciona F401)
from pathlib import Path

print("\nBienvenido al generador de pipelines para GitHub Actions.\n")

# --- Versión de Python ---
# Se divide el prompt en una variable para acortar la línea (soluciona E501)
version_prompt = "¿Qué versión mínima de Python quieres usar? (Ejemplo: 3.8): "
version = input(version_prompt) or "3.8"


# --- TEST AUTOMATIZADOS ---
usar_test = input("¿Quieres incluir tests automáticos? (S/n): ") or "s"
steps_test = ''
if usar_test.lower() == 's':
    # Se divide el prompt para acortar la línea (soluciona E501)
    cmd_test_prompt = "¿Comando para ejecutar tus tests? (por defecto: 'pytest'): "
    cmd_test = input(cmd_test_prompt) or "pytest"
    # La indentación (6 espacios) aquí es para el archivo YML final
    steps_test = f"""
      - name: Ejecutar tests
        run: {cmd_test}"""


# --- ANALISIS ESTATICO ---
usar_linter = input("¿Quieres análisis de código estático? (S/n): ") or "s"
steps_linter = ''
linter_pkg = ''
if usar_linter.lower() == 's':
    # El input multilinea ya estaba bien
    linter = input(
        "¿Qué herramienta usarás para código estático? "
        "('flake8', 'pylint', etc. por defecto: 'flake8'): "
    ) or "flake8"
    linter_pkg = linter.split()[0]
    
    # Se divide el prompt para acortar la línea (soluciona E501)
    linter_prompt = f"Comando para análisis estático (por defecto: '{linter} .'): "
    cmd_linter = input(linter_prompt) or f"{linter} ."
    steps_linter = f"""
      - name: Instalar herramienta de análisis estático
        run: pip install {linter_pkg}
      - name: Análisis de código estático ({linter})
        run: {cmd_linter}"""


# --- ANALISIS DE SEGURIDAD ---
usar_security = input("¿Quieres análisis de seguridad? (S/n): ") or "s"
steps_security = ''
security_pkg = ''
if usar_security.lower() == 's':
    # Se divide el prompt largo usando paréntesis (soluciona E501)
    security_prompt = (
        "¿Herramienta para análisis de seguridad ('bandit', 'safety', etc. "
        "por defecto: 'bandit'): "
    )
    security = input(security_prompt) or "bandit"
    security_pkg = security.split()[0]

    # Se divide el prompt para acortar la línea (soluciona E501)
    cmd_prompt = f"Comando para análisis de seguridad (por defecto: '{security} .'): "
    cmd_security = input(cmd_prompt) or f"{security} ."
    steps_security = f"""
      - name: Instalar herramienta de análisis de seguridad
        run: pip install {security_pkg}
      - name: Análisis de seguridad ({security})
        run: {cmd_security}"""


# --- Generar archivo ---
workflow_file = Path(".github/workflows/ci.yml")
workflow_file.parent.mkdir(parents=True, exist_ok=True)

# Plantilla para pipeline completo
# Los {steps_...} ya incluyen el salto de línea y la indentación correcta
yml = f'''name: CI

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v4
    - name: Configurar Python {version}
      uses: actions/setup-python@v5
      with:
        python-version: '{version}'
    - name: Instalar dependencias
      run: |
        python -m pip install --upgrade pip
        pip install -r requirements.txt{steps_linter}{steps_security}{steps_test}
'''

with open(workflow_file, "w", encoding="utf-8") as f:
    f.write(yml)

print(f"\n¡Listo! Archivo de workflow creado en: {workflow_file}\n")
