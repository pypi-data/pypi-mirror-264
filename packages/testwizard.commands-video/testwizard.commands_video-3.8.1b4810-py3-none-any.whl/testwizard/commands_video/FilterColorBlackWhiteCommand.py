import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class FilterColorBlackWhiteCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FilterColorBlackWhite")

    def execute(self, color, tolerance):
        requestObj = [color, tolerance]

        result = self.executeCommand(requestObj)

        return FilterResult(result, "FilterColorBlackWhite was successful", "FilterColorBlackWhite failed")
