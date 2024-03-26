import os
import zipfile
from .api_functions import ScenarioAPI, ScenarioData
import boto3


class CloudMain:
    _scenario_id: int
    scenario_data: ScenarioData
    model_id: int
    S3_file_path: str
    S3_bucket_name: str
    local_config_path: str
    
    def __init__(self, scenario_id: int, local_config_path: str, local_config_basepath: str | None = None) -> None:
        """
        Constructor for CloudMain, which takes in a scenario ID. CloudMain allows you to download config files from S3.

        Attributes:
            scenario_id: the scenario id used to get scenario data.
            local_config_path: relative path/folder location to put the config files, which will be added to local config basepath to create the absolute path
            local_config_basepath: the base path to put the config files, if None, initialize it with current working directory in the constructor
        """
        self._scenario_id = scenario_id
        self.scenario_data = ScenarioAPI().get_scenario_by_id(self._scenario_id)
        self.model_id = self.scenario_data.model_id
        self.S3_file_path = self.scenario_data.path
        self.S3_bucket_name = "model-inputs.pwbm-data"
        if not local_config_basepath:
            local_config_basepath = os.getcwd()
        self.local_config_abs_path = os.path.join(local_config_basepath, local_config_path)
        self._load_parameter_zip()

    def _load_parameter_zip(self) -> None:
        """
        Private method to load parameters from a zipped file.
        """
        try:
            boto3.client("s3").download_file(
                self.S3_bucket_name, self.S3_file_path, "downloaded_file.zip"
            )
            print(
                f"File downloaded from S3 bucket '{self.S3_bucket_name}' / '{self.S3_file_path}'"
            )
        except Exception as e:
            print(f"Error downloading file from S3: {e}")
            
        try:
            with zipfile.ZipFile("downloaded_file.zip", "r") as zip_ref:
                print(self.local_config_abs_path)
                zip_ref.extractall(self.local_config_abs_path)
            os.remove("downloaded_file.zip")
        except Exception as e:
            print(f"Error unzipping file from S3: {e}")


    def get_model_id(self) -> int:
        """
        Retrieve model ID associated with the scenario ID.
        """
        return self.model_id

    def get_file_path(self) -> str:
        """
        Retrieve S3 file path associated with the scenario ID.
        """
        return self.S3_file_path


# #Example usage:
# scenario_id = 39
# CloudMain(scenario_id, "src/tests/data")

