import os

import cv2

from .service import Service


class EdgeDetectionService(Service):
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
        self.__detect_edges(new_file)

    def __detect_edges(self, img_file: str) -> None:
        _, filename = os.path.split(img_file)
        _, ext = os.path.splitext(img_file)

        threshold1, threshold2 = EdgeDetectionService.__get_image_type_thresholds(ext)

        image = cv2.imread(img_file)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, threshold1, threshold2)

        for output_dir in self._output_dirs:
            cv2.imwrite(os.path.join(output_dir, filename), edges)

    @staticmethod
    def __get_image_type_thresholds(file_type: str) -> tuple[int, int]:
        # if I had more time I'd query the thresholds from persistent memory given the file type
        if file_type.lower() == "png":
            return (100, 200)
        return (100, 150)
