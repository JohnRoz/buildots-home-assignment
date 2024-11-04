from abc import ABC, abstractmethod
from multiprocessing import Event, Process
from multiprocessing.synchronize import Event as SyncEvent
from queue import Queue

from loguru import logger


class Service(Process, ABC):
    # Instance variables
    _input_dir: str
    _output_dir: str

    # Private instance variables
    __stop_event: SyncEvent

    def __init__(self, input_dir: str, output_dir: str) -> None:
        self._input_dir = input_dir
        self._output_dir = output_dir
        self.__stop_event = Event()

        super(Service, self).__init__()

    def run(self):
        """
        This is the process's main loop.
        """
        logger.info(f"Starting service {self.__class__.__name__}")

        while not self.__stop_event.is_set():
            pass  # wait on task queue

        logger.info(f"{self.__class__.__name__} service stopped.")

    def stop(self) -> None:
        """This triggers the ston syncronization event to stop the main loop of the service"""
        logger.info(f"Service {self.__class__.__name__} is stopping")
        self.__stop_event.set()

        # Make sure the process is terminated before calling thread continues
        self.join()

    def __process_file(self) -> None: ...

    def __delete_file(self) -> None: ...
