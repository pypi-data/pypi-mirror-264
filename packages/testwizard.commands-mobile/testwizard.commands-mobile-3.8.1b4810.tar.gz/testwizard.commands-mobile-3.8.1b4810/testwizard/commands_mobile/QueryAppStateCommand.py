
import sys
import json

from testwizard.commands_core import CommandBase
from .QueryAppStateResult import QueryAppStateResult


class QueryAppStateCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Mobile.QueryAppState")

    def execute(self, bundleId):
        if bundleId is None:
            requestObj = []
        else:
            requestObj = [bundleId]

        result = self.executeCommand(requestObj)

        return QueryAppStateResult(result, "QueryAppState was successful", "QueryAppState failed")
