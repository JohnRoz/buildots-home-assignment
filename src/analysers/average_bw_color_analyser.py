from typing import Any

import cv2

from .analyser import Analyser


class AverageBWColorAnalyser(Analyser):
    def analyze(self, img_file: str) -> Any:
        image = cv2.imread(img_file)

        # Calculate the average color for each channel (BGR)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Calculate the average grayscale value
        average_gray = gray_image.mean()

        return average_gray
