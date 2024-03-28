import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class ZoomCoordinatesCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.ZoomCoordinates")

    def execute(self, x, y, length):
        requestObj = [x, y, length]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "ZoomCoordinates was successful", "ZoomCoordinates failed")
