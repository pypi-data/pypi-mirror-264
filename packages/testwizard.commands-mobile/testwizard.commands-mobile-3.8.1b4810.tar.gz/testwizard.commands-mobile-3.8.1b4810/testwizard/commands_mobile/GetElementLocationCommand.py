import sys
import json

from testwizard.commands_core import CommandBase
from .GetElementLocationResult import GetElementLocationResult


class GetElementLocationCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject,
                             "Mobile.GetElementLocation")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return GetElementLocationResult(result, "GetElementLocation was successful", "GetElementLocation failed")
