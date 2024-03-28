import sys
import json

from testwizard.commands_core import CommandBase
from .FindAllPatternLocationsResult import FindAllPatternLocationsResult

class FindAllPatternLocationsExCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FindAllPatternLocationsEx")

    def execute(self, filename, mode, similarity, x, y, width, height):
        requestObj = [filename, mode, similarity, x, y, width, height]

        result = self.executeCommand(requestObj)

        return FindAllPatternLocationsResult(result, "FindAllPatternLocationsEx was successful", "FindAllPatternLocationsEx failed")