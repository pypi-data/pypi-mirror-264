import sys
import json
from testwizard.commands_core import SessionCommandBase
from .StringCompareResult import StringCompareResult

class StringCompareCommand(SessionCommandBase):
    def __init__(self, session):
        SessionCommandBase.__init__(self, session, "StringCompare")

    def execute(self, string1, string2):
        requestObj = [string1, string2]

        result = self.executeCommand(requestObj)

        return StringCompareResult(result, "StringCompare was successful", "StringCompare failed")