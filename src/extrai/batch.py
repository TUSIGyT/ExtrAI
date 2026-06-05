import json
import ollama


def process_batch(input_file, prompt_file, json_property, model, output_file):

    with open(prompt_file, "r", encoding="utf-8") as f:
        prompt = f.read()

    with open(input_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    results = []

    for item in data:

        text = item[json_property]

        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text},
            ],
        )

        results.append({**item, "response": response["message"]["content"]})

    with open(output_file, "w", encoding="utf-8") as f:

        json.dump(results, f, ensure_ascii=False, indent=4)
