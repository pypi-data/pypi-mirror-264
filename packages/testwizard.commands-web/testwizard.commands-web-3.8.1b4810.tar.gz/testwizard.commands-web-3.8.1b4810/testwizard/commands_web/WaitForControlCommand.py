import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class WaitForControl(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.WaitForControl")

    def execute(self, selector, seconds):
        requestObj = [selector, seconds]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "WaitForControl was successful", "WaitForControl failed")
