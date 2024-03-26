# gard

A simple offline Python wrapper to map Genetic and Rare Diseases Information Center (GARD) IDs to disease names / URLs.

## Installation

```bash
pip install gard
```

## Usage

```python
from gard import GARD

gard = GARD()
print(grad(1))
# {'encodedName': 'gracile-syndrome', 'name': 'GRACILE syndrome'}

print(grad.get_url(1))
# https://rarediseases.info.nih.gov/diseases/1/gracile-syndrome
```
