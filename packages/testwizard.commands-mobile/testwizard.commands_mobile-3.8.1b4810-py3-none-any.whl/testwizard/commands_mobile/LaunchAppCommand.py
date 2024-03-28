
import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class LaunchAppCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.LaunchApp")

    def execute(self, appId, activityId):
        requestObj = []
        if appId is None:
            requestObj.append(None)
        else:
            requestObj.append(appId)

        if activityId is not None:
            requestObj.append(activityId)

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "LaunchApp was successful", "LaunchApp failed")
