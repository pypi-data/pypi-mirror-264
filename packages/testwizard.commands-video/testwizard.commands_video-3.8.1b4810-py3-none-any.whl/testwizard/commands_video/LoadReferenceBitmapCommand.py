import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class LoadReferenceBitmapCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "LoadReferenceBitmap")

    def execute(self, filename):
        requestObj = [filename]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "LoadReferenceBitmap was successful", "LoadReferenceBitmap failed")
