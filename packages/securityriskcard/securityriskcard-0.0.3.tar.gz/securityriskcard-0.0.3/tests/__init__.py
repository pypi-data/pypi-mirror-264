import json
from pathlib import Path


def load_test_data(variant: str):
    data_path = Path("tests/test_data")

    with open(data_path / f"{variant}.json", "r") as f:
        raw_data = json.load(f)

    with open(data_path / f"{variant}_risk.json", "r") as f:
        expected_result = json.load(f)

    return raw_data, expected_result
