import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class OpenInNewTab(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.OpenInNewTab")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "OpenInNewTab was successful", "OpenInNewTab failed")
