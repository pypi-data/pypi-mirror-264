import sys
import json
from testwizard.commands_core import SessionCommandBase
from testwizard.commands_core import OkErrorCodeAndMessageResult

class AddCustomDataCommand(SessionCommandBase):
    def __init__(self, session):
        SessionCommandBase.__init__(self, session, "AddCustomData")

    def execute(self, key, value):
        requestObj = [key, value]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "AddCustomData was successful", "AddCustomData failed")                