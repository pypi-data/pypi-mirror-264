import pytest

from gard import GARD


def test_call():
    gard = GARD()
    assert gard(1) == {'encodedName': 'gracile-syndrome', 'name': 'GRACILE syndrome'}
    assert gard("0000001") == {'encodedName': 'gracile-syndrome', 'name': 'GRACILE syndrome'}

def test_getitem():
    gard = GARD()
    assert gard[1] == {'encodedName': 'gracile-syndrome', 'name': 'GRACILE syndrome'}
    assert gard["0000001"] == {'encodedName': 'gracile-syndrome', 'name': 'GRACILE syndrome'}

def test_call_nonexistent():
    gard = GARD()
    assert gard(0) == None

def test_getitem_nonexistent():
    gard = GARD()
    with pytest.raises(KeyError):
        gard[0]

def test_get_url():
    gard = GARD()
    assert gard.get_url(1) == 'https://rarediseases.info.nih.gov/diseases/1/gracile-syndrome'
    assert gard.get_url("0000001") == 'https://rarediseases.info.nih.gov/diseases/1/gracile-syndrome'
