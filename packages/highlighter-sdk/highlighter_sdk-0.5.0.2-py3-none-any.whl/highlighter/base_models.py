from datetime import datetime
from enum import Enum
from pathlib import Path
from highlighter.const import DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE
from typing import Any, Dict, List, Optional, Union
from uuid import UUID, uuid4
from warnings import warn

import yaml
from pydantic import BaseModel, Field, validator

UUID_STR = Union[str, UUID]


def _get_uuid_str():
    return str(uuid4())


def _get_now_str():
    return datetime.now().isoformat()


def _validate_uuid(v):
    if isinstance(v, UUID):
        return str(v)

    if v is None:
        warn("entityId was not provided, generating one")
        return _get_uuid_str()

    try:
        _ = UUID(v)
        return v
    except:
        raise ValueError(f"Invalid UUID string")


class PageInfo(BaseModel):
    hasNextPage: bool
    endCursor: Optional[str]


class ObjectClass(BaseModel):
    id: str
    uuid: str
    name: str


class ObjectClassTypeConnection(BaseModel):
    pageInfo: PageInfo
    nodes: List[ObjectClass]


# Because fileUrlOriginal contains
# a presigned url that is generated upon request
# it is not included by default.
# If you need fileUrlOriginal create a new ImageType
# BaseModel where it is being used.


class ImageType(BaseModel):
    id: str
    width: Optional[int]
    height: Optional[int]
    originalSourceUrl: str
    mimeType: str


class ImagePresignedType(ImageType):
    fileUrlOriginal: str


class ImageTypeConnection(BaseModel):
    pageInfo: PageInfo
    nodes: List[ImageType]


class EntityAttributeType(BaseModel):
    id: str
    name: str


class EntityAttributeEnumType(BaseModel):
    id: str
    value: str


class DatumSource(BaseModel):
    confidence: float


class EntityAttributeValueType(BaseModel):
    relatedEntityId: Optional[str]
    fileUuid: Optional[str]
    entityAttribute: EntityAttributeType
    entityAttributeId: str
    entityAttributeEnum: Optional[EntityAttributeEnumType]
    value: Optional[Any]
    entityId: Optional[str] = Field(default_factory=_get_uuid_str)
    entityDatumSource: Optional[DatumSource]
    occurredAt: str

    @validator("entityId", allow_reuse=True)
    def is_valid_uuid(cls, v):
        return _validate_uuid(v)


class AnnotationType(BaseModel):
    # location and confidence are guarantee to exist on AnnotationType
    location: str
    confidence: float = 1.0
    agentName: str
    dataType: str
    userId: int
    correlationId: str
    isInference: bool
    objectClass: ObjectClass
    frameId: Optional[int] = 0
    entityId: Optional[str] = Field(default_factory=_get_uuid_str)

    @validator("entityId", allow_reuse=True)
    def is_valid_uuid(cls, v):
        return _validate_uuid(v)


class UserType(BaseModel):
    id: int
    displayName: str
    email: str


class SubmissionType(BaseModel):
    id: int
    imageId: int
    annotations: List[AnnotationType]
    entityAttributeValues: List[EntityAttributeValueType]
    createdAt: str
    image: ImageType
    hashSignature: Optional[str]
    user: UserType
    backgroundInfoLayerFileData: Optional[Dict[str, Any]]
    backgroundInfoLayerFileCacheableUrl: Optional[str]


class SubmissionTypeConnection(BaseModel):
    pageInfo: PageInfo
    nodes: List[SubmissionType]


class DatasetSubmissionType(BaseModel):
    submission: SubmissionType


class DatasetSubmissionTypeConnection(BaseModel):
    pageInfo: PageInfo
    nodes: List[DatasetSubmissionType]


# TODO remove, now duplicated in highlihgter-client-v2/training_config.py
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


class TrainingRunArtefactType(BaseModel):
    id: Optional[str]
    checkpoint: Optional[str]
    fileUrl: str
    type: TrainingRunArtefactTypeEnum
    updatedAt: Optional[str] = Field(default_factory=_get_now_str)
    inferenceConfig: Optional[Dict]
    trainingConfig: Optional[Dict]
    supportingFiles: Optional[Dict]

    @validator("type", allow_reuse=True)
    def _val_type(cls, v):
        if v == DEPRECATED_CAPABILITY_IMPLEMENTATION_FILE:
            return v
        else:
            return TrainingRunArtefactTypeEnum(v)

    class Config:
        use_enum_values = True

    @classmethod
    def from_yaml(cls, path: Union[Path, str]):
        path = Path(path)
        with path.open("r") as f:
            data = yaml.safe_load(f)
        return cls(**data)


class TrainingRunType(BaseModel):
    id: int
    name: str
    modelImplementationFileUrl: Optional[str]
    trainingLogsFileUrl: Optional[str]
    trainingRunArtefacts: Optional[List[TrainingRunArtefactType]]
    trainingConfig: Optional[Any]

    # Convert enums to their values
    class Config:
        use_enum_values = True


class ResearchPlanType(BaseModel):
    id: int
    title: str
    # ToDo: Probs need more fields


class ExperimentType(BaseModel):
    id: int
    researchPlan: ResearchPlanType
    title: Optional[str]
    description: Optional[str]
    hypothesis: Optional[str]
    observation: Optional[str]
    conclusion: Optional[str]

    def to_markdown(self, save_path: str):

        def add_markdown_heading(s, heading):
            return f"## {heading}\n{s}\n"

        with open(str(save_path), "w") as f:

            f.write(f"# {self.title}\n")
            f.write(f"- **Experiment ID: {self.id}**\n")
            f.write(f"- **Research Plan ID: {self.researchPlan.id}**\n")
            f.write("\n---\n\n")

            f.write(
                add_markdown_heading(
                    self.description,
                    "Description",
                )
            )

            f.write(
                add_markdown_heading(
                    self.hypothesis,
                    "Hypothesis",
                )
            )

            f.write(
                add_markdown_heading(
                    self.observation,
                    "Observation",
                )
            )

            f.write(
                add_markdown_heading(
                    self.conclusion,
                    "Conclusion",
                )
            )


class PresignedUrlType(BaseModel):
    fields: Dict
    key: str
    storage: str
    url: str


class CompleteFileMultipartUploadPayload(BaseModel):
    errors: List[str]
    url: str


class PipelineInstanceType(BaseModel):
    id: str


class PipelineType(BaseModel):
    id: str


class TaskStatusEnum(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    SUCCESS = "SUCCESS"


class StepType(BaseModel):
    id: str


class AgentType(BaseModel):
    id: str
    machineAgentVersionId: Optional[str]
    userId: Optional[int]


class TaskType(BaseModel):
    id: str
    accountId: int
    createdAt: str
    description: Optional[str]
    image: Optional[ImageType]
    leasedByAgent: Optional[AgentType]
    leasedByPipelineInstance: Optional[PipelineInstanceType]
    leasedUntil: Optional[str]
    message: Optional[str]
    name: Optional[str]
    parameters: Optional[Any]
    pipeline: Optional[PipelineType]
    pipelineId: Optional[str]
    requestedBy: Optional[UserType]
    status: Optional[TaskStatusEnum]
    step: Optional[StepType]
    stepId: Optional[str]
    submission: Optional[SubmissionType]
    tags: Optional[List[str]]
    updatedAt: str

    class Config:
        use_enum_values = True


class ObjectClassType(BaseModel):
    id: int
    name: str
    color: Optional[str]
    annotationsCount: Optional[int]
    accountId: Optional[int]
    default: bool
    parentId: Optional[int]
    entityAttributeEnum: EntityAttributeEnumType
    uuid: str
    createdAt: str
    updatedAt: str


class ProjectObjectClassType(BaseModel):
    id: int
    objectClass: ObjectClassType
    projectId: int
    createdAt: str
    updatedAt: str
    localised: bool
    entityAttributes: List[EntityAttributeType]
    sortOrder: str


class PluginType(BaseModel):
    id: int
    accountId: int
    name: str
    description: str
    url: str
    default: bool
    module: str
    config: Any
    createdAt: str
    updatedAt: str
    projectId: int


class ProjectTypeType(BaseModel):
    id: int
    name: str
    createdAt: str
    updatedAt: str


class AccountType(BaseModel):
    id: int
    name: str
    subdomain: str
    dataUsage: Optional[int]
    organisationName: Optional[str]
    organisationAcn: Optional[str]
    hlServingMqttHost: Optional[str]
    hlServingMqttPort: Optional[int]
    hlServingMqttUsername: Optional[str]
    hlServingMqttSsl: bool
    users: List[UserType]
    createdAt: str
    updatedAt: str


class ImageQueueType(BaseModel):
    id: int
    createdAt: str
    updatedAt: str
    account: AccountType
    projectId: int
    name: str
    projectStageId: str
    objectClasses: List[ObjectClassType]
    submissions: List[SubmissionType]
    latestSubmissions: List[SubmissionType]
    images: List[ImageType]
    allImages: List[ImageType]
    users: List[UserType]
    matchedImageCount: int
    remainingImageCount: int
    lockedImageCount: int
    availableImageCount: int


class ProjectType(BaseModel):
    id: int
    name: str
    description: Optional[str]
    createdById: int
    accountId: int
    parentId: Optional[int]
    objectClasses: List[ObjectClassType]
    projectObjectClasses: List[ProjectObjectClassType]
    plugins: List[PluginType]
    projectType: Optional[ProjectTypeType]
    createdAt: str
    updatedAt: str
    ownedById: int
    modelId: Optional[int]
    activeCheckpointId: Optional[int]
    batchesCount: int
    metadata: Optional[Any]
    settings: Optional[Any]
    requiredAttributes: Optional[Any]
    multilineAttributes: Optional[Any]
    entityAttributeTaxonGroups: Optional[Any]
    ancestry: Optional[str]
    defaultSearchQuery: Optional[str]
    loadMachineSubmissions: bool
    projectTypeId: Optional[int]
    submissions: List[SubmissionType]
    latestSubmissions: List[SubmissionType]
    imageQueues: List[ImageQueueType]


class ProjectOrderType(BaseModel):
    id: str


class ProjectImageType(BaseModel):
    completedAt: Optional[str]
    createdAt: str
    id: int
    image: ImageType
    latestSubmission: Optional[SubmissionType]
    projectId: int
    projectOrder: Optional[ProjectOrderType]
    state: str
    updatedAt: str


class ExperimentResult(BaseModel):
    baselineDatasetId: Optional[int]
    comparisonDatasetId: Optional[int]
    createdAt: str
    entityAttributeId: Optional[str]
    experimentId: int
    objectClassId: Optional[int]
    occuredAt: str
    overlapThreshold: Optional[float]
    researchPlanMetricId: str
    result: float
    updatedAt: str
