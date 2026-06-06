import json
import re
import time

import ollama


def parse_llm_json(content):
    """
    Extrae JSON de respuestas LLM.
    Acepta bloques markdown: json, python, etc.
    """

    content = content.strip()

    # Caso: respuesta dentro de bloque markdown
    match = re.search(r"```[a-zA-Z0-9_-]*\s*(.*?)```", content, re.DOTALL)

    if match:
        content = match.group(1).strip()

    # Caso: texto adicional antes/después del JSON
    # busca el primer objeto JSON
    match = re.search(r"\{.*\}", content, re.DOTALL)

    if match:
        content = match.group(0)

    if not content:
        raise ValueError("LLM returned empty response")

    return json.loads(content)


def read_jsonl(input_file):
    """
    Lee archivos JSONL línea por línea.
    """

    with open(input_file, "r", encoding="utf-8") as f:

        for line_number, line in enumerate(f, start=1):

            line = line.strip()

            if not line:
                continue

            try:

                yield json.loads(line)

            except json.JSONDecodeError as e:

                raise ValueError(f"Invalid JSONL at line {line_number}: {e}")


def call_ollama(model, prompt, text, retries=3):
    """
    Ejecuta Ollama con reintentos.
    """

    last_error = None

    for attempt in range(retries):

        try:

            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
                options={"temperature": 0, "num_ctx": 4096},
                keep_alive="5m",
            )

            return response

        except Exception as e:

            last_error = e

            wait = 5 * (attempt + 1)

            print(f"Ollama error ({attempt+1}/{retries}). " f"Retrying in {wait}s...")

            time.sleep(wait)

    raise last_error


def process_batch(input_file, prompt_file, json_property, model, output_file):

    with open(prompt_file, "r", encoding="utf-8") as f:

        prompt = f.read()

    processed = 0

    with open(output_file, "w", encoding="utf-8") as f_out:

        for item in read_jsonl(input_file):

            processed += 1

            news_id = item.get("id")

            text = item.get(json_property)

            result = {"model": model, "id": news_id}

            try:

                response = call_ollama(model, prompt, text)

                raw_response = response["message"]["content"]

                extracted_data = parse_llm_json(raw_response)

                result.update(extracted_data)

            except Exception as e:

                result.update(
                    {
                        "error": str(e),
                        "raw_response": (
                            raw_response if "raw_response" in locals() else None
                        ),
                    }
                )

            f_out.write(json.dumps(result, ensure_ascii=False) + "\n")

            # libera referencia local
            if processed % 50 == 0:

                print(f"Processed {processed} news...")

    print(f"Finished. Total processed: {processed}")
