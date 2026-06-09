import json

EXPECTED_FIELDS = [
    "Nuevo siniestro vial",
    "Misiones",
    "Vehiculo",
    "Decesos",
    "Lesionados",
    "Hora",
    "Ubicación",
    "Ciudad",
    "Mujeres",
    "Hombres",
]


def validate_schema(input_file):

    total = 0
    complete = 0

    missing_counter = {field: 0 for field in EXPECTED_FIELDS}

    with open(input_file, "r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            total += 1

            record = json.loads(line)

            missing = [field for field in EXPECTED_FIELDS if field not in record]

            if not missing:
                complete += 1

            for field in missing:
                missing_counter[field] += 1

    completeness = complete / total * 100 if total > 0 else 0

    return {
        "total_records": total,
        "complete_records": complete,
        "incomplete_records": total - complete,
        "completeness": round(completeness, 2),
        "missing_fields": missing_counter,
    }
