
import sys
import json

from testwizard.commands_core import CommandBase
from .IsAppInstalledResult import IsAppInstalledResult


class IsAppInstalledCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.IsAppInstalled")

    def execute(self, bundleId):
        if bundleId is None:
            requestObj = []
        else:
            requestObj = [bundleId]

        result = self.executeCommand(requestObj)

        return IsAppInstalledResult(result, "IsAppInstalled was successful", "IsAppInstalled failed")
