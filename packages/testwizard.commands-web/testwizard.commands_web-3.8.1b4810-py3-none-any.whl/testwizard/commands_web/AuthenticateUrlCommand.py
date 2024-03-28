import sys
import json

from testwizard.commands_core import CommandBase
from testwizard.commands_core.OkErrorCodeAndMessageResult import OkErrorCodeAndMessageResult


class AuthenticateUrl(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Selenium.AuthenticateUrl")

    def execute(self, username, password, link):
        requestObj = [username, password, link]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "AuthenticateUrl was successful", "AuthenticateUrl failed")
