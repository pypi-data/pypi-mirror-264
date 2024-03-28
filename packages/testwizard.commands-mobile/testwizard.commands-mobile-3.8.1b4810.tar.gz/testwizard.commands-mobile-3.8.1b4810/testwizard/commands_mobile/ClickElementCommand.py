import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class ClickElementCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.ClickElement")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "ClickElement was successful", "ClickElement failed")
