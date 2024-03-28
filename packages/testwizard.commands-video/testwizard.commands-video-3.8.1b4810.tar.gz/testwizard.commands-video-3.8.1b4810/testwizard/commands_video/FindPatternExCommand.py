import sys
import json

from testwizard.commands_core import CommandBase
from .FindPatternResult import FindPatternResult

class FindPatternExCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FindPatternEx")

    def execute(self, filename, mode, x, y, width, height):
        requestObj = [filename, mode, x, y, width, height]

        result = self.executeCommand(requestObj)

        return FindPatternResult(result, "FindPatternEx was successful", "FindPatternEx failed")