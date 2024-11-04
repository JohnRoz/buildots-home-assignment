from __future__ import annotations

import os
import time
from multiprocessing import Event, Process
from multiprocessing.synchronize import Event as SyncEvent
from queue import Queue


class FilePoller(Process):
    __interval: float
    __target_dir: str
    __stop_event: SyncEvent
    __file_types_filter: set[str]
    files_queue: "Queue[str]"

    __seen_files: set[str]

    def __init__(
        self, target_dir: str, file_types_filter: set[str] | None, interval: float = 5
    ) -> None:
        self.__target_dir = target_dir
        self.__interval = interval
        self.__stop_event = Event()
        self.__file_types_filter = (
            set() if file_types_filter is None else file_types_filter
        )
        self.__seen_files = set()
        self.files_queue = Queue()

        super().__init__()

    def poll_directory(self):
        new_files = set(os.listdir(self.__target_dir))

        for new_file in new_files:
            if self.is_relevant_file(new_file):
                self.files_queue.put(new_file)

        self.__seen_files.update(new_files)

    def is_relevant_file(self, new_file: str) -> bool:
        _, fileext = os.path.splitext(new_file)
        return (
            fileext.lower() in self.__file_types_filter
            and new_file not in self.__seen_files
        )

    def delete_file(self, file_to_del: str) -> None:
        """If I had more time, i'd make sure this method doesn't sit here, but rather this
        code is executed by registering a callback to an event"""
        os.remove(file_to_del)
        self.__seen_files.remove(file_to_del)

    def run(self):
        while not self.__stop_event.is_set():
            self.poll_directory()
            time.sleep(self.__interval)

    def stop(self):
        self.__stop_event.set()
