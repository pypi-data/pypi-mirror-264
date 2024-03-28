import sys
import json

from testwizard.commands_core import CommandBase
from .WaitForAudioResult import WaitForAudioResult


class WaitForAudioCommand(CommandBase):
    def __init__(self, testObject):
        CommandBase.__init__(self, testObject, "WaitForAudio")

    def execute(self, level, timeout):
        requestObj = [level, timeout]

        result = self.executeCommand(requestObj)

        return WaitForAudioResult(result, "WaitForAudio was successful", "WaitForAudio failed")
