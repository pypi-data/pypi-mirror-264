import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class PinchCoordinatesCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.PinchCoordinates")

    def execute(self, x, y, length):
        requestObj = [x, y, length]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "PinchCoordinates was successful", "PinchCoordinates failed")
