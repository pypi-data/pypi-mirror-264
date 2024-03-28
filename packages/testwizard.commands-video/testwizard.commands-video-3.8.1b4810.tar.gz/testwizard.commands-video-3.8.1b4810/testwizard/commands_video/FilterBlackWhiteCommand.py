import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class FilterBlackWhiteCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FilterBlackWhite")

    def execute(self, separation):
        requestObj = [separation]

        result = self.executeCommand(requestObj)

        return FilterResult(result, "FilterBlackWhite was successful", "FilterBlackWhite failed")
