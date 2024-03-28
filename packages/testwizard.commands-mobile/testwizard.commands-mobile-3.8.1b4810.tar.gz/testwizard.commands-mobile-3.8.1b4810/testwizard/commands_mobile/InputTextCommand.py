import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class InputTextCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.InputText")

    def execute(self, selector, text):
        requestObj = [selector, text]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "InputText was successful", "InputText failed")
