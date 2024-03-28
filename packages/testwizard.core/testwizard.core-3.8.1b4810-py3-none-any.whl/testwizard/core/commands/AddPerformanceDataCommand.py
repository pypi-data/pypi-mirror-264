import sys
import json
from testwizard.commands_core import SessionCommandBase
from testwizard.commands_core import OkErrorCodeAndMessageResult

class AddPerformanceDataCommand(SessionCommandBase):
    def __init__(self, session):
        SessionCommandBase.__init__(self, session, "AddPerformanceData")

    def execute(self, dataSetName, key, value, description):
        requestObj = [dataSetName, key, value, description]

        result = self.executeCommand(requestObj)

        return OkErrorCodeAndMessageResult(result, "AddPerformanceData was successful", "AddPerformanceData failed")                