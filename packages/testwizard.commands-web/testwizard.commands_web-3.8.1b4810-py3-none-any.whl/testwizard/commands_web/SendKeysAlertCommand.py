import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class SendKeysAlert(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.SendKeysAlert")

    def execute(self, text):
        requestObj = [text]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "SendKeysAlert was successful", "SendKeysAlert failed")
