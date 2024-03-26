import subprocess


class ProcessMock:
    def __init__(
        self,
        check_error=False,
        stdout=None
    ):
        self.check_error = check_error
        self._stdout = stdout

    def check_returncode(self):
        if self.check_error:
            raise subprocess.CalledProcessError(returncode=1, cmd='non_existent_file')

    @property
    def stdout(self):
        return self._stdout

    @property
    def returncode(self):
        return 1
