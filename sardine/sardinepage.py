from PIL import Image
import fitz

from .sardinecans import SardineCans
from .sardineimg import SardineImg

class SardinePage:

    __debug: bool

    page: fitz.Page

    cans: SardineCans

    images: dict[int, list[SardineImg]]

    def __init__(self, page: fitz.Page, debug: bool = False) -> None:
        self.__debug = debug

        self.page = page
        self.images = {}

        self.__init_image(self.page)
        self.__print_debug("SardinePage initialized")

    def __init_image(self, page: fitz.Page) -> None:
        """Initialize the image."""
        self.__print_debug(f"init_image: {page}")
        self.images[1] = []
        temp_image = page.get_pixmap(dpi=80)
        temp_image = Image.frombytes("RGB", (temp_image.width, temp_image.height), temp_image.samples)
        temp_image = temp_image.convert("L")
        image = SardineImg(temp_image, debug=self.__debug)
        self.images[1].append(image)

    def __print_debug(self, message: str) -> None:
        """Print debug message."""
        if self.__debug: print(f"[SardinePage]\t {message}")

    def add_image(self, resize: int = 1, reference: tuple[int, int] = (1, 0)) -> int:    
        """Add the image."""
        self.__print_debug(f"add_image: {resize} {reference}")
        image_size = reference[0] * resize
        self.images[image_size] = [] if image_size not in self.images else self.images[image_size]
        temp_image = self.images[reference[0]][reference[1]].get_image()
        temp_image = temp_image.resize((temp_image.width // resize, temp_image.height // resize))
        self.images[image_size].append(SardineImg(temp_image, debug=self.__debug))
        return len(self.images[image_size]) - 1
    
    def clone_image(self, reference: tuple[int, int]) -> int:
        """Clone the image."""
        self.__print_debug(f"clone_image: {reference}")
        temp_image = self.images[reference[0]][reference[1]].get_image()
        self.images[reference[0]].append(SardineImg(temp_image.copy(), debug=self.__debug))
        return len(self.images[1]) - 1

    def get_images(self) -> dict[int, list[SardineImg]]:
        """Get all images."""
        self.__print_debug("get_images")
        return self.images
    
    def get_image_by_identifier(self, image_identifier: int) -> list[SardineImg]:
        """Get an image by its identifier."""
        self.__print_debug(f"get_image_by_identifier: {image_identifier}")
        return self.images[image_identifier]