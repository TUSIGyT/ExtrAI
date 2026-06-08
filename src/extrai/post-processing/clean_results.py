import argparse
import json

from extrai.utils import parse_llm_json


import argparse
import json
from pathlib import Path

from extrai.utils import parse_llm_json


def clean_results(input_file, output_file):

    total = 0
    recovered = 0
    discarded = 0

    output_path = Path(output_file)

    log_file = output_path.with_suffix(".txt")

    with (
        open(input_file, "r", encoding="utf-8") as f_in,
        open(output_file, "w", encoding="utf-8") as f_out,
    ):

        for line in f_in:

            total += 1

            item = json.loads(line)

            # Already valid
            if "error" not in item:

                f_out.write(json.dumps(item, ensure_ascii=False) + "\n")

                continue

            raw = item.get("raw_response", "")

            try:

                extracted = parse_llm_json(raw)

                cleaned = {
                    "model": item.get("model"),
                    "id": item.get("id"),
                    **extracted,
                }

                f_out.write(json.dumps(cleaned, ensure_ascii=False) + "\n")

                recovered += 1

            except Exception as e:

                discarded += 1

                print(f"Discarded {item.get('id')}: {e}")

    report = (
        f"Cleaning report\n"
        f"================\n"
        f"Input: {input_file}\n"
        f"Output: {output_file}\n\n"
        f"Total: {total}\n"
        f"Recovered: {recovered}\n"
        f"Discarded: {discarded}\n"
    )

    # print to terminal
    print()
    print(report)

    # save log
    with open(log_file, "w", encoding="utf-8") as f_log:

        f_log.write(report)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Clean LLM JSONL results")

    parser.add_argument("--input", required=True)

    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    clean_results(args.input, args.output)
