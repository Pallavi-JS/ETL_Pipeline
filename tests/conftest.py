

import pytest


@pytest.fixture
def sample_raw_records() -> list[dict]:
    """A small, realistic sample of raw API records (JSONPlaceholder shape)."""
    return [
        {
            "id": 1,
            "name": "Leanne Graham",
            "username": "Bret",
            "email": "Sincere@april.biz",
            "address": {"city": "Gwenborough"},
            "company": {"name": "Romaguera-Crona"},
        },
        {
            "id": 2,
            "name": "Ervin Howell",
            "username": "Antonette",
            "email": "Shanna@melissa.tv",
            "address": {"city": "Wisokyburgh"},
            "company": {"name": "Deckow-Crist"},
        },
        {
            # Duplicate id -> should be dropped by transform
            "id": 2,
            "name": "Ervin Howell",
            "username": "Antonette",
            "email": "Shanna@melissa.tv",
            "address": {"city": "Wisokyburgh"},
            "company": {"name": "Deckow-Crist"},
        },
        {
            # Missing email -> should be dropped by transform
            "id": 3,
            "name": "No Email User",
            "username": "noemail",
            "email": None,
            "address": {"city": "Nowhere"},
            "company": {"name": "Ghost Inc"},
        },
    ]
