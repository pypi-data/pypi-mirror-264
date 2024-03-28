import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class MultiAction_MoveToElementOffset(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_MoveToElementOffset")

    def execute(self, selector, xOffset, yOffset):
        requestObj = [selector, xOffset, yOffset]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "MultiAction_MoveToElementOffset was successful", "MultiAction_MoveToElementOffset failed")
