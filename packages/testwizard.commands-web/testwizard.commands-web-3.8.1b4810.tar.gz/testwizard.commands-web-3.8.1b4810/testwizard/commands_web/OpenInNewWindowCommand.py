from testwizard.commands_core import CommandBase
from .OpenInNewWindowResult import OpenInNewWindowResult


class OpenInNewWindow(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.OpenInNewWindow")

    def execute(self, selector):
        requestObj = [selector]

        result = self.executeCommand(requestObj)

        return OpenInNewWindowResult(result, "OpenInNewWindow was successful", "OpenInNewWindow failed")
