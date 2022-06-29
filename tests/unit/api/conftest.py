import uuid

import pytest
from pytest_mock import MockerFixture

from .constants import VALID_USER_ID


@pytest.fixture
def valid_user_id(mocker: MockerFixture) -> uuid.UUID:
    user_id = mocker.patch("ugc.api.v1.handlers.ugc.get_user_id_from_jwt", return_value=uuid.UUID(VALID_USER_ID))
    yield user_id
