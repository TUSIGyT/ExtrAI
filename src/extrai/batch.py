import json
import re
from pathlib import Path

import ollama


def parse_llm_json(content):
    """
    Limpia bloques markdown y convierte la respuesta del LLM
    en un diccionario Python.
    """

    content = re.sub(r"```(?:json)?|```", "", content).strip()

    return json.loads(content)


def read_jsonl(input_file):
    """
    Lee un archivo JSONL línea por línea.
    Cada línea debe ser un objeto JSON independiente.
    """

    with open(input_file, "r", encoding="utf-8") as f:

        for line in f:

            if line.strip():
                yield json.loads(line)


def process_batch(input_file, prompt_file, json_property, model, output_file):

    input_file = Path(input_file)
    output_file = Path(output_file)

    with open(prompt_file, "r", encoding="utf-8") as f:

        prompt = f.read()

    with open(output_file, "w", encoding="utf-8") as f_out:

        for item in read_jsonl(input_file):

            news_id = item.get("id")
            text = item.get(json_property)

            result = {"model": model, "id": news_id}

            try:

                response = ollama.chat(
                    model=model,
                    messages=[
                        {"role": "system", "content": prompt},
                        {"role": "user", "content": text},
                    ],
                )

                extracted_data = parse_llm_json(response["message"]["content"])

                result.update(extracted_data)

            except Exception as e:

                result.update(
                    {
                        "error": str(e),
                        "raw_response": (
                            response["message"]["content"]
                            if "response" in locals()
                            else None
                        ),
                    }
                )

            f_out.write(json.dumps(result, ensure_ascii=False) + "\n")
