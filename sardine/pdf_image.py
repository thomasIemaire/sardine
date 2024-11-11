import fitz
from PIL import Image
import numpy as np
import os

from .tebox import Tebox

class PdfImage:
    pdf_path: str
    pdf_images: list
    output_folder: str

    dpi: int
    threshold: int

    tebox: Tebox
    boxes: list

    def __init__(self, pdf_path: str, dpi: int = 80, threshold: int = 245, output_folder: str = "results") -> None:
        self.pdf_path = pdf_path
        self.dpi = dpi
        self.threshold = threshold
        self.__set_output_folder(output_folder)

    def __set_output_folder(self, output_folder: str) -> None:
        self.output_folder = os.path.splitext(os.path.basename(self.pdf_path))[0]
        self.output_folder = os.path.join(output_folder, self.output_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)

    def pdf_to_images(self, resize_factor: int = 1) -> None:
        self.pdf_images = []

        with fitz.open(self.pdf_path) as pdf:
            for i in range(pdf.page_count):
                page = pdf[i]
                img = page.get_pixmap(dpi=self.dpi)
                img = Image.frombytes("RGB", (img.width, img.height), img.samples)
                img = img.convert("L")
                img = img.resize((img.width // resize_factor, img.height // resize_factor))
                self.pdf_images.append(img)
                
        return self.pdf_images

    def save_images(self, prefix: str = "page", images: list = [], quality: int = 100) -> None:
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        
        img_to_save = images if images else self.pdf_images

        for i, img in enumerate(img_to_save):
            img_path = os.path.join(self.output_folder, f"{prefix}_{i+1}.png")
            img.save(img_path, quality=quality)

    def __add_pixels(self, image: Image.Image, row: int, axis:int) -> Image.Image:
        li = np.array(image)
        gp = np.ones(li.shape[1-axis])
        li = np.insert(li, row, gp, axis)
        return Image.fromarray(li)
    
    def __remove_pixels(self, image: Image.Image, row: int, axis:int) -> Image.Image:
        li = np.array(image)
        li = np.delete(li, row, axis)
        return Image.fromarray(li)

    def shake(self, image: Image.Image, axis: int) -> Image.Image:
        i1, i2 = self.__remove_pixels(image, 0, axis), self.__remove_pixels(image, -1, axis)
        i1, i2 = self.__add_pixels(i1, -1, axis), self.__add_pixels(i2, 0, axis)
        return self.superpose_images(i1, i2)
    
    def superpose_images(self, i1, i2) -> Image.Image:
        return Image.blend(i1, i2, alpha=0.5)
    
    def convert_to_black_and_white(self, image: Image.Image) -> Image.Image:
        gi = image.convert("L")
        li = np.array(gi)
        bli = np.where(li >= self.threshold, 255, 0).astype(np.uint8)
        return Image.fromarray(bli, mode="L")
    
    def reduce(self, image: Image.Image) -> Image.Image:
        return Image.fromarray(np.array(image)[::2, ::2])
    
    def __clear_corners(self, image: Image.Image) -> Image.Image:
        li = np.array(image)
        li = np.delete(li, 0, 0)
        li = np.delete(li, -1, 0)
        li = np.delete(li, 0, 1)
        return np.delete(li, -1, 1)

    def draw_boxes(self, image: Image.Image, rate: int = 1) -> Image.Image:
        i = image.convert("RGBA")
        li = np.array(i)

        for box in self.boxes:
            (x1, y1), (x2, y2) = self.__get_coordinates(box, rate)
            
            mask = np.zeros((y2 - y1, x2 - x1, 4), dtype=np.uint8)
            mask[:, :, 0] = 255
            mask[:, :, 3] = 96

            li[y1:y2, x1:x2] = (li[y1:y2, x1:x2] * (1 - mask[:, :, 3:4] / 255) + mask * (mask[:, :, 3:4] / 255)).astype(np.uint8)

        return Image.fromarray(li, mode="RGBA")

    def extract_boxes(self, image: Image.Image, rate: int = 1) -> None:
        bi = []
        li = np.array(image)
        
        for box in self.boxes:
            (x1, y1), (x2, y2) = self.__get_coordinates(box, rate)
            box_image = Image.fromarray(li[y1:y2, x1:x2])
            bi.append(box_image)

        output_temp = self.output_folder
        self.output_folder = os.path.join(self.output_folder, "boxes")
        self.save_images("boxes", bi)
        self.output_folder = output_temp

    def __get_coordinates(self, box: tuple, rate: int = 1) -> tuple:
        (y1, x1), (y2, x2) = box

        x1 = (x1 + 1) * rate - (rate - 1) // 2
        y1 = (y1 + 1) * rate - (rate - 1) // 2
        x2 = (x2 + 2) * rate + (rate - 1) // 3
        y2 = (y2 + 2) * rate + (rate - 1) // 3

        return (x1, y1), (x2, y2)

    def explore(self, image: Image.Image) -> None:
        ni = self.__clear_corners(image)
        
        self.tebox = Tebox(ni)
        self.boxes = self.tebox.determine_boxes()