import sys
import json

from testwizard.commands_core import CommandBase
from .GetElementsResult import GetElementsResult


class GetElementsCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.GetElements")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return GetElementsResult(result, "GetElements was successful", "GetElements failed")
