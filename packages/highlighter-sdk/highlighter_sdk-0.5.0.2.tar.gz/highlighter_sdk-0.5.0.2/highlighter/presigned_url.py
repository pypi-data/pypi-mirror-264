from typing import List
from pydantic import BaseModel

from .gql_client import HLClient
from .pagination import paginate
from .base_models import (
        ImagePresignedType,
        PageInfo,
        )

__all__ = [
        "get_presigned_url",
        "get_presigned_urls",
        ]

def get_presigned_url(
        client: HLClient,
        id: int,
        ):
    """Return a single ImagePresignedType BaseModel
    for the given file id
    """
    result = client.image(
            return_type=ImagePresignedType,
            id=id,
            )
    return result

class ImageTypeConnection(BaseModel):
    pageInfo: PageInfo
    nodes: List[ImagePresignedType]

def get_presigned_urls(
        client,
        ids: List[int],
        ):
    """Return a generator of ImagePresignedType BaseModels
    for the given list of file ids
    """
    return paginate(
            client.imageConnection,
            ImageTypeConnection,
            id=ids,
            )
