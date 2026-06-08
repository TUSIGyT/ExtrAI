import json
import re

from json_repair import repair_json


def parse_llm_json(content):
    """
    Extract JSON from an LLM response.

    Handles:
    - ```json ... ```
    - ```python ... ```
    - extra text before/after JSON
    - minor malformed JSON using json-repair
    """

    if not content:
        raise ValueError("Empty LLM response")

    content = content.strip()

    # Remove markdown code fences
    content = re.sub(r"```[a-zA-Z0-9_-]*", "", content)

    content = content.replace("```", "").strip()

    # Extract JSON object
    start = content.find("{")
    end = content.rfind("}")

    if start == -1:
        raise ValueError("No JSON object found")

    # If the model truncated the response,
    # keep everything after the first {
    json_text = content[start:]

    if end != -1:
        json_text = content[start : end + 1]

    try:
        return json.loads(json_text)

    except json.JSONDecodeError:

        # Try repairing malformed JSON
        repaired = repair_json(json_text)

        return json.loads(repaired)
