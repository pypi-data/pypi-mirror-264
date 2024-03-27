from enum import Enum
import jpype

import aspose.models
from aspose import helper


class PreprocessingFilter(helper.BaseJavaClass):
    """
    Base class for image processing commands.
    """
    JAVA_CLASS_NAME = "com.aspose.ocr.PreprocessingFilter"
    def __init__(self):
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        self.__javaClass = asposeClass()
        self.__javaClassName = ""

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def getJavaClass(self):
        return self.__javaClass

    @staticmethod
    def binarize():
        """
        Converts an image to black-and-white image.
        Binary images are images whose pixels have only two possible intensity values.
        They are normally displayed as black and white. Numerically, the two values are often 0 for black, and 255 for white.
        Binary images are produced by auto thresholding an image.
        @return: BinarizeFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Binarize()

    @staticmethod
    def resize(width : int, height : int):
        """
        Rescale image - upscale or downscale image resolution.
        @param width: The new width of the image.
        @param height: The new height of the image.
        @return: ResizeFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Resize(width, height)

    @staticmethod
    def binarize_and_dilate():
        """
        Dilation adds pixels to the boundaries of objects in an image.
        @return: DilateFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.BinarizeAndDilate()

    @staticmethod
    def invert():
        """
        Automatically inverts colors in a document image.
        @return: InvertFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Invert()

    @staticmethod
    def rotate(angle : float):
        """
        Rotate original image.
        @param angle: Angle of rotation. Value from -360 to 360.
        @return: RotateFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Rotate(angle)

    @staticmethod
    def scale(ratio : float):
        """
        Rescale image - Upscale or downscale image resolution.
        InterpolationFilterType bilinear or nearest neighbor.
        @param ratio: The scaling factor. Recommended value from 0.1 to 1 to shrink. From 1 to 10 to enlarge.
        @return: ScaleFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Scale(ratio)

    @staticmethod
    def to_grayscale():
        """
        Converts an image to grayscale image.
        Grayscale image have 256 level of light in image (0 to 255).
        @return: GrayscaleFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.ToGrayscale()

    @staticmethod
    def threshold(value : int):
        """
        Create a binary image based on setting a threshold value on the pixel intensity of the original image.
        @param value: The max value.
        @return: BinarizeFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Threshold(value)

    @staticmethod
    def median():
        """
        The median filter run through each element of the image and replace each pixel with the median of its neighboring pixels.
        @return: MedianFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.Median()

    @staticmethod
    def auto_denoising():
        """
        Enables the use of an additional neural network to improve the image - reduce noise.
        Useful for images with scan artifacts, distortion, spots, flares, gradients, foreign elements.
        @return: AutoDenoisingFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.AutoDenoising()

    @staticmethod
    def auto_dewarping():
        """
        Automatically corrects geometric distortions in the image.
        Extremely resource intensive!
        @return: AutoDewarpingFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.AutoDewarping()

    @staticmethod
    def auto_skew():
        """
        Enables the automatic image skew correction.
        @return: AutoSkewFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.AutoSkew()

    @staticmethod
    def contrast_correction():
        """
        Contrast correction filter.
        @return: ContrastCorrectionFilter object.
        """
        asposeClass = jpype.JClass(PreprocessingFilter.JAVA_CLASS_NAME)
        javaClass = asposeClass()
        return javaClass.ContrastCorrection()

    def add(self, filter):
        """
        Add filter to collection for further preprocessing.
        @param filter: PreprocessingFilter object.
        """
        self.getJavaClass().add(filter)



class InputType(Enum):
    """
    Types of image/ documents for processing / recognition.
    """
    SINGLE_IMAGE = 0
    """ Supports GIF, PNG, JPEG, BMP, TIFF, JFIF, binary array."""
    PDF = 1
    """ Scanned PDF document from file or from bynary array."""
    TIFF = 2
    """ Multipage TIFF, TIF document from file or from InputStream."""
    URL = 3
    """ Link on the image. Supports GIF, PNG, JPEG, BMP, TIFF."""
    DIRECTORY = 4
    """ Path to the directory. Nested archives and folders are not supported.
        Supports GIF, PNG, JPEG, BMP, TIFF.
        Default amount of processed images is all."""
    ZIP = 5
    """ Full name of the ZIP archive. Nested archives and folders are not supported.
        Supports GIF, PNG, JPEG, BMP, TIFF, JFIF.
        Default amount of processed images is all."""
    BASE64 = 6
    """ base64 string with the image or path to the .txt file with the base64 content. Supports GIF, PNG, JPEG, BMP, TIFF."""



class ImageData(helper.BaseJavaClass):
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.source = str(self.getJavaClass().Source);
        self.type = self.getJavaClass().Type;
        self.width = self.getJavaClass().Width;
        self.height = self.getJavaClass().Height;
        self.filters = self.getJavaClass().Filters;
        self.image = self.getJavaClass().Image;

class OcrInput():
    """
    Main class to collect images.
    """
    __JAVA_CLASS_NAME = "com.aspose.ocr.OcrInput"

    def __init__(self, type : InputType, filters : PreprocessingFilter = None):
        """
        Constructor to create container and set the type of images / documents and filters for further processing / recognition.
        @param type: Set the images/documents type will be added to container.
        @param filters: Set processing filters will be applied for further processing or recognition.
        """
        asposeClass = jpype.JClass(OcrInput.__JAVA_CLASS_NAME)
        jType = ModelsConverter.convertInputTypeToJava(type)
        if filters == None:
            self.__javaClass = asposeClass(jType)
        else:
            self.__javaClass = asposeClass(jType, filters.getJavaClass())
        self.__javaClassName = ""
        self.__stream = []
        self.type = type

        if self.__javaClassName == None or self.__javaClassName == "":
            self.__javaClassName = str(self.__javaClass.getClass().getName())

    def init(self, javaClass):
        self.__javaClass = javaClass

        self.source = self.__javaClass.get(0).Source


    def add(self, fullPath : str, startPage : int = None, pagesNumber: int = None):
        """
        Add the path or URI containing the image for recognition / processing.
        The type of the image must correspond to the type specified in the constructor.
        @param fullPath: Path to the image/ document / folder / archive.
        @param startPage: The first page/image for processing / recognition. Use for documents, zip, folders.
        @param pagesNumber: The total amount of pages/images for processing / recognition. Use for documents, zip, folders. Default = all.
        """
        if startPage == None or pagesNumber == None:
            self.__javaClass.add(fullPath)
        else:
            self.__javaClass.add(fullPath, startPage, pagesNumber)
        # if self.__type != None:
        #     self.__type =


    def addStream(self, image_data_binary, startPage: int = None, pagesNumber: int = None):
        """
        Add the InputStream containing the image for recognition / processing.
        The type of the image must correspond to the type specified in the constructor.

        \code
             input = OcrInput(InputType.SINGLE_IMAGE)
            file = open(imgPath, "rb")
            image_data_binary = file.read()
            file.close()
            input.addStream(image_data_binary)
            result = api.recognize(input, RecognitionSettings())
        \endcode

        @param image_data_binary: containing the image or document.
        @param startPage: The first page/image for processing / recognition. Use for documents, zip, folders.
        @param pagesNumber: The total amount of pages/images for processing / recognition. Use for documents, zip, folders. Default = all.
        """
        stream = jpype.JClass('java.io.ByteArrayInputStream')
        streamJava = stream(image_data_binary)
        if startPage == None or pagesNumber == None:
            self.__javaClass.add(streamJava)
        else:
            self.__javaClass.add(streamJava, startPage, pagesNumber)

        self.__stream.append(image_data_binary)

    def add_base64(self, base64 : str):
        """
        Add the base64 string containing the image for recognition / processing.
        The type of the image must correspond to the type specified in the constructor.
        @param base64: Base64 string with single image.
        """
        self.__javaClass.addBase64(base64)

    def clear(self):
        """
        Set the amount of items for processing / recognition as 0.
        Clear the collection.
        """
        self.__javaClass.clear()

    def clear_filters(self):
        """
        Remove all filters.
        """
        self.__javaClass.clearFilters()

    def size(self):
        """
        Amount of items for processing / recognition.
        @return: Amount of items.
        """
        return self.__javaClass.size()

    def get(self, index : int) -> ImageData:
        """
        Returns information about processed / recognized image.
        @param index: Position of the image in the List.
        @return: The object of ImageData.
        """
        return ImageData(self.__javaClass.get(index))

    def getJavaClass(self):
        return self.__javaClass

class Format(Enum):
    """ Format to save recognition result as document. """
    TEXT = 0
    """ Saves the result in the plain text format. """
    DOCX = 1
    """ Saves the result as an Office Open XML Word processing ML Document (macro-free). """
    PDF = 2
    """ Saves the result as a PDF (Adobe Portable Document) Document. """
    XLSX = 3
    """ Saves the result as an Excel ( 2007 and later) workbook Document. """
    XML = 4
    """ Saves the result as an XML Document. """
    JSON = 5
    """ Saves the result as an plain text written in JavaScript object notation. """
    HTML = 6
    """ Saves the document as an HTML file. """
    EPUB = 7
    """ Saves the document as an EPUB file. """
    RTF = 8
    """ Saves the document as an rtf file. """
    PDF_NO_IMG = 9
    """ Saves the document as a Searchable PDF (Adobe Portable Document) Document without image. """


class SpellCheckLanguage(Enum):
    """ Dictionary language for spell-check correction. """
    ENG = 0
    """ English dictionary """
    DEU = 1
    """ German dictionary """
    SPA = 2
    """ Spanish dictionary """
    FRA = 3
    """ French dictionary """
    ITA = 4
    """ Italian dictionary """
    POR = 5
    """ Portuguese dictionary """
    CZE = 6
    """ Czech dictionary """
    DAN = 7
    """ Danish dictionary """
    DUM = 8
    """ Dutch dictionary """
    EST = 9
    """ Estonian dictionary """
    FIN = 10
    """ Finnish dictionary """
    LAV = 11
    """ Latvian dictionary """
    LIT = 12
    """ Lithuanian dictionary """
    POL = 13
    """ Polish dictionary """
    RUM = 14
    """ Romanian dictionary """
    SLK = 15
    """ Slovak dictionary """
    SLV = 16
    """ Slovene dictionary """
    SWE = 17
    """ Swedish dictionary """

class Language(Enum):
    """ Language model for the recognition. """
    
    EXT_LATIN = 0
    """ Multi - language(latin alphabet + diacritic) support """

    LATIN = 1
    """ Latin alphabet """

    CYRILLIC = 2
    """ Multi - language(cyrillic alphabet) support """

    ENG = 3
    """ English alphabet """

    DEU = 4
    """ German alphabet """

    POR = 5
    """ Portuguese alphabet """

    SPA = 6
    """ Spanish alphabet """

    FRA = 7
    """ French alphabet """

    ITA = 8
    """ Italian alphabet """

    # ---NEW - --

    CES = 9
    """ Czech alphabet """

    CZE = 10
    """ Czech alphabet (deprecated)
    Will be removed in the release 25.1.0. """


    DAN = 11
    """ Danish alphabet """

    DUM = 12
    """ Dutch alphabet (deprecated)
    Will be removed in the release 25.1.0. """


    NLD = 13
    """ Dutch alphabet """

    EST = 14
    """ Estonian alphabet """

    FIN = 15
    """ Finnish alphabet """

    LAV = 16
    """ Latvian alphabet """

    LIT = 17
    """ Lithuanian alphabet """

    NOR = 18
    """ Norwegian alphabet """

    POL = 19
    """ Polish alphabet """

    RUM = 20
    """ Romanian alphabet (deprecated)
    Will be removed in the release 25.1.0. """


    RON = 21
    """ Romanian alphabet """

    HBS = 22
    """ Serbo - Croatian alphabet """

    SLK = 23
    """ Slovak alphabet """

    SLV = 24
    """ Slovene alphabet """

    SWE = 25
    """ Swedish alphabet """

    CHI = 26
    """ Chinese alphabet (deprecated)
    Will be removed in the release 25.1.0. """


    BEL = 27
    """ Belorussian alphabet """

    BUL = 28
    """ Bulgarian alphabet """

    KAZ = 29
    """ Kazakh alphabet """

    RUS = 30
    """ Russian alphabet """

    SRP = 31
    """ Serbian alphabet """

    UKR = 32
    """ Ukrainian alphabet """

    HIN = 33
    """ Hindi alphabet """

    # / NEW in 2024

    CMN = 34
    """ Mandarin (Chinese) alphabet """

    IND = 35
    """ Indonesian alphabet """

    WUU = 36
    """ Changzhou alphabet """

    VIE = 37
    """ Vietnamese alphabet """

    MAR = 38
    """ Marathi alphabet """

    TUR = 39
    """ Turkish alphabet """

    YUE = 40
    """ Cantonese alphabet """

    NAN = 41
    """ Min Nan alphabet """

    MLY = 42
    """ Malay (Melayu) alphabet """

    HAU = 43
    """ Hausa alphabet """

    HSN = 44
    """ Xiang alphabet """

    SUN = 45
    """ Sundanese (Sunda) alphabet """

    SWH = 46
    """ Swahili alphabet """

    HAK = 47
    """ Hakka alphabet """

    BHO = 48
    """ Bhojpuri alphabet """

    MAI = 49
    """ Maithili alphabet """

    TGL = 50
    """ Tagalog (Pilipino) alphabet """

    YOR = 51
    """ Yoruba alphabet """

    GAX = 52
    """ Oromo alphabet """

    CEB = 53
    """ Cebuano alphabet """

    AWA = 54
    """ Awadhi alphabet """

    AZB = 55
    """ Azerbaijani (Azeri) alphabet """

    GAN = 56
    """ Gan alphabet """

    KMR = 57
    """ Kurdish (Kurmanji) alphabet """

    BOS = 58
    """ Bosnian alphabet """

    HRV = 59
    """ Croatian alphabet """

    BHR = 60
    """ Malagasy alphabet """

    NEP = 61
    """ Nepali alphabet """

    CCX = 62
    """ Zhuang alphabet """

    TUK = 63
    """ Turkmen alphabet """

    SOM = 64
    """ Somali alphabet """

    RWR = 65
    """ Marwari alphabet """

    MAG = 66
    """ Magahi alphabet """

    BGC = 67
    """ Haryanvi alphabet """

    HUN = 68
    """ Hungarian (Magyar) alphabet """

    HNE = 69
    """ Chattisgarhi (Laria, Khaltahi) alphabet """

    NYA = 70
    """ Chichewa (Chewa, Nyanja) alphabet """

    KIN = 71
    """ Rwanda alphabet """

    MNP = 72
    """ Min Bei alphabet """

    ZUL = 73
    """ Zulu alphabet """

    DHD = 74
    """ Dhundari alphabet """

    ILO = 75
    """ Ilocano alphabet """

    CDO = 76
    """ Min Dong alphabet """

    QXA = 77
    """ Quechua alphabet """

    HIL = 78
    """ Hiligaynon alphabet """

    HMN = 79
    """ Hmong alphabet """

    SNA = 80
    """ Shona (Karanga) alphabet """

    KNN = 81
    """ Konkani alphabet """

    XHO = 82
    """ Xhosa alphabet """

    BEW = 83
    """ Betawi alphabet """

    BJJ = 84
    """ Kanauji alphabet """

    ALN = 85
    """ Albanian alphabet """

    CAT = 86
    """ Catalan alphabet """

    AFR = 87
    """ Afrikaans alphabet """

    MIN = 88
    """ Minangkabau alphabet """

    SOT = 89
    """ Sotho (Southern) alphabet """

    BCL = 90
    """ Bikol alphabet """

    WTM = 91
    """ Mewati alphabet """

    VMW = 92
    """ Makua (Makhuwa) alphabet """

    KNC = 93
    """ Kanuri alphabet """

    TSN = 94
    """ Tswana alphabet """

    KON = 95
    """ Kikongo alphabet """

    LUO = 96
    """ Luo alphabet """

    SUK = 97
    """ Sukuma alphabet """

    TSO = 98
    """ Tsonga alphabet """

    BEM = 99
    """ Bemba (Chibemba) alphabet """

    KLN = 100
    """ Nandi alphabet """

    PLM = 101
    """ Palembang alphabet """

    UMB = 102
    """ Umbundu alphabet """

    NSO = 103
    """ Sotho (Northern) alphabet """

    WAR = 104
    """ Waray - Waray alphabet """

    RJB = 105
    """ Rajbanshi alphabet """

    GBM = 106
    """ Garhwali alphabet """

    LMN = 107
    """ Lamani (Lambadi) alphabet """

    NDS = 108
    """ Low German alphabet """

    GLK = 109
    """ Gilaki alphabet """

    MUI = 110
    """ Musi alphabet """

    CPX = 111
    """ Pu - Xian alphabet """

    PAM = 112
    """ Kapampangan alphabet """

    PCC = 113
    """ Bouyei (Buyi, Giáy) alphabet """

    KFY = 114
    """ Kumauni alphabet """

    GLG = 115
    """ Galician alphabet """

    NBL = 116
    """ Ndebele alphabet """

    YAO = 117
    """ Yao alphabet """

    SAS = 118
    """ Sasak alphabet """

    SSW = 119
    """ Swati (Swazi) alphabet """

    GUZ = 120
    """ Gusii alphabet """

    MER = 121
    """ Meru alphabet """

    WBR = 122
    """ Wagdi alphabet """

    WAL = 123
    """ Wolaytta alphabet """

    DOC = 124
    """ Dong alphabet """

    PAG = 125
    """ Pangasinan alphabet """

    DIQ = 126
    """ Dimli alphabet """

    MAK = 127
    """ Makassar (Makasar) alphabet """

    TUM = 128
    """ Tumbuka alphabet """

    SRR = 129
    """ Serer - Sine alphabet """

    LNC = 130
    """ Occitan alphabet """

    CHE = 131
    """ Chechen alphabet """

    TOI = 132
    """ Tonga alphabet """

    MTQ = 133
    """ Muong alphabet """

    QUC = 134
    """ K'iche' alphabet """

    MUP = 135
    """ Malvi alphabet """

    MTR = 136
    """ Mewari alphabet """

    KBD = 137
    """ Kabardian alphabet """

    RUF = 138
    """ Luguru alphabet """

    SRP_HRV = 139
    """ Serbo - Croatian alphabet (deprecated).  Will be removed in the release 25.1.0. """

    NONE = 140
    """ Multi - language(latin alphabet + diacritic) support
   (deprecated).  Will be removed in the release 25.1.0. """



class DetectAreasMode(Enum):
    """
    Determines the type of neural network used for areas detection.
    Used in the RecognitionSettings to specify which type of image you want to recognize.
    """
    NONE = 0
    """ Doesn't detect paragraphs.
    Better for a simple one-column document without pictures. """
    DOCUMENT = 1
    """ Detects paragraphs uses NN model for documents. 
    Better for multicolumn document, document with pictures or with other not text objects. """
    PHOTO = 2
    """ Detects paragraphs uses NN model for photos. 
    Better for image with a lot of pictures and other not text objects. """
    COMBINE = 3
    """ Detects paragraphs with text and then uses other NN model to detect areas inside of paragraphs.
    Better for images with complex structure. """
    TABLE = 4
    """ Detects cells with text.
    Preferable mode for images with table structure. """
    CURVED_TEXT = 5
    """ Detects lines and recognizes text on curved images.
    Preferred mode for photos of book and magazine pages. """
    TEXT_IN_WILD = 6
    """ A super-powerful neural network specialized in extracting words from low-quality images such as street photos, license plates, passport photos, meter photos, and photos with noisy backgrounds. """

class AreasType(Enum):
    """ Determines the type of regions detected by the model.
    Used in the get_text_areas to indicate which result will be obtained - paragraph coordinates or line coordinates.
    """
    PARAGRAPHS = 0
    """ Sets regions as paragraphs """
    LINES = 1
    """ Sets regions as lines """
    WORDS = 2
    """ Sets regions as words """



class SpellCheckError(helper.BaseJavaClass):
    """
    Representing misspelled word with additional data.
    """
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.suggested_words = []
        self.initParams()

    def initParams(self):
        self.word = self.getJavaClass().word
        """
        The word being misspelled.
        """
        self.start_position = self.getJavaClass().startPosition
        """
        Word's position in the input text.
        """
        self.length = self.getJavaClass().length
        """
        Misspelled word's length in the input text.
        """
        suggestion = self.getJavaClass().suggestedWords
        """
        list of objects with suggested correct spellings
        """
        for item in suggestion:
            self.suggested_words.append(SuggestedWord(item))


class SuggestedWord(helper.BaseJavaClass):
    """
    Spelling suggestion returned from get_spell_check_error_list.
    """
    def __init__(self, javaClass):
        super().__init__(javaClass)
        self.initParams()

    def initParams(self):
        self.word = self.getJavaClass().word
        """
        The suggested correctly spelled word.
        """
        self.distance = self.getJavaClass().distance
        """
        The distance between the searched and suggestion.
        """




class ModelsConverter:

    def convertToJavaAreasType(jType):
        return ModelsConverter.__switchAreasType(jType)

    def __switchAreasType(type):
        javaType = "com.aspose.ocr.AreasType"
        areastype = jpype.JClass(javaType)
        if type.name == "PARAGRAPHS":
            return areastype.PARAGRAPHS
        if type.name == "LINES":
            return areastype.LINES
        if type.name == "WORDS":
            return areastype.WORDS

    def convertToJavaSpellCheckLanguage(jType):
        return ModelsConverter.__switchSpellCheckLanguage(jType)

    def __switchSpellCheckLanguage(type):
        javaType = "com.aspose.ocr.SpellCheck.SpellCheckLanguage"
        language = jpype.JClass(javaType)
        if type.name == "ENG":
            return language.Eng
        elif type.name == "DEU":
            return language.Deu
        if type.name =="SPA":
            return language.Spa
        if type.name =="FRA":
            return language.Fra
        if type.name =="ITA":
            return language.Ita
        if type.name =="POR":
            return language.Por
        if type.name =="CZE":
            return language.Cze
        if type.name =="DAN":
            return language.Dan
        if type.name =="DUM":
            return language.Dum
        if type.name =="EST":
            return language.Est
        if type.name =="FIN":
            return language.Fin
        if type.name =="LAV":
            return language.Lav
        if type.name =="LIT":
            return language.Lit
        if type.name =="POL":
            return language.Pol
        if type.name =="RUM":
            return language.Rum
        if type.name =="SLK":
            return language.Slk
        if type.name =="SLV":
            return language.Slv
        if type.name =="SWE":
            return language.Swe

    def convertToJavaFormat(jType):
        return ModelsConverter.__switchFormat(jType)

    def __switchFormat(type):
        javaType = "com.aspose.ocr.Format"
        format = jpype.JClass(javaType)
        if type.name == "TEXT":
            return format.Text
        elif type.name == "DOCX":
            return format.Docx
        if type.name == "PDF":
                return format.Pdf
        if type.name == "XLSX":
                return format.Xlsx
        if type.name == "XML":
                return format.Xml
        if type.name == "JSON":
                return format.Json
        if type.name == "HTML":
                return format.Html
        if type.name == "EPUB":
                return format.Epub
        if type.name == "RTF":
                return format.Rtf
        if type.name == "PDF_NO_IMG":
                return format.PdfNoImg


    def convertInputTypeToJava(jType):
        return ModelsConverter.__switchInputType(jType)

    def __switchInputType(type):
        javaType = "com.aspose.ocr.InputType"
        inputType = jpype.JClass(javaType)
        if type.name == "SINGLE_IMAGE":
            return inputType.SingleImage
        elif type.name == "PDF":
            return inputType.PDF
        elif type.name == "TIFF":
            return inputType.TIFF
        elif type.name == "URL":
            return inputType.URL
        elif type.name == "DIRECTORY":
            return inputType.Directory
        elif type.name == "ZIP":
            return inputType.Zip
        elif type.name == "BASE64":
            return inputType.Base64



    def convertToJavaAreasMode(jType):
        return ModelsConverter.__switchAreasMode(jType)

    def __switchAreasMode(type):
        javaType = "com.aspose.ocr.DetectAreasMode"
        detectAreasMode = jpype.JClass(javaType)
        if type.name == "NONE":
            return detectAreasMode.NONE
        elif type.name == "DOCUMENT":
            return detectAreasMode.DOCUMENT
        elif type.name == "PHOTO":
            return detectAreasMode.PHOTO
        elif type.name == "COMBINE":
            return detectAreasMode.COMBINE
        elif type.name == "TABLE":
            return detectAreasMode.TABLE
        elif type.name == "CURVED_TEXT":
            return detectAreasMode.CURVED_TEXT
        elif type.name == "TEXT_IN_WILD":
            return detectAreasMode.TEXT_IN_WILD

    def convertToJavaLanguage(jType):
        return ModelsConverter.__switchLanguage(jType)

    def __switchLanguage(type):
        javaType = "com.aspose.ocr.Language"
        language = jpype.JClass(javaType)
        if type.name == "NONE":
            return language.Latin
        if type.name == "EXT_LATIN":
            return language.ExtLatin
        if type.name == "LATIN":
            return language.Latin
        if type.name == "CYRILLIC":
            return language.Cyrillic
        if type.name == "ENG":
            return language.Eng
        if type.name == "DEU":
            return language.Deu
        if type.name == "POR":
            return language.Por
        if type.name == "SPA":
            return language.Spa
        if type.name == "FRA":
            return language.Fra
        if type.name == "ITA":
            return language.Ita
        if type.name == "CES":
            return language.Ces
        if type.name == "CZE":
            return language.Cze
        if type.name == "DAN":
            return language.Dan
        if type.name == "DUM":
            return language.Dum
        if type.name == "NLD":
            return language.Nld
        if type.name == "EST":
            return language.Est
        if type.name == "FIN":
            return language.Fin
        if type.name == "LAV":
            return language.Lav
        if type.name == "LIT":
            return language.Lit
        if type.name == "NOR":
            return language.Nor
        if type.name == "POL":
            return language.Pol
        if type.name == "RUM":
            return language.Rum
        if type.name == "RON":
            return language.Ron
        if type.name == "HBS":
            return language.Hbs
        if type.name == "SLK":
            return language.Slk
        if type.name == "SLV":
            return language.Slv
        if type.name == "SWE":
            return language.Swe
        if type.name == "CHI":
            return language.Chi
        if type.name == "BEL":
            return language.Bel
        if type.name == "BUL":
            return language.Bul
        if type.name == "KAZ":
            return language.Kaz
        if type.name == "RUS":
            return language.Rus
        if type.name == "SRP":
            return language.Srp
        if type.name == "UKR":
            return language.Ukr
        if type.name == "HIN":
            return language.Hin
        if type.name == "CMN":
            return language.Cmn
        if type.name == "IND":
            return language.Ind
        if type.name == "WUU":
            return language.Wuu
        if type.name == "VIE":
            return language.Vie
        if type.name == "MAR":
            return language.Mar
        if type.name == "TUR":
            return language.Tur
        if type.name == "YUE":
            return language.Yue
        if type.name == "NAN":
            return language.Nan
        if type.name == "MLY":
            return language.Mly
        if type.name == "HAU":
            return language.Hau
        if type.name == "HSN":
            return language.Hsn
        if type.name == "SUN":
            return language.Sun
        if type.name == "SWH":
            return language.Swh
        if type.name == "HAK":
            return language.Hak
        if type.name == "BHO":
            return language.Bho
        if type.name == "MAI":
            return language.Mai
        if type.name == "TGL":
            return language.Tgl
        if type.name == "YOR":
            return language.Yor
        if type.name == "GAX":
            return language.Gax
        if type.name == "CEB":
            return language.Ceb
        if type.name == "AWA":
            return language.Awa
        if type.name == "AZB":
            return language.Azb
        if type.name == "GAN":
            return language.Gan
        if type.name == "KMR":
            return language.Kmr
        if type.name == "BOS":
            return language.Bos
        if type.name == "HRV":
            return language.Hrv
        if type.name == "BHR":
            return language.Bhr
        if type.name == "NEP":
            return language.Nep
        if type.name == "CCX":
            return language.Ccx
        if type.name == "TUK":
            return language.Tuk
        if type.name == "SOM":
            return language.Som
        if type.name == "RWR":
            return language.Rwr
        if type.name == "MAG":
            return language.Mag
        if type.name == "BGC":
            return language.Bgc
        if type.name == "HUN":
            return language.Hun
        if type.name == "HNE":
            return language.Hne
        if type.name == "NYA":
            return language.Nya
        if type.name == "KIN":
            return language.Kin
        if type.name == "MNP":
            return language.Mnp
        if type.name == "ZUL":
            return language.Zul
        if type.name == "DHD":
            return language.Dhd
        if type.name == "ILO":
            return language.Ilo
        if type.name == "CDO":
            return language.Cdo
        if type.name == "QXA":
            return language.Qxa
        if type.name == "HIL":
            return language.Hil
        if type.name == "HMN":
            return language.Hmn
        if type.name == "SNA":
            return language.Sna
        if type.name == "KNN":
            return language.Knn
        if type.name == "XHO":
            return language.Xho
        if type.name == "BEW":
            return language.Bew
        if type.name == "BJJ":
            return language.Bjj
        if type.name == "ALN":
            return language.Aln
        if type.name == "CAT":
            return language.Cat
        if type.name == "AFR":
            return language.Afr
        if type.name == "MIN":
            return language.Min
        if type.name == "SOT":
            return language.Sot
        if type.name == "BCL":
            return language.Bcl
        if type.name == "WTM":
            return language.Wtm
        if type.name == "VMW":
            return language.Vmw
        if type.name == "KNC":
            return language.Knc
        if type.name == "TSN":
            return language.Tsn
        if type.name == "KON":
            return language.Kon
        if type.name == "LUO":
            return language.Luo
        if type.name == "SUK":
            return language.Suk
        if type.name == "TSO":
            return language.Tso
        if type.name == "BEM":
            return language.Bem
        if type.name == "KLN":
            return language.Kln
        if type.name == "PLM":
            return language.Plm
        if type.name == "UMB":
            return language.Umb
        if type.name == "NSO":
            return language.Nso
        if type.name == "WAR":
            return language.War
        if type.name == "RJB":
            return language.Rjb
        if type.name == "GBM":
            return language.Gbm
        if type.name == "LMN":
            return language.Lmn
        if type.name == "NDS":
            return language.Nds
        if type.name == "GLK":
            return language.Glk
        if type.name == "MUI":
            return language.Mui
        if type.name == "CPX":
            return language.Cpx
        if type.name == "PAM":
            return language.Pam
        if type.name == "PCC":
            return language.Pcc
        if type.name == "KFY":
            return language.Kfy
        if type.name == "GLG":
            return language.Glg
        if type.name == "NBL":
            return language.Nbl
        if type.name == "YAO":
            return language.Yao
        if type.name == "SAS":
            return language.Sas
        if type.name == "SSW":
            return language.Ssw
        if type.name == "GUZ":
            return language.Guz
        if type.name == "MER":
            return language.Mer
        if type.name == "WBR":
            return language.Wbr
        if type.name == "WAL":
            return language.Wal
        if type.name == "DOC":
            return language.Doc
        if type.name == "PAG":
            return language.Pag
        if type.name == "DIQ":
            return language.Diq
        if type.name == "MAK":
            return language.Mak
        if type.name == "TUM":
            return language.Tum
        if type.name == "SRR":
            return language.Srr
        if type.name == "LNC":
            return language.Lnc
        if type.name == "CHE":
            return language.Che
        if type.name == "TOI":
            return language.Toi
        if type.name == "MTQ":
            return language.Mtq
        if type.name == "QUC":
            return language.Quc
        if type.name == "MUP":
            return language.Mup
        if type.name == "MTR":
            return language.Mtr
        if type.name == "KBD":
            return language.Kbd
        if type.name == "RUF":
            return language.Ruf
        if type.name == "SRP_HRV":
            return language.Srp_hrv
        if type.name == "NONE":
            return language.Latin