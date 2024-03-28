import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_ContextClick(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_ContextClick")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "MultiAction_ContextClick was successful", "MultiAction_ContextClick failed")
