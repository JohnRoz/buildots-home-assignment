import os

import imageio as im
import numpy as np

from ..lib.nfov import NFOV
from .service import Service


class ProjectorService(Service):
    def __init__(
        self,
        input_dir: str,
        output_dir: str,
        file_polling_interval: float = 5,
    ):
        super().__init__(
            input_dir=input_dir,
            output_dirs={output_dir},
            file_types_filter=None,
            file_polling_interval=file_polling_interval,
        )

    def _process_file(self, new_file: str) -> None:
        self.__project(new_file)

    def __project(self, img_file: str) -> None:
        _, filename = os.path.split(img_file)

        img = im.imread(img_file)
        nfov = NFOV()
        center_point = np.array([0.5, 0.5])
        output = nfov.toNFOV(img, center_point)

        for output_dir in self._output_dirs:
            im.imwrite(os.path.join(output_dir, filename), output)
