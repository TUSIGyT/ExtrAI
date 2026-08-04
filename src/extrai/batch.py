import json
import time

import ollama

from extrai.utils import parse_llm_json


def read_jsonl(input_file, start_line=1):
    """
    Lee archivos JSONL línea por línea
    comenzando desde start_line.
    """

    with open(input_file, "r", encoding="utf-8") as f:

        for line_number, line in enumerate(f, start=1):

            if line_number < start_line:
                continue

            line = line.strip()

            if not line:
                continue

            try:
                yield json.loads(line)

            except json.JSONDecodeError as e:

                raise ValueError(f"Invalid JSONL at line {line_number}: {e}")


def call_ollama(model, prompt, text, retries=3):

    last_error = None

    for attempt in range(retries):

        try:

            response = ollama.chat(
                model=model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text},
                ],
                options={"temperature": 0, "num_ctx": 4096, "thinking": False},
                keep_alive="5m",
            )

            return response

        except Exception as e:

            last_error = e

            wait = 5 * (attempt + 1)

            print(f"Ollama error ({attempt+1}/{retries}). " f"Retrying in {wait}s...")

            time.sleep(wait)

    raise last_error


def process_batch(
    input_file,
    prompt_file,
    json_property,
    model,
    output_file,
    start_line=1,
):

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()

    processed = 0

    # usar "a" para continuar un procesamiento
    # usar "w" para comenzar desde cero
    with open(output_file, "a", encoding="utf-8") as f_out:

        print(f"Starting from line: {start_line}")

        for item in read_jsonl(input_file, start_line=start_line):

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

            if processed % 50 == 0:

                print(
                    f"Processed {processed} news " f"(starting at line {start_line})..."
                )

    print(f"Finished. Total processed: {processed}")
