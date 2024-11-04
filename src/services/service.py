import os
from abc import ABC, abstractmethod
from multiprocessing import Event, Process
from multiprocessing.synchronize import Event as SyncEvent
from typing import Any, Iterable

from loguru import logger

from ..exceptions.invalid_schema_exception import InvalidSchemaException
from ..file_utils.file_poller import FilePoller


class Service(Process, ABC):
    # Protected instance variables
    _input_dir: str
    _output_dirs: Iterable[str]
    _file_poller: FilePoller

    # Private instance variables
    __stop_event: SyncEvent

    def __init__(
        self,
        input_dir: str,
        output_dirs: Iterable[str],
        file_types_filter: set[str] | None,
        file_polling_interval: float = 5,
    ) -> None:
        self._input_dir = input_dir
        self._output_dirs = output_dirs
        self.__stop_event = Event()
        self._file_poller = FilePoller(
            target_dir=input_dir,
            file_types_filter=file_types_filter,
            interval=file_polling_interval,
        )

        super(Service, self).__init__()

    def run(self):
        """
        This is the process's main loop.
        """
        logger.info(f"Starting service {self.__class__.__name__}")

        while not self.__stop_event.is_set():
            try:
                # This is blocking
                new_file = self._file_poller.files_queue.get()

                self._process_file(new_file)
                self.__delete_file(new_file)
            except InvalidSchemaException as e:
                # TODO: Handle appropriatly
                logger.error(f"Invalid Schema: {str(e)}")
            except Exception as e:
                # If I had more time i'd make sure to handle all types of exceptions (I can think of) gracfully
                logger.error(f"An error occurred {str(e)}")

        logger.info(f"{self.__class__.__name__} service stopped.")

    def stop(self) -> None:
        """This triggers the ston syncronization event to stop the main loop of the service"""
        logger.info(f"Service {self.__class__.__name__} is stopping")
        self.__stop_event.set()

        # Make sure the process is terminated before calling thread continues
        self.join()

    @abstractmethod
    def _process_file(self, new_file: str) -> None: ...

    def __delete_file(self, processed_file: str) -> None:
        self._file_poller.delete_file(processed_file)
