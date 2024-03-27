from . import helper
import jpype.imports
from aspose.models import *



class LinesResult(helper.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.text_in_line = None
        self.line = None
        self.initParams()

    def initParams(self):
        self.text_in_line = self.getJavaClass().textInLine
        self.line = self.getJavaClass().line

class RecognitionResult():
    """
    The results of the image recognition. Contains elements with recognition
    information and methods for result export.
    """
    __JAVA_CLASS_NAME = "com.aspose.ocr.RecognitionResult"

    def __init__(self, javaClass):
        self.__javaClass = javaClass
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

        self.recognition_areas_text = []
        """
        List recognition results of a list of areas (Rectangles).
        """
        self.recognition_lines_result = []
        """
        Gets a list of recognition results with a list of rows (Rectangles).
        """
        self.init()


    def init(self):
        for t in self.getJavaClass().recognitionAreasText:
            self.recognition_areas_text.append(t)

        for t in self.getJavaClass().recognitionLinesResult:
            lines = LinesResult(t)
            self.recognition_lines_result.append(lines)
        self.recognition_text = self.getJavaClass().recognitionText
        """
        Recognition result of all page or one area.
        """
        self.recognition_areas_rectangles = self.getJavaClass().recognitionAreasRectangles
        """
        List recognition results of a list of areas (Rectangles).
        """
        self.skew = self.getJavaClass().skew
        """
        Skew angle of the image.
        """
        self.warnings = self.getJavaClass().warnings
        """
        Gets or sets list of the warnings messages describing non-critical faults
        appeared during generation.
        """
        self.recognition_characters_list = self.getJavaClass().recognitionCharactersList
        """
        A set of characters found by the recognition algorithm and arranged in descending order of probability.
        """


    def getJavaClass(self):
        return self.__javaClass

    def get_json(self):
        """
        Form JSON string with recognition results.
        @return: Recognition results as JSON string.
        """
        return self.getJavaClass().GetJson()

    def get_xml(self):
        """
        Form JSON string with recognition results.
        @return: Recognition results as XML string.
        """
        return self.getJavaClass().GetXml()

    def save(self, fullFileName : str, format : Format):
        """
        Saves the document in the plain text or other document format.
        @param fullFileName: Filename with a path for saving recognition result.
        @param format: Document format enum type of Format.
        """
        jTypeFormat = ModelsConverter.convertToJavaFormat(format)
        self.getJavaClass().save(fullFileName, jTypeFormat)

    def save_spell_check_corrected_text(self, fullFileName : str, format : Format, language : SpellCheckLanguage = SpellCheckLanguage.ENG):
        """
        Corrects text (replaces misspelled words).
        Saves the corrected text in the document in the plain text or other format.
        @param fullFileName: Filename with a path for saving recognition result
        @param format: Document format enum type of Format.
        @param language: Dictionary for spell check.
        """
        jTypeLang = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        jTypeFormat = ModelsConverter.convertToJavaFormat(format)
        self.getJavaClass().saveSpellCheckCorrectedText(fullFileName, jTypeFormat, jTypeLang)

    def get_spell_check_corrected_text(self, language : SpellCheckLanguage) -> str:
        """
        Corrects text (replaces misspelled words).
        @param language: Dictionary to use.
        @return: Corrected recognition results string.
        """
        jType = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        return self.getJavaClass().getSpellCheckCorrectedText(jType)

    def get_spell_check_error_list(self, language : SpellCheckLanguage = SpellCheckLanguage.ENG):
        """
        Find the misspelled words with suggested spellings for a given input text.
        @param language: Dictionary to use.
        @return: List of SpellCheckError object representing misspelled words with lists suggested correct spellings for the each misspelled word,
        and with the edit distance.
        """
        jType = ModelsConverter.convertToJavaSpellCheckLanguage(language)
        list = self.getJavaClass().getSpellCheckErrorList(jType)
        pythonList = []
        for elem in list:
            pythonList.append(SpellCheckError(elem))
        return pythonList

    def use_user_dictionary(self, dictionaryPath : str):
        """
        Allows to use own dictionary for spell-check correction.
        @param dictionaryPath: Full path to the user dictionary (frequency dictionary).
        Dictionary file format:
        Plain text file in UTF-8 encoding.
        Word and Word Frequency are separated by comma, the word is expected in the first column and the frequency in the second column.
        Every word-frequency-pair in a separate line.A line is defined as a sequence of characters followed by a line feed ("\n"), a carriage return ("\r"),
        or a carriage return immediately followed by a line feed("\r\n").
        Every word is expected to be in lower case.
        Example:
        \code
            word,5984819
            hello,5761742
            down,5582768
        \endcode
        """
        self.getJavaClass().useUserDictionary(dictionaryPath)

    @staticmethod
    def save_multipage_document(self, fullPath : str):
        """
        Private
        """
        self.getJavaClass().add(fullPath)


class SkewOutput(helper.BaseJavaClass):
    """
    Data about skew angle in degrees and name of the file.
    \code
        source - The full path to the file or URL, if any. Empty for streams, byte arrays, base64.
        page - Page number.
        image_index - Sequence number of the image on the page.
        angle - Skew angle in degrees.
    \endcode
    """
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.source = self.getJavaClass().Source
        """
        The full path to the file or URL, if any. Empty for streams, byte arrays, base64.
        """
        self.angle = self.getJavaClass().Angle
        """
        Skew angle in degrees.
        """
        self.page = self.getJavaClass().Page
        """
        Page number.
        """
        self.image_index = self.getJavaClass().ImageIndex
        """
        Sequence number of the image on the page.
        """

class RectangleOutput(helper.BaseJavaClass):
    """
    Data about detected text areas or lines.
    \code
        source - The full path to the file or URL, if any. Empty for streams, byte arrays, base64.
        page - Page number.
        image_index - Sequence number of the image on the page.
        rectangles - List of detected text areas or lines.
    \endcode
    """
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.source = self.getJavaClass().Source
        """
        The full path to the file or URL, if any. Empty for streams, byte arrays, base64.
        """
        self.rectangles = []
        """
        List of detected text areas or lines.
        """
        for rect in self.getJavaClass().Rectangles:
            self.rectangles.append(rect)
        self.page = self.getJavaClass().Page
        """
        Page number.
        """
        self.image_index = self.getJavaClass().ImageIndex
        """
        Sequence number of the image on the page.
        """


