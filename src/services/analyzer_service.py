import json
import os
from typing import Iterable, Type

from ..analysers.analyser import Analyser
from ..lib.nfov import NFOV
from .service import Service


class AnalyserService(Service):
    """
    This service can recieve an iterable of Analyser classes.
    For each one an instance of the analyzer is constructed and saved in an iterable to be used later-on.
    Currently the Analysers are equivilant to pure-functions and an instance is not really necessary, but if the
    """

    __analysers: Iterable[Analyser]

    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        analyser_classes: Iterable[Type[Analyser]],
        file_polling_interval: float = 5,
    ):
        self.__analysers = set()

        for AnalyserCls in analyser_classes:
            self.__analysers.add(AnalyserCls())

        super().__init__(
            input_dir=input_dir,
            output_dirs={output_dir},
            file_types_filter=None,
            file_polling_interval=file_polling_interval,
        )

    def _process_file(self, new_file: str) -> None:
        """This supports adding any class that inherits from Analyser"""
        _, filename = os.path.split(new_file)

        result = {}

        # Iterate through all registered analysers and get result from each
        for analyzer in self.__analysers:
            result[analyzer.__class__.__name__] = analyzer.analyze(new_file)

        for output_dir in self._output_dirs:
            with open(os.path.join(output_dir, filename), "w") as file:
                json.dump(result, file)
