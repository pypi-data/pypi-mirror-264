from dataclasses import dataclass
from typing import Optional, List


@dataclass
class ScenarioUploadData:
    """
    Represents data for uploading a scenario.

    Attributes:
        parent_id (int): The ID of the parent scenario folder.
        model_id (int): The ID of the model associated with the scenario.
        folder_name (Optional[str]): The name of the folder containing the scenario files.
        file (Optional[bytes]): The binary content of the scenario file.
    """

    parent_id: int
    model_id: int
    folder_name: Optional[str] = None
    file: Optional[bytes] = None

    def as_dict(self) -> dict:
        """Converts the data to a dictionary."""
        return {
            "parent_id": self.parent_id,
            "model_id": self.model_id,
            "folder_name": self.folder_name,
        }


@dataclass
class ScenarioData:
    """
    Represents data for a scenario.

    Attributes:
        id (int): The ID of the scenario.
        parent_id (int): The ID of the parent scenario folder.
        model_id (int): The ID of the model associated with the scenario.
        created (str): The creation timestamp of the scenario.
        path (str): The path of the scenario.
        children (Optional[List[str]]): The list of child scenario IDs.
    """

    id: int
    parent_id: int
    model_id: int
    created: str
    path: str
    children: Optional[List[str]] = None

    def get_data(self) -> dict:
        """Returns the scenario data as a dictionary."""
        return {
            "id": self.id,
            "parent_id": self.parent_id,
            "model_id": self.model_id,
            "created": self.created,
            "path": self.path,
            "children": self.children,
        }


# TODO Currently not in use
class RunList:
    def __init__(self, name, description, runtime_configuration, model_id):
        self.data = {
            "name": name,
            "description": description,
            "runtime_configuration": runtime_configuration,
            "model_id": model_id,
        }

    def get_data(self):
        return self.data

# TODO Currently not in use
class Policy:
    def __init__(self, name, description, model_id):
        self.data = {
            "name": name,
            "description": description,
            "model_id": model_id,
        }

    def get_data(self):
        return self.data

# TODO Currently not in use
class ModelData:
    def __init__(
        self,
        name,
        description,
        output_bucket,
        job_queue,
        job_definition,
        compute_environment,
        ecr_registry,
    ):
        self.data = {
            "name": name,
            "description": description,
            "output_bucket": output_bucket,
            "job_queue": job_queue,
            "job_definition": job_definition,
            "compute_environment": compute_environment,
            "ecr_registry": ecr_registry,
        }

    def get_data(self):
        return self.data
