import glob
import os
from pathlib import Path


class PrintNpmLogs:

    @staticmethod
    def print_last_lines(lines: int = 50):
        inst: PrintNpmLogs = PrintNpmLogs()
        inst.print_last_npm_logs(lines)

    def get_last_file(self, file_pattern: str) -> str:
        list_of_files = glob.glob(file_pattern)
        latest_file = max(list_of_files, key=os.path.getctime)
        return latest_file

    def print_lines(self, filename: str, no_of_lines: int = 1):
        file = open(filename, 'r')
        lines = file.readlines()
        last_lines = lines[-no_of_lines:]
        for line in last_lines:
            print(line)
        file.close()

    def print_last_npm_logs(self, lines: int):
        npm_log_dir: Path = Path(Path().home() / '.npm/_logs')
        if npm_log_dir.is_dir():
            logs: Path = Path(self.get_last_file(npm_log_dir.as_posix() + '/*.log'))
            if logs.is_file():
                self.print_lines(logs.as_posix(), lines)
            else:
                print('No npm file log found')
        else:
            print('No npm dif log found at ' + npm_log_dir.as_posix())
