import mimetypes
from pathlib import Path
from typing import List, Tuple
from highlighter.datasets.interfaces import IReader
from highlighter.datasets.base_models import (
        AttributeRecord,
        ImageRecord,
        )
from highlighter.const import (
        OBJECT_CLASS_ATTRIBUTE_UUID,
        PIXEL_LOCATION_ATTRIBUTE_UUID,
        )
from warnings import warn

__all__ = ["HighlighterAssessmentsReader",
        ]

class HighlighterAssessmentsReader(IReader):

    format_name = "highlighter_assessments"
    def __init__(self, assessments_gen):
        self.assessments_gen = assessments_gen

    def read(self) -> Tuple[List[AttributeRecord], List[ImageRecord]]:
        attribute_records = []
        data_file_records = []
        for i, assessment in enumerate(self.assessments_gen):

            data_file = assessment.image
            assessment_id = assessment.id
            hash_signature = assessment.hashSignature
            data_file_id = data_file.id
            filename_original = Path(data_file.originalSourceUrl)

            ext = filename_original.suffix
            if ext == "":
                ext = mimetypes.guess_extension(data_file.mimeType).lower()

            filename = f"{data_file_id}{ext}"
            data_file_records.append(
                    ImageRecord(
                        data_file_id=data_file_id,
                        width=data_file.width,
                        height=data_file.height,
                        filename=filename,
                        extra_fields={"filename_original": str(filename_original)},
                        assessment_id=assessment_id,
                        hash_signature=hash_signature,
                        )
                    )

            for eavt in assessment.entityAttributeValues:
                """EntityAttributeValueType(entityAttributeId='570cbb54-3c18-4887-a907-5c44bc1a3862', entityAttributeEnumId=None, value='True', entityId='7755292d-0959-4940-bef3-4dc38eac6148')
                """
                value = eavt.value
                if value is None:
                    value = eavt.entityAttributeEnum.id

                datum_source = eavt.entityDatumSource
                if datum_source is None:
                    conf = 1.0
                else:
                    conf = datum_source.confidence

                attribute_records.append(
                        AttributeRecord(
                            data_file_id=data_file_id,
                            entity_id=eavt.entityId,
                            attribute_id=eavt.entityAttribute.id,
                            attribute_name=eavt.entityAttribute.name,
                            value=value,
                            confidence=conf,
                            )
                        )


            for annotation in assessment.annotations:
                # Why empty entityAttributeValues
                # This polecap from eq dataset 155 should have one.
                # Ahhh this dataset was created before the
                # entityAttribute label was made.
                # You'll need to find/create a dataset with one.
                # Link to data_file below:
                # https://energy-queensland.highlighter.ai/data_files/5706377
                """AssessmentType(imageId=5706377, annotations=[AnnotationType(location='POLYGON ((1639.0 1490.0, 1775.0 1490.0, 1775.0 1609.0, 1639.0 1609.0, 1639.0 1490.0))', confidence=1.0, agentName='Lucas Belz', isInference=False, objectClass=ObjectClass(id='2047', uuid='a6ff0dd3-6397-4353-a6e3-99bbab02c118', name='Pole Cap'))], entityAttributeValues=[])
                """
                """
                | imageId | Polygon | objectClass | ConditionCode |
                | 001     | ...     | x_arm       |    NA         |
                | 001     | ...     | NA          |    P0         |

                # Go with this one
                | imageId | entityId | attrType      | attrValue  |
                | 001     |          | Objectclass   |    x_arm   |
                | 001     |          | ConditionCode |    P0      |

                """
                if annotation.location is None:
                    warn("Null value found in location. Get it together bro.")
                    continue

                confidence = getattr(annotation, "confidence", None)
                object_class = annotation.objectClass
                attribute_records.append(
                        AttributeRecord(
                            data_file_id=data_file_id,
                            entity_id=annotation.entityId,
                            attribute_id=str(OBJECT_CLASS_ATTRIBUTE_UUID),
                            attribute_name=OBJECT_CLASS_ATTRIBUTE_UUID.label,
                            value=object_class.uuid,
                            frame_id=annotation.frameId,
                            confidence=confidence,
                            )
                        )
                attribute_records.append(
                        AttributeRecord(
                            data_file_id=data_file_id,
                            entity_id=annotation.entityId,
                            attribute_id=str(PIXEL_LOCATION_ATTRIBUTE_UUID),
                            attribute_name=PIXEL_LOCATION_ATTRIBUTE_UUID.label,
                            value=annotation.location,
                            frame_id=annotation.frameId,
                            confidence=confidence,
                            )
                        )

        return data_file_records, attribute_records

