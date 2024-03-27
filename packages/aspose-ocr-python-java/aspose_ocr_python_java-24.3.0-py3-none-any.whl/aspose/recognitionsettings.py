import jpype.imports
from typing import List

import aspose.models
from aspose.models import *




class RecognitionSettings():
    """
    Settings for the image recognition.
    Contains elements that allow customizing the recognition process.
    """
    JAVA_CLASS_NAME = "com.aspose.ocr.RecognitionSettings"

    def __init__(self):
        """
        Default constructor: set recognitionAreas null, linesFiltration false, autoSkew false, recognizeSingleLine false.
        """
        asposeClass = jpype.JClass(RecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_recognize_single_line(self, recognizeSingleLine : bool):
        """
        Sets single-line image recognition.
        Disabled (false) by default.
        Disable all the processing steps associated with splitting into lines.
        Set this parameter to true if your image contains only one line. Disables set_recognition_areas settings, so all areas settings will be ignored.
        @param recognizeSingleLine: True for single-line image
        """
        self.getJavaClass().setRecognizeSingleLine(recognizeSingleLine)

    def set_detect_areas_mode(self, detectAreasMode : DetectAreasMode):
        """
        Determines the type of neural network used for areas detection.
        @param detectAreasMode: contains enum DetectAreasMode value.
        """
        jType = aspose.models.ModelsConverter.convertToJavaAreasMode(detectAreasMode)
        self.getJavaClass().setDetectAreasMode(jType)

    def set_language(self, language : Language):
        """
        Sets the language used for OCR.
        Multi-language (none) by default.
        @param language: contains enum Language value.
        """
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters : str):
        """
        Sets blacklist for recognition symbols.
        @param ignoredCharacters: Characters excluded from recognition.
        """
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        """
        Allowed characters set. Determines the array of characters allowed for recognition result.
        @param allowedCharacters: contains string of characters.
        """
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount : int):
        """
        Gets or sets the number of threads for processing.
        By default, 0 means that the image will be processed with the number of threads equal to your number of processors.
        ThreadsCount = 1 means that the image will be processed in the main thread.
        @param threadsCount: the number of threads that will be created for parallel recognition of image fragments.
        """
        self.getJavaClass().setThreadsCount(threadsCount)

    def set_upscale_small_font(self, upscaleSmallFont: bool):
        """
        Allows you to use additional algorithms specifically for small font recognition.
        Useful for images with small size characters.
        @param upscaleSmallFont: contains boolean value - an upscaleSmallFont is set.
        """
        self.getJavaClass().setUpscaleSmallFont(upscaleSmallFont)

    def set_automatic_color_inversion(self, automaticColorInversion: bool):
        """
        Detect images with white text on dark/black background and automatically choose a special OCR algorithm for them.
        @param automaticColorInversion: contains boolean value - a automaticColorInversion is set. True by default.
        """
        self.getJavaClass().setAutomaticColorInversion(automaticColorInversion)



class ReceiptRecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.ReceiptRecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(ReceiptRecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_language(self, language: Language):
        """
        Sets the language used for OCR.
        Multi-language (none) by default.
        @param language: contains enum Language value.
        """
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters: str):
        """
        Sets blacklist for recognition symbols.
        @param ignoredCharacters: Characters excluded from recognition.
        """
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        """
        Allowed characters set. Determines the array of characters allowed for recognition result.
        @param allowedCharacters: contains string of characters.
        """
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount: int):
        """
        Gets or sets the number of threads for processing.
        By default, 0 means that the image will be processed with the number of threads equal to your number of processors.
        ThreadsCount = 1 means that the image will be processed in the main thread.
        @param threadsCount: the number of threads that will be created for parallel recognition of image fragments.
        """
        self.getJavaClass().setThreadsCount(threadsCount)

    def set_upscale_small_font(self, upscaleSmallFont: bool):
        """
        Allows you to use additional algorithms specifically for small font recognition.
        Useful for images with small size characters.
        @param upscaleSmallFont: contains boolean value - an upscaleSmallFont is set.
        """
        self.getJavaClass().setUpscaleSmallFont(upscaleSmallFont)

    def set_automatic_color_inversion(self, automaticColorInversion: bool):
        """
        Detect images with white text on dark/black background and automatically choose a special OCR algorithm for them.
        @param automaticColorInversion: contains boolean value - a automaticColorInversion is set. True by default.
        """
        self.getJavaClass().setAutomaticColorInversion(automaticColorInversion)



class PassportRecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.PassportRecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(PassportRecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_language(self, language: Language):
        """
        Sets the language used for OCR.
        Multi-language (none) by default.
        @param language: contains enum Language value.
        """
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters: str):
        """
        Sets blacklist for recognition symbols.
        @param ignoredCharacters: Characters excluded from recognition.
        """
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        """
        Allowed characters set. Determines the array of characters allowed for recognition result.
        @param allowedCharacters: contains string of characters.
        """
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount: int):
        """
        Gets or sets the number of threads for processing.
        By default, 0 means that the image will be processed with the number of threads equal to your number of processors.
        ThreadsCount = 1 means that the image will be processed in the main thread.
        @param threadsCount: the number of threads that will be created for parallel recognition of image fragments.
        """
        self.getJavaClass().setThreadsCount(threadsCount)

    def set_upscale_small_font(self, upscaleSmallFont: bool):
        """
        Allows you to use additional algorithms specifically for small font recognition.
        Useful for images with small size characters.
        @param upscaleSmallFont: contains boolean value - an upscaleSmallFont is set.
        """
        self.getJavaClass().setUpscaleSmallFont(upscaleSmallFont)

    def set_automatic_color_inversion(self, automaticColorInversion: bool):
        """
        Detect images with white text on dark/black background and automatically choose a special OCR algorithm for them.
        @param automaticColorInversion: contains boolean value - a automaticColorInversion is set. True by default.
        """
        self.getJavaClass().setAutomaticColorInversion(automaticColorInversion)



class IDCardRecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.IDCardRecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(IDCardRecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_language(self, language: Language):
        """
        Sets the language used for OCR.
        Multi-language (none) by default.
        @param language: contains enum Language value.
        """
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters: str):
        """
        Sets blacklist for recognition symbols.
        @param ignoredCharacters: Characters excluded from recognition.
        """
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        """
        Allowed characters set. Determines the array of characters allowed for recognition result.
        @param allowedCharacters: contains string of characters.
        """
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount: int):
        """
        Gets or sets the number of threads for processing.
        By default, 0 means that the image will be processed with the number of threads equal to your number of processors.
        ThreadsCount = 1 means that the image will be processed in the main thread.
        @param threadsCount: the number of threads that will be created for parallel recognition of image fragments.
        """
        self.getJavaClass().setThreadsCount(threadsCount)

    def set_upscale_small_font(self, upscaleSmallFont: bool):
        """
        Allows you to use additional algorithms specifically for small font recognition.
        Useful for images with small size characters.
        @param upscaleSmallFont: contains boolean value - an upscaleSmallFont is set.
        """
        self.getJavaClass().setUpscaleSmallFont(upscaleSmallFont)

    def set_automatic_color_inversion(self, automaticColorInversion: bool):
        """
        Detect images with white text on dark/black background and automatically choose a special OCR algorithm for them.
        @param automaticColorInversion: contains boolean value - a automaticColorInversion is set. True by default.
        """
        self.getJavaClass().setAutomaticColorInversion(automaticColorInversion)



class InvoiceRecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.InvoiceRecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(InvoiceRecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_language(self, language: Language):
        """
        Sets the language used for OCR.
        Multi-language (none) by default.
        @param language: contains enum Language value.
        """
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters: str):
        """
        Sets blacklist for recognition symbols.
        @param ignoredCharacters: Characters excluded from recognition.
        """
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        """
        Allowed characters set. Determines the array of characters allowed for recognition result.
        @param allowedCharacters: contains string of characters.
        """
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount: int):
        """
        Gets or sets the number of threads for processing.
        By default, 0 means that the image will be processed with the number of threads equal to your number of processors.
        ThreadsCount = 1 means that the image will be processed in the main thread.
        @param threadsCount: the number of threads that will be created for parallel recognition of image fragments.
        """
        self.getJavaClass().setThreadsCount(threadsCount)

    def set_upscale_small_font(self, upscaleSmallFont: bool):
        """
        Allows you to use additional algorithms specifically for small font recognition.
        Useful for images with small size characters.
        @param upscaleSmallFont: contains boolean value - an upscaleSmallFont is set.
        """
        self.getJavaClass().setUpscaleSmallFont(upscaleSmallFont)

    def set_automatic_color_inversion(self, automaticColorInversion: bool):
        """
        Detect images with white text on dark/black background and automatically choose a special OCR algorithm for them.
        @param automaticColorInversion: contains boolean value - a automaticColorInversion is set. True by default.
        """
        self.getJavaClass().setAutomaticColorInversion(automaticColorInversion)



class CarPlateRecognitionSettings():
    JAVA_CLASS_NAME = "com.aspose.ocr.CarPlateRecognitionSettings"

    def __init__(self):
        asposeClass = jpype.JClass(CarPlateRecognitionSettings.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    def set_language(self, language: Language):
        """
        Sets the language used for OCR.
        Multi-language (none) by default.
        @param language: contains enum Language value.
        """
        jType = aspose.models.ModelsConverter.convertToJavaLanguage(language)
        self.getJavaClass().setLanguage(jType)

    def set_ignored_characters(self, ignoredCharacters: str):
        """
        Sets blacklist for recognition symbols.
        @param ignoredCharacters: Characters excluded from recognition.
        """
        self.getJavaClass().setIgnoredCharacters(ignoredCharacters)

    def set_allowed_characters(self, allowedCharacters: str):
        """
        Allowed characters set. Determines the array of characters allowed for recognition result.
        @param allowedCharacters: contains string of characters.
        """
        self.getJavaClass().setAllowedCharacters(allowedCharacters)

    def set_threads_count(self, threadsCount: int):
        """
        Gets or sets the number of threads for processing.
        By default, 0 means that the image will be processed with the number of threads equal to your number of processors.
        ThreadsCount = 1 means that the image will be processed in the main thread.
        @param threadsCount: the number of threads that will be created for parallel recognition of image fragments.
        """
        self.getJavaClass().setThreadsCount(threadsCount)