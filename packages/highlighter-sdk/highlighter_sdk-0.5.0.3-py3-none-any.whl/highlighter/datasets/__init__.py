from pathlib import Path
import tempfile
from typing import Optional
from pydantic import BaseModel
from .base_models import *
from .dataset import Dataset, DatasetFormat
from .formats.coco.reader import CocoReader
from .formats.coco.writer import CocoWriter
from .formats.coco.common import CocoCategory, bbox_to_wkt, segmentation_to_wkt
from .formats.highlighter.reader import HighlighterAssessmentsReader
from .formats.highlighter.writer import HighlighterAssessmentsWriter
from ..pagination import paginate, DEFAULT_PAGE_SIZE
from ..base_models import DatasetSubmissionTypeConnection

# These 4 imports are made availiable from this file
# for backwards compatability.
from .formats import get_reader, get_writer, READERS, WRITERS

__all__ = [
        "get_reader",
        "get_writer",
        "read_dataset_from_highlighter",
        "write_assessments_to_highlighter",
        "READERS",
        "WRITERS",
        "bbox_to_wkt",
        "segmentation_to_wkt",
        ]

def read_dataset_from_highlighter(
        client: "HLClient",
        dataset_id: int,
        datasets_cache_dir: Path=None,
        data_files_cache_dir: Path=None,
        page_size: int=DEFAULT_PAGE_SIZE,
        ):
    """Reads and initializes a dataset stored in HL
    """
    ds = Dataset.read_from(
            dataset_format=DatasetFormat.HIGHLIGHTER_DATASET,
            client=client,
            dataset_id=dataset_id,
            datasets_cache_dir=datasets_cache_dir,
            data_files_cache_dir=data_files_cache_dir,
            page_size=page_size,
            )

    return ds


def write_assessments_to_highlighter(client, ds, workflow_id, user_id=None):
    """Write a dataset as assessments to a highlighter workflow

    Args:
        client (highlighter.gql_client.HLClient): graphql client
        ds (highlighter.datasets.Dataset): dataset to write
        workflow_id (int): id of workflow to write new assessments to
        user_id (int): id of the user to be the 'submitter' e.g. 493, default=None

    Returns:
        _type_: dataset with updated assessment id's and hashes (edited in place)
    """
    writer = get_writer("highlighter_assessments")(
            client, workflow_id, user_id=user_id)

    writer.write(ds)

    return ds

