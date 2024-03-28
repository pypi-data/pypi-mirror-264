import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult

class MultiAction_ClickAndHold(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.MultiAction_ClickAndHold")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result,"MultiAction_ClickAndHold was successful", "MultiAction_ClickAndHold failed")