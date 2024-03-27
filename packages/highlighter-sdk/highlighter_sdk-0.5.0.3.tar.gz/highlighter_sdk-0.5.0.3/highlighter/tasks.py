from typing import Any, Dict, List, Optional
from pydantic import BaseModel

import highlighter as hl
from highlighter.base_models import SubmissionType

__all__ = ["update_task_result"]

class UpdateTaskResultPayload(BaseModel):
    assessment: SubmissionType
    errors: List[Any]

def update_task_result(client: hl.HLClient,
                       task_id: str,
                       status: str,
                       observations: List[Dict] = [],
                       background_info_layer_file_data: Optional[Dict]=None,
                       ):
    assert status in ("PENDING", "RUNNING", "FAILED", "SUCCESS")

    kwargs = {"id": task_id,
              "status": status,
              "eavtAttributes": observations,
            }
    if background_info_layer_file_data is not None:
        kwargs["backgroundInfoLayerFileData"] = background_info_layer_file_data

    result = client.updateTaskResultV2(return_type=UpdateTaskResultPayload,
                                       **kwargs)
    return result
