import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class SwipeArcCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.SwipeArc")

    def execute(self, centerX, centerY, radius, startDegree, degrees, steps):
        requestObj = [centerX, centerY, radius, startDegree, degrees, steps]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "SwipeArc was successful", "SwipeArc failed")
