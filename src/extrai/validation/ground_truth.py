import json


def load_ground_truth(file):

    truth = {}

    with open(file, "r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            item = json.loads(line)

            truth[item["id"]] = item["expected"]

    return truth


def normalize_list(value):

    if value is None:
        return []

    if isinstance(value, list):
        return sorted(value)

    return [value]


def compare_field(prediction, expected):

    # list fields
    if isinstance(expected, list):

        return normalize_list(prediction) == normalize_list(expected)

    # numeric fields
    if isinstance(expected, int):

        try:
            return int(prediction) == expected

        except:

            return False

    # text fields

    if isinstance(prediction, str):

        return prediction.lower() == expected.lower()

    return prediction == expected


def evaluate_ground_truth(prediction_file, truth_file):

    truth = load_ground_truth(truth_file)

    total = 0

    correct_fields = 0
    total_fields = 0

    field_scores = {}

    with open(prediction_file, "r", encoding="utf-8") as f:

        for line in f:

            if not line.strip():
                continue

            pred = json.loads(line)

            item_id = pred.get("id")

            if item_id not in truth:
                continue

            expected = truth[item_id]

            total += 1

            for field, expected_value in expected.items():

                if field not in pred:
                    continue

                total_fields += 1

                ok = compare_field(pred[field], expected_value)

                if ok:
                    correct_fields += 1

                if field not in field_scores:

                    field_scores[field] = {"correct": 0, "total": 0}

                field_scores[field]["total"] += 1

                if ok:
                    field_scores[field]["correct"] += 1

    accuracy = correct_fields / total_fields * 100 if total_fields else 0

    for field in field_scores:

        data = field_scores[field]

        data["accuracy"] = round(data["correct"] / data["total"] * 100, 2)

    return {
        "evaluated_records": total,
        "field_accuracy": round(accuracy, 2),
        "fields": field_scores,
    }
