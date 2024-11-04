from typing import Any

import cv2

from .analyser import Analyser


class AverageColorAnalyser(Analyser):
    def analyze(self, img_file: str) -> Any:
        image = cv2.imread(img_file)

        # Calculate the average color for each channel (BGR)
        average_color_per_channel = image.mean(axis=0).mean(axis=0)

        average_color_rgb = average_color_per_channel[::-1]

        return average_color_rgb
