import re


def read_cleaning_report(report_file):

    with open(report_file, "r", encoding="utf-8") as f:

        text = f.read()

    def extract(name):

        match = re.search(rf"{name}: (\d+)", text)

        return int(match.group(1)) if match else None

    total = extract("Total")
    recovered = extract("Recovered")
    discarded = extract("Discarded")

    success_rate = (total - discarded) / total * 100 if total else 0

    return {
        "total": total,
        "recovered": recovered,
        "discarded": discarded,
        "success_rate": round(success_rate, 2),
    }


import argparse
import json
from pathlib import Path

from extrai.validation.schema import validate_schema
from extrai.validation.semantic import validate_semantic
from extrai.validation.ground_truth import evaluate_ground_truth


def load_cleaning_report(file):

    data = {}

    with open(file, "r", encoding="utf-8") as f:

        for line in f:

            if ":" not in line:
                continue

            key, value = line.split(":", 1)

            key = key.strip()
            value = value.strip()

            try:
                data[key] = int(value)
            except:
                data[key] = value

    if "Total" in data and "Discarded" in data:

        data["Success rate"] = round(
            (data["Total"] - data["Discarded"]) / data["Total"] * 100, 2
        )

    return data


def generate_validation_report(
    input_file, cleaning_file, output_file, ground_truth=None
):

    report = {}

    # 1. Structural
    report["structural"] = load_cleaning_report(cleaning_file)

    # 2. Schema
    report["schema"] = validate_schema(input_file)

    # 3. Semantic
    report["semantic"] = validate_semantic(input_file)

    # 4. Ground truth
    if ground_truth:

        report["ground_truth"] = evaluate_ground_truth(input_file, ground_truth)

    # Save JSON report
    json_file = Path(output_file).with_suffix(".json")

    with open(json_file, "w", encoding="utf-8") as f:

        json.dump(report, f, ensure_ascii=False, indent=4)

    # Save TXT report

    with open(output_file, "w", encoding="utf-8") as f:

        f.write("ExtrAI Validation Report\n" "========================\n\n")

        for section, values in report.items():

            f.write(f"\n{section.upper()}\n")

            f.write("-" * 40 + "\n")

            f.write(json.dumps(values, ensure_ascii=False, indent=4))

            f.write("\n")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Generate full validation report")

    parser.add_argument("--input", required=True)

    parser.add_argument("--cleaning-report", required=True)

    parser.add_argument("--output", required=True)

    parser.add_argument("--ground-truth", default=None)

    args = parser.parse_args()

    generate_validation_report(
        args.input, args.cleaning_report, args.output, args.ground_truth
    )
