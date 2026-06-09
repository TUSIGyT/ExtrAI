import json


def validate_structure(input_file):

    total = 0
    valid = 0
    invalid = 0

    with open(input_file, "r", encoding="utf-8") as f:

        for line_number, line in enumerate(f, start=1):

            if not line.strip():
                continue

            total += 1

            try:

                json.loads(line)

                valid += 1

            except json.JSONDecodeError:

                invalid += 1

    success_rate = valid / total * 100 if total > 0 else 0

    return {
        "total": total,
        "valid": valid,
        "invalid": invalid,
        "success_rate": round(success_rate, 2),
    }
