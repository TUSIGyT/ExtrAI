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

    results = []

    for item in data:

        text = item[json_property]
        news_id = item.get("id")

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
        )
        extracted_data = parse_llm_json(response["message"]["content"])

        results.append({"id": news_id, **extracted_data})

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(results, f, ensure_ascii=False, indent=4)
