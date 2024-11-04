from pydantic import BaseModel


class ImgUrlsSchema(BaseModel):
    image_list: list[str]
