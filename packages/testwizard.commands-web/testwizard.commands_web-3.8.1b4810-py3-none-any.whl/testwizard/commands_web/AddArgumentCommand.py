import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.SimpleResult import SimpleResult


class AddArgumentCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.AddArgument")

    def execute(self, argument):
        requestObj = [argument]

        result = self.executeCommand(requestObj)

        return SimpleResult(result, "AddArgument was successful", "AddArgument failed")
