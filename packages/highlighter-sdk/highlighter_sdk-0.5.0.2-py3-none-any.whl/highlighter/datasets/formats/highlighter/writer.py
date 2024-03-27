import warnings
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID
from tqdm import tqdm
from datetime import datetime

from pydantic import BaseModel, StrictBool, StrictFloat, StrictInt, StrictStr, validator, conlist

from highlighter.base_models import ObjectClass, SubmissionType
from highlighter.datasets.interfaces import IWriter
from highlighter.gql_client import HLClient
from highlighter.labeled_uuid import LabeledUUID

tqdm.pandas()

def is_valid_uuid(attr_id):
    if isinstance(attr_id, (LabeledUUID, UUID)):
        return True
    try:
        UUID(attr_id)
        return True
    except (ValueError, TypeError):
        return False

class CreateAssessmentPayload(BaseModel):
    submission: Optional[SubmissionType]
    errors: List[str]


class DatumSourceInputType(BaseModel):
    pipelineId: Optional[int]
    pipelineElementId: Optional[str]
    pipelineElementName: Optional[str]
    trainingRunId: Optional[int]
    confidence: float
    hostId: Optional[int]


class EAVTInputType(BaseModel):
    entityId: Union[str, UUID]  # GUID
    attributeId: Union[str, UUID]  # GUID
    value: Union[StrictInt, StrictFloat, StrictBool, UUID, conlist(int, min_items=1), StrictStr]
    datumSource: Optional[DatumSourceInputType]
    time: str = datetime.now().isoformat()

    @validator("attributeId")
    def cast_attributId_to_str(cls, v):
        return str(v)

    @validator("entityId")
    def cast_entityId_to_str(cls, v):
        return str(v)

    @validator("value")
    def cast_value_uuid_to_str(cls, v):
        if isinstance(v, (UUID, LabeledUUID)):
            return str(v)
        return v


class CreateAssessmentParams(BaseModel):
    projectId: int
    userID: int
    imageId: int
    status: str = "completed"
    startedAt: str = datetime.now().isoformat()
    eavtAttributes: List[EAVTInputType]


PathLike = Union[str, Path]

class HighlighterAssessmentsWriter(IWriter):

    format_name = "highlighter_assessments"

    def __init__(
        self,
        client: HLClient,
        workflow_id: int,
        object_class_uuid_lookup: Optional[Dict[str, str]] = None,
        user_id: Optional[int] = None
    ):
        self.client = client
        self.user_id = user_id
        self.workflow_id = workflow_id

        if object_class_uuid_lookup is None:
            self.object_class_uuid_lookup = self._get_project_object_class_uuid_lookup()
        else:
            self.object_class_uuid_lookup = object_class_uuid_lookup

    def _get_project_object_class_uuid_lookup(self):
        class Project(BaseModel):
            objectClasses: List[ObjectClass]

        object_classes = self.client.project(
            return_type=Project, id=self.workflow_id
        ).objectClasses
        lookup = {o.name: o.uuid for o in object_classes}
        lookup.update({o.id: o.uuid for o in object_classes})
        return lookup

    def write(
        self,
        dataset: "Dataset",
    ):
        """Write to highlighter assessments in project"""

        def img_group_to_subs(
            name, grp, dataset, object_class_uuid_lookup=self.object_class_uuid_lookup
        ):
            data_file_id = name
            attrs = grp.to_dict("records")

            eavt_attrs = []
            for attr in attrs:
                entity_id = attr["entity_id"]
                attr_id = attr["attribute_id"]

                if is_valid_uuid(attr_id):
                    # Cast/validate attribute value
                    value = attr["value"]

                    if isinstance(value, str):
                        value = str(self.object_class_uuid_lookup.get(value, value))

                    eavt_attrs.append(
                        EAVTInputType(
                            entityId=entity_id,
                            attributeId=attr_id,
                            value=value,
                            datumSource=DatumSourceInputType(
                                confidence=float(attr["confidence"])
                            ),
                        ).dict()
                    )
                else:
                    warnings.warn((f"Skipping invallid attribute_id, got: '{attr_id}'"))

            kwargs = {"userId": self.user_id}
            kwargs = {k:v for k,v in kwargs.items() if v is not None}

            response = self.client.create_submission(
                return_type=CreateAssessmentPayload,
                projectId=self.workflow_id,
                imageId=data_file_id,
                status="completed",
                startedAt=datetime.now().isoformat(),
                eavtAttributes=eavt_attrs,
                **kwargs,
            )

            if (response.submission is None) or (response.errors):
                warnings.warn(
                    "Failed to create assessment: {} ".format(response.errors)
                )

            # We check if data_files_df is populated before adding these fields
            # because when we're just performing inference we may not have this
            # DataFrame populated.
            elif dataset.data_files_df.shape[0] > 0:

                # update assessment_id and hash
                dataset.data_files_df.loc[
                    dataset.data_files_df.data_file_id == data_file_id, "assessment_id"
                ] = response.submission.id
                dataset.data_files_df.loc[
                    dataset.data_files_df.data_file_id == data_file_id, "hash_signature"
                ] = response.submission.hashSignature

        # group annotations by data_file id and create assessments
        for name, grp in tqdm(dataset.annotations_df.groupby("data_file_id")):
            img_group_to_subs(name, grp, dataset)

