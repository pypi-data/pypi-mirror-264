import jpype
import os
from aspose import asposeocr, models, recognitionsettings, recognitionresult, license

__asposeocr_dir__ = os.path.dirname(__file__)
__ocr_jar_path__ = __asposeocr_dir__ + "/jlib/aspose-ocr-24.3.0.jar"
__onnx_jar_path__ = __asposeocr_dir__ + "/jlib/onnxruntime-1.16.0.jar"

jpype.startJVM('-ea', classpath=[__ocr_jar_path__, __onnx_jar_path__])


__all__ = ['asposeocr', 'models', 'recognitionsettings', 'recognitionresult', 'license', 'helper']

from .recognitionsettings import CarPlateRecognitionSettings
from .recognitionsettings import IDCardRecognitionSettings
from .recognitionsettings import InvoiceRecognitionSettings
from .recognitionsettings import PassportRecognitionSettings
from .recognitionsettings import ReceiptRecognitionSettings
from .recognitionsettings import *
from .recognitionresult import *
from .asposeocr import AsposeOcr
from .asposeocr import Resources
from .license import *

