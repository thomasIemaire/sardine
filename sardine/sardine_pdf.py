import fitz
import os

from .sardine_page import SardinePage

class SardinePdf:

    __debug: bool

    pdf_path: str
    output_folder: str

    pages: list[SardinePage] = []

    resize: int
    dpi: int
    threshold: int

    def __init__(self, pdf_path: str, output_folder: str = "results", debug: bool = False) -> None:
        self.__debug = debug

        self.pdf_path = pdf_path
        self.output_folder = output_folder

        self.__set_output_folder(output_folder) if debug else None

    def __set_output_folder(self, output_folder: str) -> None:
        self.output_folder = os.path.splitext(os.path.basename(self.pdf_path))[0]
        self.output_folder = os.path.join(output_folder, self.output_folder)
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
    
    def open(self, resize: int = 1, dpi: int = 80) -> list[SardinePage]:
        self.resize = resize
        self.dpi = dpi

        self.pages = []

        with fitz.open(self.pdf_path) as pdf:
            self.pages = [SardinePage(page, self.resize, self.dpi) for page in pdf]
                
        return self.pages
    
    def __save(self, pages: list[SardinePage], prefix: str = "page") -> None:
        for i, page in enumerate(pages):
            page.save(f"{self.output_folder}/{prefix}_{i+1}.png")

    def shake(self) -> None:
        sp = [p.shake() for p in self.pages]
        if self.__debug: self.__save(sp, "shake")

    def binary(self, resize: int = None, threshold: int = 246) -> None:
        bp = [p.binary(resize, threshold) for p in self.pages]
        if self.__debug: self.__save(bp, "binary")

    def reduce(self, factor: int = 2) -> None:
        rp = [p.reduce(factor) for p in self.pages]
        if self.__debug: self.__save(rp, "reduce")

    def explore(self) -> None:
        ep = [p.explore() for p in self.pages]

    def draw(self, prefix: str = "draw") -> None:
        dp = [p.draw(f"{self.output_folder}/{prefix}_{i+1}.png") for i, p in enumerate(self.pages)]