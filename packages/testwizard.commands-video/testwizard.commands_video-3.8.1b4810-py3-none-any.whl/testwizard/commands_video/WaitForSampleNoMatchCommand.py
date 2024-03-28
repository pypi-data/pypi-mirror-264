import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForSampleResult import WaitForSampleResult


class WaitForSampleNoMatchCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForSampleNoMatch")

    def execute(self, x, y, width, height, minSimilarity, timeout, tolerance, distanceMethod, maxDistance):
        requestObj = [x, y, width, height, minSimilarity, timeout]
        if tolerance is not None:
            requestObj.append(tolerance)
        if distanceMethod is not None:
            requestObj.append(distanceMethod)
            if maxDistance is not None:
                requestObj.append(maxDistance)

        result = self.executeCommand(requestObj)

        return WaitForSampleResult(result, "WaitForSampleNoMatch was successful", "WaitForSampleNoMatch failed")
