import sys
import json

from testwizard.commands_core import CommandBase
from .FilterResult import FilterResult


class SetRegionCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "SetRegion")

    def execute(self, x, y, width, height):
        requestObj = [x, y, width, height]

        result = self.executeCommand(requestObj)

        return FilterResult(result, "SetRegion was successful", "SetRegion failed")
