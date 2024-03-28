import sys
import json

from testwizard.commands_core import CommandBase
from .SendNotificationResult import SendNotificationResult


class SendNotificationCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "Services.SendNotification")

    def execute(self, errorId, description, priority):
        requestObj = [errorId, description, priority]

        result = self.executeCommand(requestObj)

        return SendNotificationResult(result, "SendNotification was successful", "SendNotification failed")
