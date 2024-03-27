"""
TODO remove this as it's now duplicated in sdk/python/training_config.py
"""

import json
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import yaml
from pydantic import BaseModel, Extra, Field, confloat, validator

from highlighter import HLClient

__all__ = [
    "get_training_config",
    "MetricType",
    "EntityAttributeValueTypeEnum",
    "EntityAttributeValue",
    "EntityAttribute",
    "ModelOutputType",
    "ModelInputs",
    "ModelSchemaType",
    "DatasetType",
    "ArtefactInfo",
    "TrainingConfigType",
    "TrainingRunArtefactTypeEnum",
]


def validate_uuid(v, key):
    validated = None
    if isinstance(v, UUID):
        validated = str(v)
    else:
        try:
            UUID(v)
            validated = v
        except:
            msg = f"'{key}' must be valid UUID, got: {v}"
            raise ValueError(msg)
    return validated


class MetricType(BaseModel, extra=Extra.forbid):
    researchPlanId: int
    experimentId: int
    researchPlanMetricId: int
    result: float
    objectClassUuid: Optional[str] = None

    # iso datetime str will be generated at instantiation
    # if not supplied manually.
    occuredAt: str = Field(default_factory=datetime.now().isoformat())

    @validator("occuredAt")
    def validate_is_iso_time_str(cls, v):
        assert datetime.fromisoformat(v)
        return v

    @validator("objectClassUuid")
    def validate_is_uuid(cls, v):
        return str(validate_uuid(v, "objectClassUuid"))

    @classmethod
    def from_yaml(cls, path: Union[Path, str]):
        path = Path(path)
        with path.open("r") as f:
            data = yaml.safe_load(f)
        return cls(**data)


class EntityAttributeValueTypeEnum(str, Enum):
    boolean = "boolean"
    enum = "enum"
    integer = "integer"
    decimal = "decimal"
    string = "string"
    geometry = "geometry"
    array = "array"


class ModelOutputType(BaseModel, extra=Extra.forbid):
    head: int
    position: int
    conf_thresh: confloat(ge=0.0, lt=1.0)
    entity_attribute_enum_id: Optional[Union[UUID, str]]
    entity_attribute_enum_value: Optional[str]
    entity_attribute_id: Union[UUID, str]
    entity_attribute_name: str
    entity_attribute_value_type: Optional[EntityAttributeValueTypeEnum]

    @validator("entity_attribute_enum_id")
    def validate_entity_attribute_enum_id(cls, v):
        if v is None:
            return True
        else:
            return str(validate_uuid(v, "entity_attribute_enum_id"))

    @validator("entity_attribute_id")
    def validate_entity_attribute_id(cls, v):
        return str(validate_uuid(v, "entity_attribute_id"))

    @property
    def value_type(self):
        return self.entity_attribute_value_type


class EntityAttribute(BaseModel, extra=Extra.forbid):

    entity_attribute_id: Union[UUID, str]
    entity_attribute_name: str

    @validator("entity_attribute_id")
    def validate_entity_attribute_id(cls, v):
        return str(validate_uuid(v, "entity_attribute_id"))


class EntityAttributeValue(BaseModel, extra=Extra.forbid):
    entity_attribute_enum_id: Optional[Union[UUID, str]]
    entity_attribute_enum_value: Optional[str]
    entity_attribute_id: Union[UUID, str]
    entity_attribute_name: str
    entity_attribute_value_type: EntityAttributeValueTypeEnum
    entity_attribute_value: Any

    @validator("entity_attribute_enum_id")
    def validate_entity_attribute_enum_id(cls, v):
        if v is None:
            return v
        return str(validate_uuid(v, "entity_attribute_enum_id"))

    @validator("entity_attribute_id")
    def validate_entity_attribute_id(cls, v):
        return str(validate_uuid(v, "entity_attribute_id"))

    @property
    def value_type(self):
        return self.entity_attribute_value_type

    @property
    def value(self):
        if self.value_type == EntityAttributeValueTypeEnum.enum:
            return self.entity_attribute_enum_id
        else:
            return self.entity_attribute_value


class ModelInputs(BaseModel, extra=Extra.forbid):
    entity_attributes: List[EntityAttribute]
    filters: List[List[EntityAttributeValue]]


class ModelSchemaType(BaseModel, extra=Extra.forbid):
    model_inputs: ModelInputs
    model_outputs: List[ModelOutputType]

    @validator("model_outputs")
    def validate_model_output_positions(cls, model_outputs):
        if len(model_outputs) == 0:
            #####################################################################
            # ❗❗❗ Remove when all inference capabilities are using TrainingConfig
            # as oposed schema's tied up in ManifestV1
            #####################################################################
            return model_outputs

        model_outputs = sorted(model_outputs, key=lambda o: (o.head, o.position))
        if (model_outputs[0].position != 0) and (model_outputs[0].head != 0):
            raise ValueError("model_outputs ids must start at 0")

        num_heads = len(set([o.head for o in model_outputs]))
        for head_idx in range(num_heads):
            for pos_idx, o in enumerate(
                [_o for _o in model_outputs if _o.head == head_idx]
            ):
                if head_idx != o.head:
                    raise ValueError(
                        "model_output.head values must start at 0 and be contigious"
                    )
                if pos_idx != o.position:
                    raise ValueError(
                        "model_output.position values must start at 0 and be contigious"
                    )

        return model_outputs

    def get_input_select_attribute_ids(self) -> List[str]:
        return [
            str(i.entity_attribute_id)
            for i in self.model_inputs.entity_attributes
        ]

    def get_input_filter_attribute_ids(self) -> List[str]:
        filter_attr_ids = []
        for input_filter in self.model_inputs.filters:
            filter_attr_ids.append([str(i.entity_attribute_id) for i in input_filter])
        return filter_attr_ids

    def get_input_filter_attribute_values(self) -> List[Any]:
        filter_values = []
        for input_filter in self.model_inputs.filters:
            filter_values.append([i.value for i in input_filter])

        filter_values = [v if len(v) > 0 else None for v in filter_values]
        return filter_values

    def get_head_model_outputs(self, head: int):
        model_outputs = [m for m in self.model_outputs if m.head == head]
        return model_outputs

    def get_head_output_attribute_ids(self, head: int) -> List[str]:
        head_model_outputs = self.get_head_model_outputs(head)
        return [str(m.entity_attribute_id) for m in head_model_outputs]

    def get_head_output_attribute_enum_ids(self, head: int) -> List[str]:
        head_model_outputs = self.get_head_model_outputs(head)
        return [str(m.entity_attribute_enum_id) for m in head_model_outputs]

    def get_head_output_attribute_enum_values(self, head: int) -> List[str]:
        head_model_outputs = self.get_head_model_outputs(head)
        return [str(m.entity_attribute_enum_value) for m in head_model_outputs]

    def get_head_output_value_type(
        self, head: int
    ) -> Optional[EntityAttributeValueTypeEnum]:
        """Will return None if the entity_attribute_value_type is also None
        because it is an Optional parameter of ModelOutputType
        """
        head_model_outputs = self.get_head_model_outputs(head)
        head_output_value_types = {
            m.entity_attribute_value_type for m in head_model_outputs
        }
        assert len(head_output_value_types) == 1
        return head_output_value_types.pop()


class DatasetType(BaseModel, extra=Extra.forbid):
    id: int
    hash_signature: str


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


class ArtefactInfo(BaseModel):
    """camelCase dict keys are intended as these args will be passed to a graphql mutation"""

    type: TrainingRunArtefactTypeEnum
    trainingRunId: int
    artefactPath: str
    checkpoint: str
    inferenceConfig: Dict
    trainingConfig: Dict

    def to_dict(self) -> dict:
        returnDict = self.dict()
        returnDict["type"] = str(self.type.name)
        return returnDict


class TrainingConfigType(BaseModel, extra=Extra.forbid):
    base_conf: Optional[str]
    config_overrides: Dict
    data: Dict[str, List[DatasetType]]
    model_arguments: Dict
    model_config: Dict
    model_schema: ModelSchemaType
    training_run_id: int
    research_plan_id: Optional[int]
    experiment_id: Optional[int]

    def get_dataset_ids(self, purpose: str):
        purposes = ["train", "test", "dev"]
        if purpose not in purposes:
            raise KeyError(
                f"Invalid dataset purpose, expected one of {purposes} "
                f"got: {purpose}"
            )

        return [d.id for d in self.data.get(f"datasets_{purpose}", [])]

    def get_dataset_purpose_id_lookup(self) -> Dict[str, List[int]]:
        purposes = ["train", "test", "dev"]
        return {p: self.get_dataset_ids(p) for p in purposes}

    @classmethod
    def from_yaml(cls, yaml_path: Path):
        with yaml_path.open("r") as f:
            data = yaml.safe_load(f)
        return cls(**data)

    def dump(self, fmt: str, path: Union[str, Path]):
        path = Path(path)
        dumpers = {
            "yaml": self._dump_yaml,
            "json": self._dump_json,
        }
        dumper = dumpers[fmt]
        dumper(path)

    def _dump_yaml(self, path: Path):
        with path.open("w") as f:
            yaml.safe_dump(self.dict(), f)

    def _dump_json(self, path: Path):
        with path.open("w") as f:
            json.dump(self.dict(), f, indent=2)

def get_training_config(
    client: HLClient,
    training_run_id: int,
) -> TrainingConfigType:

    class TrainingRunType(BaseModel, extra=Extra.forbid):
        trainingConfig: dict

    result = client.trainingRun(
        return_type=TrainingRunType,
        id=training_run_id,
    )
    return TrainingConfigType(**result.trainingConfig)
