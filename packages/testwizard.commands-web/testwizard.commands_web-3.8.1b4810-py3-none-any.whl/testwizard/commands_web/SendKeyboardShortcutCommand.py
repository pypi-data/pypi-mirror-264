import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class SendKeyboardShortcut(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.SendKeyboardShortcut")

    def execute(self, selector, keys):
        requestObj = [selector, keys]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "SendKeyboardShortcut was successful", "SendKeyboardShortcut failed")
