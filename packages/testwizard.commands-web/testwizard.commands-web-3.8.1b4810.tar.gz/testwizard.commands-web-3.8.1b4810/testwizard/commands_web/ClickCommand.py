import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class Click(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.Click")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "Click was successful", "Click failed")
