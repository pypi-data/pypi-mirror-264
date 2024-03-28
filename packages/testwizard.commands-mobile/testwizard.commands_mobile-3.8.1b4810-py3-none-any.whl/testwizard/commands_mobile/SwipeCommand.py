import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class SwipeCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.Swipe")

    def execute(self, startX, startY, endX, endY, duration):
        requestObj = [startX, startY, endX, endY, duration]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "Swipe was successful", "Swipe failed")
