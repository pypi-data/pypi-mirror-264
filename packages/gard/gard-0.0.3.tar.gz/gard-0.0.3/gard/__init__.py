import json
from importlib.resources import files


class GARD:
  def __init__(self) -> None:
    self.map = {}

    with open(files('gard').joinpath('diseases.trimmed.json')) as f:
        diseases = json.load(f)
        for disease in diseases:
            self.map[disease['id']] = {
                'name': disease['name'],
                'encodedName': disease['encodedName']
            }

  def __call__(self, gard_id: int | str) -> dict:
    return self.map.get(int(gard_id))

  def __getitem__(self, gard_id: int | str) -> dict:
    return self.map[int(gard_id)]

  def get_url(self, gard_id: int | str) -> str:
    gard_id = int(gard_id)
    encoded_name = self[gard_id]['encodedName']
    return f'https://rarediseases.info.nih.gov/diseases/{gard_id}/{encoded_name}'
