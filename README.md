# ExtrAI - Extracción Automática de Información con LLM

ExtrAI es un proyecto desarrollado para la extracción automática de información sobre siniestros viales ocurridos en la provincia de Misiones (Argentina), utilizando noticias recopiladas del diario Primera Edición.

El sistema utiliza modelos de Lenguaje Natural (LLM) ejecutados localmente mediante [Ollama](https://ollama.com/), permitiendo transformar textos periodísticos no estructurados en datos estructurados en formato JSON.

---

# Requisitos

Antes de ejecutar el proyecto es necesario instalar:

- [Ollama](https://ollama.com/download)
- Modelos LLM compatibles descargados desde [Ollama Models](https://ollama.com/search)

Ejemplo:

```bash
ollama pull qwen3:8b
````

Verificar instalación:

```bash
ollama --version
```

---

# Instalación

Clonar el repositorio:

```bash
git clone git@github.com:TUSIGyT/ExtrAI.git
```

Acceder al proyecto:

```bash
cd ExtrAI
```

---

## Opción 1 - Instalación con venv

Crear ambiente virtual:

```bash
python -m venv .venv
```

Activar ambiente:

Linux/macOS:

```bash
source .venv/bin/activate
```

Actualizar pip:

```bash
pip install --upgrade pip
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

---

## Opción 2 - Instalación con Poetry (recomendado)

Instalar dependencias:

```bash
poetry install
```

Las herramientas del proyecto pueden ejecutarse utilizando:

```bash
poetry run <comando>
```

---

# Estructura del proyecto

```
ExtrAI/
│
├── news/
│   └── archivos JSON con noticias
│
├── src/
│   └── extrai/
│       ├── prompts/
│       │   └── prompts utilizados por los modelos
│       │
│       ├── post-processing/
│       │   └── limpieza y normalización de resultados
│       │
│       ├── batch.py
│       ├── cli.py
│       └── data_preparation.py
│
└── results/
    └── resultados de extracción
```

---

# Flujo de trabajo

El proceso de extracción está compuesto por tres etapas:

1. Preparación de los datos
2. Extracción mediante LLM
3. Post-procesamiento de resultados

---

# 1. Preparación de datos

Los modelos LLM reciben como entrada un texto consolidado dentro de una propiedad JSON.

La herramienta `data_preparation` crea una nueva propiedad llamada `content`, concatenando las informaciones disponibles en cada noticia.

Ejemplo:

Entrada:

```json
{
    "title": "Accidente vial",
    "date": "2024-01-01",
    "location": "Posadas"
}
```

Salida:

```json
{
    "title": "Accidente vial",
    "date": "2024-01-01",
    "location": "Posadas",
    "content": "title: Accidente vial; date: 2024-01-01; location: Posadas"
}
```

Ejecutar:

```bash
poetry run python src/extrai/data_preparation.py \
    --input news/sample/sample_primera_edicion_siniestros_viales_2024.json \
    --output news/sample/sample_w_content.json
```

---

# 2. Extracción con modelos LLM

ExtrAI ejecuta el mismo prompt sobre múltiples noticias utilizando diferentes modelos locales.

Los elementos necesarios son:

* Archivo JSON con noticias.
* Prompt de extracción.
* Modelo LLM instalado en Ollama.

Ejemplo:

```bash
poetry run extrai-batch \
    --input news/sample/sample_w_content.json \
    --prompt src/extrai/prompts/prompt_v3.txt \
    --property content \
    --model qwen3:8b \
    --output results/qwen3_8b_result.json
```

---

# Ejecutar múltiples modelos

Ejemplo para comparar diferentes LLM:

```bash
for model in gemma3:4b Granite4.1:8b qwen3:8b llama3:8b; do

    poetry run extrai-batch \
        --input news/sample/sample_w_content.json \
        --prompt src/extrai/prompts/prompt_final.txt \
        --property content \
        --model $model \
        --output results/${model}_result.json

done
```

Es posible, también,  procesar el archivos JSONL a partir de una línea:

```commandline
poetry run extrai-batch \
    --input news/sample/sample_w_content.jsonl \
    --start-line 2 \
    --prompt src/extrai/prompts/prompt_v3.txt \
    --property content \
    --model gemma3:4b \
    --output results/gemma3_4b_result.jsonl
```

---

# 3. Post-procesamiento

Algunos modelos pueden devolver información adicional junto al JSON esperado.

Por ese motivo se incluye una etapa de limpieza:

```
src/extrai/post-processing/data_cleaning.py
```

Esta etapa permite normalizar las respuestas generadas por los modelos antes de su análisis posterior.

---

# Resultados

Los resultados generados se almacenan en:

```
results/
```

Ejemplo:

```
results/
├── qwen3:8b_result.json
├── deepseek-r1:8b_result.json
└── llama3.2_result.json
```

Cada archivo contiene las noticias procesadas junto con la información extraída por el modelo LLM.
