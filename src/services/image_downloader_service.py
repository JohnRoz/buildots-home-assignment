import json
import os
from typing import Iterable

import requests

from ..schemas.img_urls_schema import ImgUrlsSchema
from .service import Service


class ImageDownloaderService(Service):
    def __init__(
        self,
        input_dir: str,
        output_dirs: Iterable[str],
        file_polling_interval: float = 5,
    ):
        relevant_file_types = {"json"}
        super().__init__(
            input_dir=input_dir,
            output_dirs=output_dirs,
            file_types_filter=relevant_file_types,
            file_polling_interval=file_polling_interval,
        )

    def _process_file(self, new_file: str) -> None:
        with open(new_file, "r") as json_file:
            data = json.load(json_file)

        imgs_url = ImgUrlsSchema(**data)

        for img_url in imgs_url.image_list:
            self.__download_image(img_url)

    def __download_image(self, img_url: str):
        try:
            img_name = img_url.split("/")[-1]
            response = requests.get(img_url)

            for output_dir in self._output_dirs:
                with open(os.path.join(output_dir, img_name), "wb") as file:
                    file.write(response.content)
        except Exception:
            # TODO: Handle HTTP Exceptions properly
            raise
