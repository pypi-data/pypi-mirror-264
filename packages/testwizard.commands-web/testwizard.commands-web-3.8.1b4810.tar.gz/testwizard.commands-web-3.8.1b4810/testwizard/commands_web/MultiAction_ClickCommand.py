import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_Click(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_Click")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "MultiAction_Click was successful", "MultiAction_Click failed")
