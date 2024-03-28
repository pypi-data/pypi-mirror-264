import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class AddCapabilityCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.AddCapability")

    def execute(self, key, value):
        requestObj = [key, value]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "AddCapability was successful", "AddCapability failed")
