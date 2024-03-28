import sys
import json

from testwizard.commands_core import CommandBase
from .GetChildrenResult import GetChildrenResult


class GetChildren(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.GetChildren")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return GetChildrenResult(result, "GetChildren was successful", "GetChildren failed")
