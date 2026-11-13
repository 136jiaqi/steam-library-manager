import pytest

from services.steam_api import validate_steam_id64


def test_accepts_steam_id64():
    assert validate_steam_id64("76561197960287930") == "76561197960287930"


@pytest.mark.parametrize("value", ["", "123", "ABCDEFG", "7656119796028793x", "12345678901234567"])
def test_rejects_invalid_steam_id64(value):
    with pytest.raises(ValueError):
        validate_steam_id64(value)
