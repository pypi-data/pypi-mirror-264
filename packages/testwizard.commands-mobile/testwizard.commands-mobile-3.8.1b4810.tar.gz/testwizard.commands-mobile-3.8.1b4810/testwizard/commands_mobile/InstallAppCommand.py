
import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class InstallAppCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.InstallApp")

    def execute(self, ipaPath):
        requestObj = [ipaPath]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "InstallApp was successful", "InstallApp failed")
