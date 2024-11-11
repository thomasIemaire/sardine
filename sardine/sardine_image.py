import fitz
from PIL import Image
import numpy as np

from .sardine_can import SardineCans

class SardineImage:

    image: Image.Image

    resize: int
    dpi: int

    cans: SardineCans

    def __init__(self, page: fitz.Page = None, image: Image.Image = None, resize: int = 1, dpi: int = 80) -> None:
        self.resize = resize
        self.dpi = dpi

        if image: self.image = image
        else: self.open(page)
    
    def save(self, output_path: str) -> None:
        self.image.save(output_path, quality=100)
    
    def open(self, page: fitz.Page) -> None:
        self.image = page.get_pixmap(dpi=self.dpi)
        self.image = Image.frombytes("RGB", (self.image.width, self.image.height), self.image.samples)
        self.image = self.image.convert("L")
        self.image = self.__resize()

    def __resize(self, factor: int = None) -> Image.Image:
        fr = factor if factor else self.resize
        return self.image.resize((self.image.width // fr, self.image.height // fr))
    
    def superpose(self, i1, i2) -> Image.Image:
        return Image.blend(i1, i2, alpha=0.5)
    
    def shake(self) -> Image.Image:
        i1, i2 = self.__remove_pixels(self.image, 0, 1), self.__remove_pixels(self.image, -1, 1)
        i1, i2 = self.__add_pixels(i1, -1, 1), self.__add_pixels(i2, 0, 1)
        s1 = self.superpose(i1, i2)

        i1, i2 = self.__remove_pixels(self.image, 0, 0), self.__remove_pixels(self.image, -1, 0)
        i1, i2 = self.__add_pixels(i1, -1, 0), self.__add_pixels(i2, 0, 0)
        s2 = self.superpose(i1, i2)

        self.image = self.superpose(s1, s2)
        return self.image
    
    def __add_pixels(self, image: Image.Image, row: int, axis:int) -> Image.Image:
        li = np.array(image)
        gp = np.ones(li.shape[1-axis])
        li = np.insert(li, row, gp, axis)
        return Image.fromarray(li)
    
    def __remove_pixels(self, image: Image.Image, row: int, axis:int) -> Image.Image:
        li = np.array(image)
        li = np.delete(li, row, axis)
        return Image.fromarray(li)
        
    def binary(self, resize: int = None, threshold: int = 246) -> None:
        self.image = self.__resize(resize) if resize else self.image
        self.image = self.image.convert("L")
        self.image = np.array(self.image)
        self.image = np.where(self.image > threshold, 255, 0).astype(np.uint8)
        self.image = Image.fromarray(self.image)

    def reduce(self, factor: int = 2) -> None:
        self.image = Image.fromarray(np.array(self.image)[::factor, ::factor])

    def __clear_corners(self) -> Image.Image:
        li = np.array(self.image)
        li = np.delete(li, 0, 0)
        li = np.delete(li, -1, 0)
        li = np.delete(li, 0, 1)
        li = np.delete(li, -1, 1)
        return Image.fromarray(li)

    def explore(self) -> None:
        self.image = self.__clear_corners()
        self.cans = SardineCans(self.image)
    
    def draw_cans(self, rate: int = 1) -> Image.Image:
        i = self.image.convert("RGBA")
        li = np.array(i)

        for can in self.cans.get_cans():
            (x1, y1), (x2, y2) = SardineCans.get_coordinates(can, rate)
            
            mask = np.zeros((y2 - y1, x2 - x1, 4), dtype=np.uint8)
            mask[:, :, 0] = 255
            mask[:, :, 3] = 96

            li[y1:y2, x1:x2] = (li[y1:y2, x1:x2] * (1 - mask[:, :, 3:4] / 255) + mask * (mask[:, :, 3:4] / 255)).astype(np.uint8)

        return Image.fromarray(li, mode="RGBA")