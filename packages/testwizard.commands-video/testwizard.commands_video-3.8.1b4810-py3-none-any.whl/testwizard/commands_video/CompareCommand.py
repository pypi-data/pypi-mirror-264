import sys
import json

from testwizard.commands_core import CommandBase
from .CompareResult import CompareResult


class CompareCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Compare")

    def execute(self, x, y, width, height, filename, tolerance):
        requestObj = [x, y, width, height, filename, tolerance]

        result = self.executeCommand(requestObj)

        return CompareResult(result, "compare was successful", "compare failed")
