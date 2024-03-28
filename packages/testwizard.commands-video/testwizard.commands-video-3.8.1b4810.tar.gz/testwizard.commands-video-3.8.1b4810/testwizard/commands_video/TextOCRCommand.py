import sys
import json

from testwizard.commands_core import CommandBase
from .TextOCRResult import TextOCRResult


class TextOCRCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "TextOCR")

    def execute(self, dictionary):
        requestObj = [dictionary]

        result = self.executeCommand(requestObj)

        return TextOCRResult(result, "TextOCR was successful", "TextOCR failed")
