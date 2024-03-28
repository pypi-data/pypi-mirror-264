
import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class ActivateAppCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.ActivateApp")

    def execute(self, bundleId):
        if bundleId is None:
            requestObj = []
        else:
            requestObj = [bundleId]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "ActivateApp was successful", "ActivateApp failed")
