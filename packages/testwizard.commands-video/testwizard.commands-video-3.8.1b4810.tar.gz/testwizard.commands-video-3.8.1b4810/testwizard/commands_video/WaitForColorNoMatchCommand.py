import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForColorResult import WaitForColorResult


class WaitForColorNoMatchCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForColorNoMatch")

    def execute(self, x, y, width, height, refColor, tolerance, minSimilarity, timeout):
        requestObj = [x, y, width, height, refColor,
                      tolerance, minSimilarity, timeout]

        result = self.executeCommand(requestObj)

        return WaitForColorResult(result, "WaitForColorNoMatch was successful", "WaitForColorNoMatch failed")
