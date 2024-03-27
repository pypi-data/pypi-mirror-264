from .coco.reader import CocoReader
from .coco.writer import CocoWriter

from .highlighter.reader import HighlighterAssessmentsReader
from .highlighter.writer import HighlighterAssessmentsWriter

from .torch_image_folder.writer import TorchImageFolderWriter
from .torch_image_folder.reader import TorchImageFolderReader

READERS = {
        CocoReader.format_name: CocoReader,
        HighlighterAssessmentsReader.format_name: HighlighterAssessmentsReader,
        TorchImageFolderReader.format_name: TorchImageFolderReader,
        }

WRITERS = {
        CocoWriter.format_name: CocoWriter,
        HighlighterAssessmentsWriter.format_name: HighlighterAssessmentsWriter,
        TorchImageFolderWriter.format_name: TorchImageFolderWriter,
        }


def get_reader(name):
    return READERS[name]

def get_writer(name):
    return WRITERS[name]
