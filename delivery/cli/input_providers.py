import sys
from typing import List

class InputProvider:
    def get_input(self, prompt: str = "") -> str:
        raise NotImplementedError


class ConsoleInputProvider(InputProvider):
    def get_input(self, prompt: str = "") -> str:
        return input(prompt)


class FileInputProvider(InputProvider):
    def __init__(self, lines: List[str]):
        self.lines = lines
        self.index = 0

    @classmethod
    def from_file(cls, file_path: str) -> "FileInputProvider":
        with open(file_path, "r") as f:
            lines = [
                line.strip()
                for line in f.readlines()
                if line.strip() and not line.strip().startswith("#") and not line.strip().startswith("//")
            ]
        return cls(lines)

    def get_input(self, prompt: str = "") -> str:
        if self.index < len(self.lines):
            line = self.lines[self.index]
            self.index += 1
            return line
        sys.exit("Error: End of input file reached unexpectedly.")
