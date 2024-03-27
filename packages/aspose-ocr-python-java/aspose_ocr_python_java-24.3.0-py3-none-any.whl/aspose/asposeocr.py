# Aspose.OCR for Python via Java
# Main functionality of the interface
#
# Author:   aspose
# Created:  Nov 2023
#
# Copyright (C) 2013 Aspose
# For license information, see LICENSE.txt

"""
Python interface to the Aspose OCR

**Aspose.OCR for Python via .Java** is a powerful,
while easy-to-use optical character recognition (OCR)
 engine for your Python applications and notebooks.
In less than **10** lines of code, you can recognize
text in **28** languages based on Latin, Cyrillic,
and Asian scripts, returning results in the most popular
document and data interchange formats.
There is no need to learn complex mathematical models,
build machine learning algorithms and train neural
networks — our simple and robust API will do everything for you.
"""

##########################################################################
## Imports
##########################################################################

import jpype.imports

import typing

import aspose.recognitionsettings
from .helper import *
from .recognitionresult import *
from .recognitionsettings import *
from .models import *

#from com.aspose.ocr import *

##########################################################################
## Main Functionality
##########################################################################

class Resources():
    """
    Manage downloadable resources that enhance Aspose.OCR recognition capabilities.

    @author Aspose
    @version 24.3.0
    """
    __JAVA_CLASS_NAME = "com.aspose.ocr.Resources"

    @staticmethod
    def __init__():
        Resources.asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        #self.__initJavaClass(asposeClass())

    @staticmethod
    def set_repository(url: str):
        """
        Specify the URL of the online repository from which Aspose.OCR resources will be downloaded.
        By default, the resources are downloaded from https://github.com/aspose-ocr/resources/.
        @param url: URL of the online repository.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        asposeClass.SetRepository(url)

    @staticmethod
    def get_repository():
        """
        Return the URL of the online repository from which Aspose.OCR resources are downloaded.
        @return URL of the online repository.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        return asposeClass.GetRepository()

    @staticmethod
    def list_remote() -> [str]:
        """
        List all compatible resources from the online repository.
        @return List of resources names.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        result = []
        list = asposeClass.ListRemote()
        for res in list:
            result.append(res)
        return result

    @staticmethod
    def set_local_path(path : str, create : bool = True):
        """
        Specify an absolute or relative path to the directory where the resources will be downloaded.
        Pass `false` to the `create` parameter to prevent the directory from being created automatically.
        If the provided directory does not exist and creation is not allowed, the resources will be loaded into the aspose_data directory in the application's working directory.
        @param path: Absolute or relative path to the directory.
        @param create: Parameter to prevent the directory from being created automatically.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        asposeClass.SetLocalPath(path, create)

    @staticmethod
    def get_local_path():
        """
        Return the full path to the directory where the resources will be downloaded.
        @return String with the path to the resources directory.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        return asposeClass.GetLocalPath()

    @staticmethod
    def list_local() -> [str]:
        """
        List all Aspose.OCR resources stored in the local directory.
        @return List all Aspose.OCR resources stored in the local directory.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        result = []
        for res in asposeClass.ListLocal():
            result.append(res)
        return result

    @staticmethod
    def allow_automatic_downloads(allow : bool):
        """
        Allow (true) or block (false) automatic downloading of required resources from the online repository.
        By default, a resource is automatically downloaded when a method that depends on it is called.
        @param allow: Boolean value to allow or block automatic downloading of required resources.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        asposeClass.AllowAutomaticDownloads(allow)

    @staticmethod
    def fetch_resources(names: []):
        """
        Download the resources specified in the `names` parameter from the online repository. If one or more resources are already downloaded, they will be overwritten.
        You can omit the .OCR extension and use file names only.
        @param names: Array with resources names. See the ListRemote method.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        asposeClass.FetchResources(names)

    @staticmethod
    def fetch_all():
        """
        Download all compatible resources from the online repository. The existing resource files will be overwritten.
        """
        asposeClass = jpype.JClass(Resources.__JAVA_CLASS_NAME)
        asposeClass.FetchAll()



class AsposeOcr():
    """
    AsposeOcr main class for recognition.

    This sample shows how to recognize image.
    \code
        api = AsposeOcr()
        input = OcrInput(InputType.SINGLE_IMAGE)
        input.add(os.path.join(self.dataDir, "SpanishOCR.bmp"))
        result = api.recognize(input)
    \endcode
    """
    __JAVA_CLASS_NAME = "com.aspose.ocr.AsposeOCR"

    def __init__(self):
        asposeClass = jpype.JClass(self.__JAVA_CLASS_NAME)
        self.__initJavaClass(asposeClass())

    def __initJavaClass(self, javaClass: object):
        self.__javaClass = javaClass
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def image_has_text(self, fullPath : str, text : str, settings : RecognitionSettings = None, ignoreCase : bool = True) -> bool:
        """
        Check if the image contains the provided text fragment.
        @param fullPath: Path to the image.
        @param text: Text fragment for searching on the image.
        @param settings: Recognition settings.
        @param ignoreCase: True - means a case-insensitive search.
        @return: True if image contains text fragment. False - image doesn't contains text fragment.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()
        return self.__getJavaClass().ImageHasText(fullPath, text, settings, ignoreCase)

    def compare_image_texts(self, fullPath1: str, fullPath2: str, settings: RecognitionSettings = None,
                            ignoreCase: bool = True) -> bool:
        """
        Check if two images contain the same text.
        @param fullPath1: Path to the first image.
        @param fullPath2: Path to the second image.
        @param settings: Recognition settings.
        @param ignoreCase: True - means a case-insensitive search.
        @return: True if images have the same text (90% similarity).
        """
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()
        return self.__getJavaClass().CompareImageTexts(fullPath1, fullPath2, settings, ignoreCase)

    def image_text_diff(self, fullPath1 : str, fullPath2 : str, settings : RecognitionSettings = None, ignoreCase : bool = True) -> float:
        """
        Compare the texts on the two images and return a number representing how similar they are (0 to 1).
        @param fullPath1: Path to the first image.
        @param fullPath2: Path to the second image.
        @param settings: Recognition settings.
        @param ignoreCase: True - means a case-insensitive search.
        @return: 0 means that the texts are completely different; 1 means the texts are identical.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()
        return self.__getJavaClass().ImageTextDiff(fullPath1, fullPath2, settings, ignoreCase)

    def recognize(self, input: OcrInput, settings: RecognitionSettings = None) -> typing.List[RecognitionResult]:
        """
        Recognizes image with the ability to specify RecognitionSettings.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param settings: RecognitionSettings object.
        @return: RecognitionResult list with images recognition results.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().Recognize(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_street_photo(self, input: OcrInput) -> typing.List[RecognitionResult]:
        """
        Recognizes text on street photos.
        Extract text from street photos, traffic camera images, ID cards, driver licenses, and other images with sparse text and noisy/colored backgrounds.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @return: RecognitionResult list with images recognition results.
        """
        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizeStreetPhoto(inputJava)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_receipt(self, input: aspose.models.OcrInput, settings: aspose.recognitionsettings.ReceiptRecognitionSettings = None) -> typing.List[RecognitionResult]:
        """
        Recognize receipts with the ability to specify ReceiptRecognitionSettings.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param settings: ReceiptRecognitionSettings
        @return: RecognitionResult list with images recognition results.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.ReceiptRecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizeReceipt(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_invoice(self, input: aspose.models.OcrInput, settings: aspose.recognitionsettings.InvoiceRecognitionSettings = None) -> typing.List[RecognitionResult]:
        """
        Recognize invoice with the ability to specify InvoiceRecognitionSettings
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param settings: InvoiceRecognitionSettings
        @return: RecognitionResult list with images recognition results.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.InvoiceRecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizeInvoice(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_id_card(self, input: aspose.models.OcrInput,
                            settings: aspose.recognitionsettings.IDCardRecognitionSettings = None) -> typing.List[RecognitionResult]:
        """
        Recognizes ID card with the ability to specify IDCardRecognitionSettings.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param settings: IDCardRecognitionSettings
        @return: RecognitionResult list with images recognition results.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.IDCardRecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizeIDCard(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_car_plate(self, input: aspose.models.OcrInput,
                            settings: aspose.recognitionsettings.CarPlateRecognitionSettings = None) -> typing.List[RecognitionResult]:
        """
        Recognizes car plate with the ability to specify CarPlateRecognitionSettings.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param settings: CarPlateRecognitionSettings
        @return: RecognitionResult list with images recognition results.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.CarPlateRecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizeCarPlate(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_passport(self, input: aspose.models.OcrInput,
                            settings: aspose.recognitionsettings.PassportRecognitionSettings = None) -> typing.List[RecognitionResult]:
        """
        Recognizes passport with the ability to specify PassportRecognitionSettings.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param settings: PassportRecognitionSettings
        @return: RecognitionResult list with images recognition results.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.PassportRecognitionSettings()
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().RecognizePassport(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult



    def recognize_fast(self, input : OcrInput) -> typing.List[RecognitionResult]:
        """
        Recognizes text on good quality image. Doesn't use automatic image skew correction and text areas
        detection.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @return: RecognitionResult list with images recognition results.
        """
        inputJava = input.getJavaClass()
        results = self.__javaClass.RecognizeFast(inputJava)
        pythonResult = []
        for result in results:
            r = str(result)
            pythonResult.append(r)

        return pythonResult

    def recognize_lines(self, input: OcrInput, settings: RecognitionSettings = None) -> typing.List[RecognitionResult]:
        """
        Recognizes single line image with the ability to specify RecognitionSettings.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param settings: RecognitionSettings object.
        @return: RecognitionResult list with images recognition results.
        """
        if (settings == None):
            settings = aspose.recognitionsettings.RecognitionSettings()
        settings.set_recognize_single_line(True)
        settings = settings.getJavaClass()

        inputJava = input.getJavaClass()
        results = self.__getJavaClass().Recognize(inputJava, settings)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RecognitionResult(result)
            pythonResult.append(r)

        return pythonResult

    def calculate_skew(self, input: OcrInput) -> typing.List[SkewOutput]:
        """
        Calculates the skew angles of an images.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance. The container with sources.
        @return: List of skew angles in degrees - SkewOutput.
        """
        inputJava = input.getJavaClass()
        results = self.__getJavaClass().CalculateSkew(inputJava)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.SkewOutput(result)
            pythonResult.append(r)
        return pythonResult

    def detect_rectangles(self, input: OcrInput, areasType : aspose.models.AreasType, isDetectAreas : bool) -> typing.List[RectangleOutput]:
        """
        Detects text areas on images.
        Supports GIF, PNG, JPEG, WBMP, TIFF, JFIF, TIFF, PDF, binary array, folder, array, zip archive, URL, base64.
        @param input: :py:any:`~aspose.models.OcrInput`. instance.
        @param areasType: Determinates wich rectangles to return - line, paragraphs or words.
        @param isDetectAreas: Enable automatic text areas detection.
        @return: List of RectangleOutput with detected text areas or lines.
        """
        inputJava = input.getJavaClass()
        jAreasType = ModelsConverter.convertToJavaAreasType(areasType)
        results = self.__getJavaClass().DetectRectangles(inputJava, jAreasType, isDetectAreas)

        pythonResult = []
        for result in results:
            r = aspose.recognitionresult.RectangleOutput(result)
            pythonResult.append(r)
        return pythonResult


    def correct_spelling(self, text : str, language : SpellCheckLanguage) -> str:
        """
        Corrects text (replaces misspelled words).
        @param text: Text for correction.
        @param language: Dictionary to use SpellCheckLanguage.
        @return: Text with replaced words.
        """
        jType = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        return self.__javaClass.CorrectSpelling(text, jType)



    @staticmethod
    def save_multipage_document(fullFileName: str, saveFormat: Format, results: List):
        """
        Allows to get multipage document from list of RecognitionResult objects.
        @param fullFileName: Filename with a path for saving recognition result in the selected format.
        @param saveFormat: Document format (Docx, Txt, Pdf, Xlsx, Xml, Json).
        @param results:
        """
        javaList = Helper.converToArrayList(results)
        javaStrClass = jpype.JClass('java.lang.String')
        javaStr = javaStrClass(fullFileName)
        asposeClass = jpype.JClass(AsposeOcr.__JAVA_CLASS_NAME)

        format = ModelsConverter.convertToJavaFormat(saveFormat)
        asposeClass.SaveMultipageDocument(javaStr, format, javaList)


    def shutdown(self):
        """
        Shut down the JVM machine.
        """
        jpype.shutdownJVM()


    def __getJavaClass(self):
        return self.__javaClass


class ImageProcessing():
    """
    Helper class for Aspose OCR library. Allows to preprocess and save images.
    """
    __JAVA_CLASS_NAME = "com.aspose.ocr.ImageProcessing"

    @staticmethod
    def save(images, folderPath):
        """
        Use image processing to improve the accuracy of OCR.
        Create a list of filters that will be applied to the input image in the order you specify.
        \code
            filters = new PreprocessingFilter();
            filters.add(PreprocessingFilter.auto_dewarping());
            filters.add(PreprocessingFilter.invert());
            filters.add(PreprocessingFilter.threshold(150));
            filters.add(PreprocessingFilter.binarize());
            filters.add(PreprocessingFilter.rotate(180));
            filters.add(PreprocessingFilter.scale(6));
            filters.add(PreprocessingFilter.dilate());

            images = OcrInput(InputType.PDF, filters);
        \endcode
        You don't need all of them. Set only what you need.
        @param images: OcrInput object containing different images OcrInput.
        @param folderPath: Path without image names for saving processed images.
        @return: OcrInput object containing result processed images OcrInput.
        """
        asposeClass = jpype.JClass(ImageProcessing.__JAVA_CLASS_NAME)
        inputJava = images.getJavaClass()
        joutput = asposeClass.Save(inputJava, folderPath)
        outputJava = aspose.models.OcrInput(aspose.models.InputType.SINGLE_IMAGE)
        outputJava.init(joutput)
        return outputJava
