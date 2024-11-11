import fitz
from PIL import Image

from .sardine_image import SardineImage

class SardinePage:

    page: fitz.Page
    image: SardineImage
    
    resize: int
    dpi: int

    def __init__(self, page, resize: int = 1, dpi: int = 80) -> None:
        self.page = page
        self.resize = resize
        self.dpi = dpi
        self.to_image()

    def to_image(self) -> None:
        self.image = SardineImage(page=self.page, resize=self.resize, dpi=self.dpi)

    def shake(self) -> Image.Image:
        self.image.shake()
        return self.image.image

    def binary(self, resize: int = None, threshold: int = 246) -> Image.Image:
        self.image.binary(resize, threshold)
        return self.image.image

    def reduce(self, factor: int = 2) -> Image.Image:
        self.image.reduce(factor)
        return self.image.image

    def explore(self) -> None:
        self.image.explore()

    def save(self, output_path: str) -> None:
        self.image.save(output_path)

    def draw(self, output_path: str) -> None:
        self.image.draw_cans(1).save(output_path, quality=100)