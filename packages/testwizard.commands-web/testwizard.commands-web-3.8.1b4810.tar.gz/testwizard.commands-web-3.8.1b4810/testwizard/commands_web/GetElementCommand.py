import sys
import json

from testwizard.commands_core import CommandBase
from .GetElementResult import GetElementResult


class GetElement(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.GetElement")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return GetElementResult(result, "GetElement was successful", "GetElement failed")
