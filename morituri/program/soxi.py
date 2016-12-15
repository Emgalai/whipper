import os

from morituri.common import log, common
from morituri.common import task as ctask

SOXI = 'soxi'

class AudioLengthTask(ctask.PopenTask, log.Loggable):
    """
    I calculate the length of a track in audio samples.

    @ivar  length: length of the decoded audio file, in audio samples.
    """
    logCategory = 'AudioLengthTask'
    description = 'Getting length of audio track'
    length = None

    def __init__(self, path):
        """
        @type  path: unicode
        """
        assert type(path) is unicode, "%r is not unicode" % path

        self._path = path
        self.logName = os.path.basename(path).encode('utf-8')

        self.command = [SOXI, '-s', self._path]

        self._error = []
        self._output = []

    def commandMissing(self):
        raise common.MissingDependencyException('sox')

    def readbytesout(self, bytes):
        self._output.append(bytes)

    def readbyteserr(self, bytes):
        self._error.append(bytes)

    def failed(self):
        self.setException(Exception("soxi failed: %s"%"".join(self._error)))

    def done(self):
        if self._error:
            self.warning("soxi reported on stderr: %s", "".join(self._error))
        self.length = int("".join(self._output))
