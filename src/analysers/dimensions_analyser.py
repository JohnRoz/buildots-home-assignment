from typing import Any, Mapping

import cv2

from .analyser import Analyser


class DimensionsAnalyser(Analyser):
    def analyze(self, img_file: str) -> Any:
        try:
            image = cv2.imread(img_file)

            # If the image is not greyscale, shape returns a third value for channels
            dimentions = image.shape
            height, width = dimentions[0], dimentions[1]

            return {"height": height, "width": width}
        except Exception:
            # TODO: Handle Properly
            raise
