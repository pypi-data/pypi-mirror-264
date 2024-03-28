import json
import sys

from . import convert_to_risk

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m securityriskcard <path/to/scorecard.json>")

    with open(sys.argv[1]) as f:
        input_data = json.load(f)

    data = convert_to_risk(input_data)
    print(json.dumps(data, indent=4))
