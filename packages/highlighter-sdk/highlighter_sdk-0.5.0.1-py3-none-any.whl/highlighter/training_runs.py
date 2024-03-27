from typing import List, Optional, Union, Dict
from datetime import datetime
from enum import Enum
from pathlib import Path
from pydantic import BaseModel, Field, validator
import tempfile
import yaml
import json

from highlighter.gql_client import HLClient
from highlighter.aws_s3 import upload_file_to_s3
from highlighter.const import DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE
from highlighter.io import download_bytes

__all__ = ["TrainingRunArtefactTypeEnum",
           "TrainingRunArtefactType",
           "TrainingRunType",
           "get_training_run_artefacts",
           "get_training_run_artefact",
           "get_latest_training_run_artefact",
           "get_capability_implementation_file_url",
           "create_training_run_artefact"]


def _get_now_str():
    return datetime.now().isoformat()


class TrainingRunArtefactTypeEnum(str, Enum):
    OnnxOpset11 = "OnnxOpset11"
    OnnxOpset14 = "OnnxOpset14"
    TorchScriptV1 = "TorchScriptV1"
    TensorFlowV1 = "TensorFlowV1"
    DeprecatedMmpond = "DeprecatedMmpond"
    DeprecatedClassilvier = "DeprecatedClassilvier"
    DeprecatedSilverclassify = "DeprecatedSilverclassify"
    OnnxRuntimeAmd64 = "OnnxRuntimeAmd64"
    OnnxRuntimeArm = "OnnxRuntimeArm"
    DeprecatedCapabilityImplementationFile = DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE


class TrainingRunArtefactType(BaseModel):
    id: Optional[str]
    checkpoint: Optional[str]
    fileUrl: str
    type: TrainingRunArtefactTypeEnum
    updatedAt: Optional[str] = Field(default_factory=_get_now_str)
    inferenceConfig: Dict = {} # Graphql expects at least an empty dict not None
    trainingConfig: Dict = {}  # Graphql expects at least an empty dict not None
    supportingFiles: Dict = {} # Graphql expects at least an empty dict not None

    @validator("inferenceConfig", "trainingConfig", "supportingFiles", pre=True)
    def none_to_empty_dict(cls, v):
        if v is None:
            return {}
        return v

    @validator("type", allow_reuse=True)
    def _val_type(cls, v):
        if v == DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE:
            return v
        else:
            return TrainingRunArtefactTypeEnum(v)

    class Config():
        use_enum_values = True

    @classmethod
    def from_yaml(cls, path: Union[Path, str]):
        path = Path(path)
        with path.open("r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def dump_yaml(self, path: Union[Path, str]):
        path = Path(path)
        with path.open("w") as f:
            yaml.dump(self.dict(), f)
    


class TrainingRunType(BaseModel):
    id: int
    name: str
    modelImplementationFileUrl: Optional[str]
    updatedAt: str
    trainingRunArtefacts: Optional[List[TrainingRunArtefactType]]

    # Convert enums to their values
    class Config:
        use_enum_values = True


def _download_training_run_artefact(
        training_run_artefact: TrainingRunArtefactType,
        file_url_save_path: Optional[str]=None,
        ):
    if file_url_save_path is None:
        file_url_save_path = f"{tempfile.mkdtemp()}/{training_run_artefact.id}"

    download_bytes(training_run_artefact.fileUrl,
                   Path(file_url_save_path))

    training_run_artefact.fileUrl = str(file_url_save_path)
    return training_run_artefact


def get_training_run_artefacts(
        hl_client: HLClient,
        training_run_id: int,
        filter_by_artefact_type: Optional[Union[str, TrainingRunArtefactTypeEnum]]=None,
    ) -> List[TrainingRunArtefactType]:
    """Return a list of artefacts for a training run
    sorted newest to oldest according to TrainingRunArtefactType.updatedAt

    If `filter_by_artefact_type` is set then will only retrun artefacts with
    matching TrainingRunArtefactType.type
    """

    training_run: TrainingRunType = hl_client.trainingRun(
        return_type=TrainingRunType,
        id=training_run_id,
    )

    if training_run.modelImplementationFileUrl is not None:
        # If TrainingRun.updatedAt is None then we set it to
        # datetime.min for the purposes of sorting.
        capability_implementation_file_artefact: TrainingRunArtefactType
        capability_implementation_file_artefact = TrainingRunArtefactType(
                id=None,
                checkpoint=None,
                fileUrl=training_run.modelImplementationFileUrl,
                type=TrainingRunArtefactTypeEnum.DeprecatedCapabilityImplementationFile,
                updatedAt=datetime.min.isoformat() if training_run.updatedAt else training_run.updatedAt,
                inferenceConfig=None,
                trainingConfig=None,
                supportingFiles=None,
                )
        training_run.trainingRunArtefacts.append(capability_implementation_file_artefact)

    if filter_by_artefact_type is not None:
        artefact_type = TrainingRunArtefactTypeEnum(filter_by_artefact_type)
        training_run.trainingRunArtefacts = [a for a in training_run.trainingRunArtefacts if a.type == artefact_type]

    return sorted(training_run.trainingRunArtefacts, key=lambda x: x.updatedAt,
                  reverse=True)

def get_training_run_artefact(
        hl_client: HLClient,
        training_run_artefact_id: str,
        download_file_url: bool=False,
        file_url_save_path: Optional[str]=None,
    ) -> TrainingRunArtefactType:
    """Get the TrainingRunArtefact object for a given training_run_artefact_id.

    If `download_file_url` is `True` then download either to a temporary
    directory or `file_url_save_path`. Once downloaded TrainingRunArtefact.fileUrl
    will be updated to the location where is has been downloaded to.
    """

    training_run_artefact: TrainingRunArtefactType
    training_run_artefact = hl_client.trainingRunArtefact(
            return_type=TrainingRunArtefactType,
            id=training_run_artefact_id)

    if download_file_url:
        training_run_artefact = _download_training_run_artefact(
                training_run_artefact,
                file_url_save_path=file_url_save_path)

    return training_run_artefact


def get_latest_training_run_artefact(
        hl_client: HLClient,
        training_run_id: int,
        download_file_url: bool=False,
        file_url_save_path: Optional[str]=None,
        filter_by_artefact_type: Optional[Union[str, TrainingRunArtefactTypeEnum]]=None,
    ) -> Optional[TrainingRunArtefactType]:
    """Get the TrainingRunArtefact with the most recent updatedAt value.

    If `download_file_url` is `True` then download either to a temporary
    directory or `file_url_save_path`. Once downloaded TrainingRunArtefact.fileUrl
    will be updated to the location where is has been downloaded to.
    """
    training_run_artefacts: List[TrainingRunArtefactType] = get_training_run_artefacts(
            hl_client,
            training_run_id,
            filter_by_artefact_type=filter_by_artefact_type)

    if len(training_run_artefacts) == 0:
        return None
    training_run_artefact: TrainingRunArtefactType = training_run_artefacts[0]

    if download_file_url:
        abs_file_url_save_path = str(Path(file_url_save_path).absolute())
        training_run_artefact = _download_training_run_artefact(
                training_run_artefact,
                file_url_save_path=abs_file_url_save_path)

    return training_run_artefact


def get_capability_implementation_file_url(
        hl_client: HLClient,
        training_run_id: int,
    ) -> str:

    result: TrainingRunType = hl_client.trainingRun(
        return_type=TrainingRunType,
        id=training_run_id,
    )
    return result.modelImplementationFileUrl


def create_training_run_artefact(
        hl_client: HLClient,
        training_run_id: int,
        artefact_path: str,
        training_run_artefact_type: TrainingRunArtefactTypeEnum,
        checkpoint_name: str,
        training_config: Union[Path, str, Dict],
        inference_config: Union[Path, str, Dict]
        ) -> TrainingRunArtefactType:
    if not isinstance(training_config, dict):
        training_config_path = Path(training_config_path)
        with training_config_path.open('r') as f:
            training_config = {
                training_config_path.name: f.read(),
            }

    if not isinstance(inference_config, dict):
        inference_config_path = Path(inference_config_path)
        with inference_config_path.open('r') as f:
            
            loaders = {".yaml": yaml.safe_load,
                       ".yml": yaml.safe_load,
                       ".json": json.load,
                       }

            inference_config = loaders[inference_config_path.suffix](f)

    artefact_file_data = upload_file_to_s3(
        hl_client,
        artefact_path,
    )
    print(f"Created file in s3:\n{artefact_file_data}")

    class CreateTrainingRunPayload(BaseModel):
        errors: List[str]
        trainingRunArtefact: Optional[TrainingRunArtefactType]


    result = hl_client.createTrainingRunArtefact(
        return_type=CreateTrainingRunPayload,
        trainingRunId=training_run_id,
        type=training_run_artefact_type,
        checkpoint=checkpoint_name,
        fileData=artefact_file_data,
        inferenceConfig=inference_config,
        trainingConfig=training_config,
    )
    if result.errors:
        raise ValueError(f"{result.errors}")

    return result.trainingRunArtefact
