# SecurityRiskCard

This package provides an simple shared way of converting security scorecard data from "wellness" into risk.

### Installing

To install from PyPi:
```bash
pip install securityriskcard
```

If you want to install directly from source, you can do that by adding the following into your `requirements.txt`:
```
git+https://github.com/morphysm/securityriskcard.git@main
```

### Usage example:
```python
from securityriskcard import convert_to_risk

# Your scorecard result goes here.
data = convert_to_risk(scorecard_data)
print(json.dumps(data, indent=4))
```
Or if you want to test if the package is installed and you have scorecard result as json file:
```bash
python -m securityriskcard <path/to/scorecard.json>
```

### Testing

Currently package contains some regression tests, which you can run during development or refactor to ensure data is output the same.
The directory with test data also includes a script to generate output to 'freeze' current state. Do not run it until you are confident that change behaves as expected.
