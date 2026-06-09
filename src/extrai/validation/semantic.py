import json
import re

ALLOWED_YES_NO = ["sí", "si", "no"]


ALLOWED_UNKNOWN = [
    "No informado",
    "No identificable",
    "no informado",
    "no identificable",
]


ALLOWED_VEHICLES = [
    "Automovil",
    "Automovil y Bicicleta",
    "Automovil y Motocicleta",
    "Automovil y Camion",
    "Automoviles",
    "Camioneta",
    "Camioneta y Automovil",
    "Camionetas y Automoviles",
    "Camioneta y Motocicleta",
    "Camionetas",
    "Camión",
    "Camión y Automovil",
    "Camión y Automoviles",
    "Camión y Motocicleta",
    "Camión y Camioneta",
    "Camión y Motocicleta",
    "Camión y Camioneta",
    "Camión, Camioneta y Automovil",
    "Camiones y Automovil",
    "Camiones y Camioneta",
    "Camiones",
    "Motocicleta",
    "Motocicleta y Bicicleta",
    "Motocicletas",
    "Colectivo",
    "Colectivo y Motocicleta",
    "Colectivo y automovil",
    "Colectivos",
    "Bicicleta",
    "Tractor",
    "Tractores",
    "Monopatín",
    "Motoniveladora y motocicleta",
    "No indentificable",
]


def is_valid_yes_no(value):

    if not isinstance(value, str):
        return False

    return value.lower() in ALLOWED_YES_NO


def is_valid_number(value):

    try:

        number = int(value)

        return number >= 0

    except:

        return False


def is_valid_hour(value):

    if value in ALLOWED_UNKNOWN:
        return True

    if not isinstance(value, str):
        return False

    return bool(re.match(r"^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$", value))


def is_valid_vehicle(value):

    if isinstance(value, str):

        value = [value]

    if not isinstance(value, list):
        return False

    return all(v in ALLOWED_VEHICLES for v in value)


def validate_record(record):

    errors = []

    # boolean fields
    for field in ["Nuevo siniestro vial", "Misiones"]:

        if field in record:

            if not is_valid_yes_no(record[field]):
                errors.append(f"{field}: invalid value")

    # numeric fields
    for field in ["Decesos", "Lesionados", "Hombres", "Mujeres"]:

        if field in record:

            if record[field] not in ALLOWED_UNKNOWN and not is_valid_number(
                record[field]
            ):
                errors.append(f"{field}: invalid number")

    if "Hora" in record:

        hours = record["Hora"]

        if isinstance(hours, list):

            for h in hours:

                if not is_valid_hour(h):
                    errors.append("Hora: invalid format")

        else:

            if not is_valid_hour(hours):
                errors.append("Hora: invalid format")

    if "Vehiculo" in record:

        if not is_valid_vehicle(record["Vehiculo"]):
            errors.append("Vehiculo: invalid value")

    return errors


def validate_semantic(input_file):

    total = 0
    valid = 0
    invalid = 0

    field_errors = {}

    with open(input_file, "r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            total += 1

            record = json.loads(line)

            errors = validate_record(record)

            if errors:

                invalid += 1

                for error in errors:

                    field = error.split(":")[0]

                    field_errors[field] = field_errors.get(field, 0) + 1

            else:

                valid += 1

    return {
        "total_records": total,
        "valid_records": valid,
        "invalid_records": invalid,
        "semantic_validity": round(valid / total * 100, 2),
        "field_errors": field_errors,
    }
