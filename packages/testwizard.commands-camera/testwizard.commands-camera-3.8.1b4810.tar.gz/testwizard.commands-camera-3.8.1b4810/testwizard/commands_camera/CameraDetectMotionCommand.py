import sys
import json

from testwizard.commands_core import CommandBase
from .CameraDetectMotionResult import CameraDetectMotionResult


class CameraDetectMotionCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Camera.DetectMotion")
    
    def execute(self, x, y, width, height, duration, distanceThreshold):
        if distanceThreshold is None:
            requestObj = [x, y, width, height, duration]
        else:
            requestObj = [x, y, width, height, duration, distanceThreshold]

        result = self.executeCommand(requestObj)

        return CameraDetectMotionResult(result, "CameraDetectMotion was successful", "CameraDetectMotion failed")