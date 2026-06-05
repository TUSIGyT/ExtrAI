import json
import re

import ollama


def parse_llm_json(content):

    content = re.sub(r"```(?:json)?|```", "", content).strip()

    return json.loads(content)


def process_batch(input_file, prompt_file, json_property, model, output_file):

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    with open(output_file, "w", encoding="utf-8") as f_out:

        for item in data:

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
