import pytest
from pydantic import ValidationError
from py_gamma_sdk.models import Market

def test_market_model_validation():
    # Valid data
    valid_data = {
        "id": "1",
        "question": "Q",
        "conditionId": "0x1",
        "slug": "slug",
        "outcomes": ["A", "B"],
        "clobTokenIds": ["T1", "T2"]
    }
    market = Market(**valid_data)
    assert market.id == "1"

def test_market_model_invalid():
    # Missing required field
    invalid_data = {
        "id": "1",
        "question": "Q"
    }
    with pytest.raises(ValidationError):
        Market(**invalid_data)
