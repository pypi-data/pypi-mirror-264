import pytest
from unittest.mock import MagicMock, patch
from PWBM_Cloud_Utils import CloudMain


@pytest.fixture
def cloud_main():
    scenario_id = 39
    return CloudMain(scenario_id, "")


def test_get_model_id(cloud_main):
    # Mocking ScenarioAPI.get_scenario_by_id method
    expected_model_id = 46
    scenario_data_mock = MagicMock()
    scenario_data_mock.model_id = expected_model_id
    assert cloud_main.get_model_id() == expected_model_id


# TODO more tests

