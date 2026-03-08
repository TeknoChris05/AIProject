import json
import os


def load_incident_data(input_path: str):
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"Input file not found: {input_path}")

    with open(input_path, "r") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError("Incident data must be a list")

    return data
