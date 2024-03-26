"""
The API classes are introduced for two reasons:
    (a) Protect the rest of the code from changes to the API, especially during rapid development. 
    This is not fool-proof, because the current implementations are very thin, yet it can still be
    quite useful.
    (b) Facilitate testing by allowing the actual APIClient objects to be replaced with stand-ins.
"""

import requests
from .entities import ScenarioData, ScenarioUploadData


class APIClient:
    """
    A base class for making requests to an API.

    Attributes:
        base_url: The base URL of the API.
    """

    def __init__(self, base_url: str = "https://wits.pwbm-api.net"):
        """
        Initializes the APIClient with a base URL.

        Args:
            base_url (str, optional): The base URL of the API. Defaults to "https://wits.pwbm-api.net".
        """
        self.base_url = base_url

    def _make_request(self, method: str, endpoint: str, data=None, files=None) -> dict:
        """
        Makes a request to the API endpoint.

        Args:
            method (str): The HTTP method (e.g., 'GET', 'POST', 'PUT', 'DELETE').
            endpoint (str): The endpoint of the API.
            data (dict, optional): The data to be sent with the request. Defaults to None.
            files (dict, optional): The files to be sent with the request. Defaults to None.

        Returns:
            dict: The JSON response from the API.
        """
        url = f"{self.base_url}/{endpoint}"
        # The optional parameters are handled by the requests package, whose default values
        # are None in the package. See Session.request() for more information.
        response = requests.request(method, url, json=data, files=files)
        return response.json()


class ScenarioAPI(APIClient):

    def get_scenario_by_id(self, scenario_id: int) -> ScenarioData:
        """
        Retrieve a scenario by its ID.

        Args:
            scenario_id (int): The ID of the scenario.

        Returns:
            ScenarioData: An instance of ScenarioData containing the retrieved scenario details.
        """
        endpoint = f"scenario/{scenario_id}"
        response_data = self._make_request("GET", endpoint)
        return ScenarioData(**response_data)

    def create_scenario(self, scenario_data: ScenarioUploadData) -> ScenarioData:
        """
        Create a scenario using the provided scenario_data.

        Args:
            scenario_data (ScenarioData): An instance of ScenarioData containing the data for the new scenario.

        Returns:
            ScenarioData: An instance of ScenarioData containing the created scenario details.
        """
        endpoint = "scenario/"
        params = scenario_data.as_dict()
        files = {"file": scenario_data.file} if scenario_data.file else None
        response_data = self._make_request("PUT", endpoint, data=params, files=files)
        return ScenarioData(**response_data)


# TODO Currently not in use
class RunListAPI(APIClient):
    def get_run_list(self, run_list_id):
        return self._make_request("GET", f"run_list/{run_list_id}")

    def get_run_list_output_path(self, run_list_id, policy_id):
        return self._make_request(
            "GET",
            f"run_list/run_list_output_path?run_id={run_list_id}&policy_id={policy_id}",
        )

    def delete_run_list(self, run_list_id):
        return self._make_request("DELETE", f"run_list/{run_list_id}")

    def get_run_lists_by_model(self, model_id):
        return self._make_request("GET", f"run_list/model/{model_id}")

    def upload_run_list(self, model_id, run_list_data):
        return self._make_request(
            "POST", f"run_list/upload/{model_id}", data=run_list_data
        )

    def put_run_list(self, run_list_data):
        return self._make_request("PUT", "run_list", data=run_list_data)

    def create_run_list(self, run_list_data):
        return self._make_request("POST", "run_list", data=run_list_data)

    def execute_run_list(self, run_list_id):
        return self._make_request("POST", f"run_list/execute/{run_list_id}")

    def get_batch_job_status(self, run_list_id):
        return self._make_request("GET", f"run_list/job_status/{run_list_id}")

    def get_run_list_output(self, run_list_id):
        return self._make_request("GET", f"run_list/output/{run_list_id}")


# TODO Currently not in use
class PolicyAPI(APIClient):
    def get_all_policies(self, model_id):
        return self._make_request("GET", f"policy/get_all/{model_id}")

    def get_policy(self, policy_id):
        return self._make_request("GET", f"policy/{policy_id}")

    def delete_policy(self, policy_id):
        return self._make_request("DELETE", f"policy/{policy_id}")

    def update_policy(self, policy_data):
        return self._make_request("PUT", "policy", data=policy_data)

    def add_policy(self, policy_data):
        return self._make_request("POST", "policy", data=policy_data)


# TODO Currently not in use
class PolicyFilesAPI(APIClient):
    def upload_files(self, policy_id, files):
        endpoint = f"policy_files/upload/{policy_id}"
        data = {"files": files}
        return self._make_request("POST", endpoint, data)

    def create_files(self, policy_id, files):
        endpoint = f"policy_files/{policy_id}"
        data = {"files": files}
        return self._make_request("POST", endpoint, data)

    def get_all_files_by_policy(self, policy_id):
        endpoint = f"policy_files/all_files_by_policy/{policy_id}"
        return self._make_request("GET", endpoint)

    def delete_all_files_by_policy(self, policy_id):
        endpoint = f"policy_files/all_files_by_policy/{policy_id}"
        return self._make_request("DELETE", endpoint)

    def get_file(self, file_id):
        endpoint = f"policy_files/{file_id}"
        return self._make_request("GET", endpoint)

    def delete_file(self, file_id):
        endpoint = f"policy_files/{file_id}"
        return self._make_request("DELETE", endpoint)

    def delete_policy_file_link(self, policy_id, file_id):
        endpoint = "policy_files/policy_file_link"
        data = {"policy_id": policy_id, "file_id": file_id}
        return self._make_request("DELETE", endpoint, data)

    def update_file(self, file_id, file_data):
        endpoint = f"policy_files/file/{file_id}"
        return self._make_request("PUT", endpoint, data=file_data)

    def object_update_file(self, file_data):
        endpoint = "policy_files"
        return self._make_request("PUT", endpoint, data=file_data)


# TODO Currently not in use
class ModelsAPI(APIClient):

    def get_model(self, id: int):
        return self._make_request("GET", "models/get/" + str(id))

    def get_all_models(self):
        return self._make_request("GET", "models/get_all")

    def create_model(self, model_data):
        return self._make_request("POST", "models", data=model_data)

    def delete_model(self, model_id):
        return self._make_request("DELETE", f"models/{model_id}")
