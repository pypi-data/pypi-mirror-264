import json
from uuid import uuid4
from pathlib import Path
from typing import List, Tuple, Union

from highlighter.datasets.interfaces import IReader
from highlighter.const import (
        OBJECT_CLASS_ATTRIBUTE_UUID,
        PIXEL_LOCATION_ATTRIBUTE_UUID,
        )
from highlighter.datasets.formats.coco.common import (
        segmentation_to_wkt,
        bbox_to_wkt,
        CocoKeys
        )

from highlighter.datasets.base_models import (
        AttributeRecord,
        ImageRecord,
        )

PathLike = Union[str, Path]

class CocoReader(IReader):
    format_name = "coco"

    def __init__(self,
                 annotations_file: PathLike,
                 bbox_only: bool=False,
                 ):
        """Read a coco dataset from disk into highlighter DataFrame format

        By default, the coco reader will preference the segmentation label
        over the bbox label because we can always infer a bbox from a segmentation
        but not vice versa. You can optionally override this behavior by setting
        the bbox_only option to True. This can be useful if the segmentation labels
        are very large and take a long time to parse

        Args:
          annotations_file: Where to save coco json
          bbox_only: Preference bbox label over segmentation

        """
        self.annotations_file = Path(annotations_file)
        self.bbox_only = bbox_only

    def read(self) -> Tuple[List[AttributeRecord], List[ImageRecord]]:

        with self.annotations_file.open("r") as f:
            coco_data = json.load(f)

        id_to_name = {ele.pop(CocoKeys.ID): ele for ele in coco_data[CocoKeys.CATS]}
        def get_category_name(cat_id):
            return id_to_name[cat_id][CocoKeys.NAME]

        def get_uuid():
            return str(uuid4())

        def get_wkt_str(anno, bbox_only=self.bbox_only):
            if bbox_only:
                wkt = bbox_to_wkt(anno[CocoKeys.BBOX])
            elif CocoKeys.SEG in anno:
                wkt = segmentation_to_wkt(anno[CocoKeys.SEG])
            elif CocoKeys.BBOX in anno:
                wkt = bbox_to_wkt(anno[CocoKeys.BBOX])
            else:
                ValueError((
                        f"Each coco annotation must have either a {SEG} or "
                        f"{BBOX}, got: {anno}"
                        ))
            return wkt

        data_files = {ele.pop(CocoKeys.ID): ele for ele in coco_data[CocoKeys.IMAGES]}
        # Annotations can be polygons or masks. We just want the polygons.
        # https://github.com/cocodataset/cocoapi/blob/master/PythonAPI/pycocotools/coco.py#L255
        attribute_records = []
        data_file_records = []
        processed_data_file_ids = set()
        for anno in coco_data[CocoKeys.ANNOS]:
            # print(coco_data[CocoKeys.ANNOS])
            extra_fields = anno.get(CocoKeys.EXTRA_FIELDS, {})
            entity_uuid = extra_fields.pop("entity_id", get_uuid())
            data_file_id = anno[CocoKeys.IMAGE_ID]
            data_file = data_files[data_file_id]

            if data_file_id not in processed_data_file_ids:
                processed_data_file_ids.update([data_file_id])
                data_file_records.append(
                        ImageRecord(
                            data_file_id=data_file_id,
                            width=data_file[CocoKeys.WIDTH],
                            height=data_file[CocoKeys.HEIGHT],
                            filename=data_file[CocoKeys.FILE_NAME],
                            extra_fields=data_file.get(CocoKeys.EXTRA_FIELDS, {}),
                            )
                        )

            attribute_records.append(
                    AttributeRecord(
                        data_file_id=data_file_id,
                        entity_id = entity_uuid,
                        attribute_id = str(OBJECT_CLASS_ATTRIBUTE_UUID),
                        attribute_name = OBJECT_CLASS_ATTRIBUTE_UUID.label,
                        value = get_category_name(anno[CocoKeys.CAT_ID])
                        )
                    )

            attribute_records.append(
                    AttributeRecord(
                        data_file_id=data_file_id,
                        entity_id = entity_uuid,
                        attribute_id = str(PIXEL_LOCATION_ATTRIBUTE_UUID),
                        attribute_name = PIXEL_LOCATION_ATTRIBUTE_UUID.label,
                        value = get_wkt_str(anno),
                        )
                    )

            for key, value in extra_fields.items():
                attribute_records.append(
                        AttributeRecord(
                            data_file_id=data_file_id,
                            entity_id = entity_uuid,
                            attribute_id = key,
                            attribute_name = "ToDo", # ToDo: Try and lookup from hl
                            value = value,
                            )
                        )

        return data_file_records, attribute_records

