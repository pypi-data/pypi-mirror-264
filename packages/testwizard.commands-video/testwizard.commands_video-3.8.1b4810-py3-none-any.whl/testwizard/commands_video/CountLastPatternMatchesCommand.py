import sys
import json

from testwizard.commands_core import CommandBase
from .CountLastPatternMatchesResult import CountLastPatternMatchesResult


class CountLastPatternMatchesCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "CountLastPatternMatches")

    def execute(self, similarity):
        requestObj = [similarity]

        result = self.executeCommand(requestObj)

        return CountLastPatternMatchesResult(result, "CountLastPatternMatches was successful", "CountLastPatternMatches failed")
