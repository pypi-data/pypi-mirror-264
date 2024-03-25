import enum
import barcode
from barcode.writer import ImageWriter
from ppy_file_text import FileUtil


class BarcodeType(enum.Enum):
    CODE_128 = "code128"
    EAN8 = "ean8"
    EAN13 = "ean13"
    PZN = "pzn"
    CODABAR = "codabar"


class BarcodeGenerator:

    def __get_file_path(self, file_name, file_path):
        if not file_path or not file_name:
            return
        FileUtil.create_directories(file_path)
        filename_with_extension = file_name + ".png"
        filename_and_path = FileUtil.join_path(file_path, filename_with_extension)
        FileUtil.delete(filename_and_path)
        return filename_and_path

    def generate(self, code: str, file_name, file_path, code_type: BarcodeType = BarcodeType.CODE_128, writer=ImageWriter(), options: dict = None):
        barcode_format = barcode.get_barcode_class(code_type.value)
        generated_barcode = barcode_format(code, writer=writer)
        filename_and_path = self.__get_file_path(file_name=file_name, file_path=file_path)
        generated_barcode.save(filename_and_path, options=options)
        return filename_and_path
