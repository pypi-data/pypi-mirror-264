import sys
import json

from testwizard.commands_core import CommandBase
from .FindPatternResult import FindPatternResult

class FindPatternCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "FindPattern")
    
    def execute(self, filename, mode):
        requestObj = [filename, mode]

        result = self.executeCommand(requestObj)        

        return FindPatternResult(result, "FindPattern was successful", "FindPattern failed")   