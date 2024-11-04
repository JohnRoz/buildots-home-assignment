from abc import ABC, abstractmethod
from typing import Any


class Analyser(ABC):
    @abstractmethod
    def analyze(self, img_file: str) -> Any:
        pass
