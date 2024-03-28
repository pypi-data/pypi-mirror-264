import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class SendKeys(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.SendKeys")

    def execute(self, selector, text):
        requestObj = [selector, text]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "SendKeys was successful", "SendKeys failed")
