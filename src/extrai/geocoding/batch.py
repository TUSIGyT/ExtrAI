import json

import ollama

from extrai.geocoding.nominatim import query_nominatim, select_candidate
from extrai.batch import parse_llm_json

def normalize_location(location, city):

    response = ollama.chat(
        model="extrai-geocoder",
        messages=[
            {
                "role": "user",
                "content": f"""
                Ciudad: {city}
                Ubicación: {location}
                """,
            }
        ],
    )

    return response["message"]["content"]


def geocode_batch(input_file, output_file):

    with open(input_file, encoding="utf-8") as f:

        data = [json.loads(line) for line in f if line.strip()]

    with open(output_file, "w", encoding="utf-8") as out:

        for item in data:

            location = item.get("Ubicación")

            city = item.get("Ciudad")

            try:

                geo_query = normalize_location(
                    location,
                    city
                )
                print(geo_query)

                results = query_nominatim(geo_query, '')

                geo = select_candidate(results)

                item["geocoding"] = geo

            except Exception as e:

                item["geocoding"] = {"error": str(e)}

            out.write(json.dumps(item, ensure_ascii=False) + "\n")
