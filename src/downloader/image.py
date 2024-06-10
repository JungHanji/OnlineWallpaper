from PIL import Image as PILImage
from src.downloader.utils import *
from typing import cast, List
import io

class Image:
    def __init__(self, tags: list[str], prev_url: str, main_url: str, resolution: tuple[int, int], preview_resolution: tuple[int, int]):
        self.tags = tags
        self.prev_url = prev_url
        self.main_url = main_url
        self.resolution = resolution
        self.preview_resolution = preview_resolution
    
    def __str__(self) -> str:
        return f"Image, with tags {", ".join(self.tags)}:\n\tpreview url: {self.prev_url}\n\tmain url: {self.main_url}"

    def save(self, path: str, type: str = 'main'):
        url = self.main_url if type == 'main' else self.prev_url
        response = get(url)
        if response.status_code == 200:
            image = PILImage.open(io.BytesIO(response.content))
            image.save(path)
        else:
            raise Exception(f"Failed to download image from {url}")
    
    def data(self, type: str = 'main') -> list[float]:
        data: list[float] = []
        
        url = self.main_url if type == 'main' else self.prev_url
        response = get(url)
        if response.status_code == 200:
            image = PILImage.open(io.BytesIO(response.content))
            image.convert("RGB")
            data = [(i[0], i[1], i[2], 255) for i in list(image.getdata())]
        else:
            raise Exception(f"Failed to download image from {url}")


        return data