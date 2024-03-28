import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForPatternResult import WaitForPatternResult


class WaitForPatternNoMatchCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForPatternNoMatch")

    def execute(self, filename, minSimilarity, timeout, mode, x, y, width, height):
        requestObj = [filename, minSimilarity,
                      timeout, mode, x, y, width, height]

        result = self.executeCommand(requestObj)

        return WaitForPatternResult(result, "WaitForPatternNoMatch was successful", "WaitForPatternNoMatch failed")
