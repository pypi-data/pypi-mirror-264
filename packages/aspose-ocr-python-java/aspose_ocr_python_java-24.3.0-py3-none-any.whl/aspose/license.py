import jpype
from . import helper

class License(helper.BaseJavaClass):
    javaClassName = "com.aspose.ocr.License"

    def __init__(self):
        javaLicense = jpype.JClass(self.javaClassName)
        self.javaClass = javaLicense()
        super().__init__(self.javaClass)

    def set_license(self, filePath):
        """
        Licenses the component.
        @:param: filePath:  Can be a full or short file name. Use an empty string to switch to evaluation mode.
        """
        self.getJavaClass().setLicense(filePath)

    def is_licensed(self):
        javaClass = self.getJavaClass()
        is_licensed = javaClass.isLicensed()
        return str(is_licensed) == "true"


    @staticmethod
    def openFile(filename):
        file = open(filename, "rb")
        image_data_binary = file.read()
        file.close()
        array = []
        array.append('')
        i = 0
        while (i < len(image_data_binary)):
            array.append(str(image_data_binary[i]))
            i += 1
        return array

    def init(self):
        return

