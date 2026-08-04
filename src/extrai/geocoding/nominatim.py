import requests
from urllib.parse import quote

NOMINATIM_URL = "https://nominatim.misiones.gob.ar/search"


def query_nominatim(location, city):

    query = f"{location}, " f"{city}, " "Misiones"

    params = {"q": query, "format": "json", "limit": 5}

    response = requests.get(NOMINATIM_URL, params=params, timeout=10)

    response.raise_for_status()

    return response.json()


def select_candidate(results):

    if not results:
        return None

    # prefer administrative places
    preferred = [
        r
        for r in results
        if r.get("addresstype") in ["road", "place", "city", "suburb"]
    ]

    if preferred:
        result = preferred[0]

    else:
        result = results[0]

    return {
        "lat": float(result["lat"]),
        "lon": float(result["lon"]),
        "display_name": result.get("display_name"),
        "osm_type": result.get("osm_type"),
        "osm_id": result.get("osm_id"),
    }
