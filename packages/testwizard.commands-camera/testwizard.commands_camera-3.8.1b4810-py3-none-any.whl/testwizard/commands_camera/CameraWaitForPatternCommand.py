import sys
import json

from testwizard.commands_core import CommandBase
from .CameraWaitForSampleResult import CameraWaitForSampleResult


class CameraWaitForPatternCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Camera.WaitForPattern")

    def execute(self, filePath, x, y, width, height, timeout, distanceThreshold):
        if distanceThreshold is None:
            requestObj = [filePath, x, y, width, height, timeout]
        else:
            requestObj = [filePath, x, y, width, height, timeout, distanceThreshold]

        result = self.executeCommand(requestObj)

        return CameraWaitForSampleResult(result, "WaitForPattern was successful", "WaitForPattern failed")
