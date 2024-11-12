from PIL import Image
import numpy as np
import os

class SardineImg:

    __debug: bool

    image: Image.Image

    width: int
    height: int

    def __init__(self, image: Image.Image, debug: bool = False) -> None:
        self.__debug = debug
        
        self.image = image
        self.__set_size(self.image.size)

        self.__print_debug("SardineImg initialized")

    def __print_debug(self, message: str) -> None:
        """Print debug message."""
        if self.__debug: print(f"[SardineImg]\t {message}")

    def get_image(self) -> Image.Image:
        """Get the image."""
        self.__print_debug("get_image")
        return self.image
    
    def __set_size(self, size: tuple[int, int]) -> None:
        """Set the size."""
        self.__print_debug(f"set_size: {size}")
        self.width, self.height = size

    def binarization(self, threshold: int = 246) -> None:
        """Binarize the image."""
        self.__print_debug(f"binarization: {threshold}")
        temp_image: Image.Image = self.image
        temp_image = temp_image.convert("L")
        array_image: np.NDArray[np.Any] = np.array(temp_image)
        array_image = np.where(array_image > threshold, 255, 0).astype(np.uint8)
        temp_image = Image.fromarray(array_image)
        self.image = temp_image

    def clear_borders(self, border: int = 1) -> None:
        """Clear the borders of the image."""
        self.__print_debug(f"clear_borders: {border}")
        temp_image: Image.Image = self.image
        temp_image = temp_image.crop((border, border, self.width - border, self.height - border))
        self.image = temp_image
        self.__set_size(self.image.size)
    
    def reduce(self, factor: int = 2) -> None:
        """Reduce the image."""
        self.__print_debug(f"reduce: {factor}")
        temp_image: Image.Image = self.image
        array_image: np.NDArray[np.Any] = np.array(temp_image)
        array_image = array_image[::factor, ::factor]
        temp_image = Image.fromarray(array_image)
        self.image = temp_image
        self.__set_size(self.image.size)

    def superpose(self, image: Image.Image) -> None:
        """Superpose an image."""
        self.__print_debug(f"superpose: {image}")
        temp_image: Image.Image = self.image
        temp_image = Image.blend(temp_image, image, 0.5)
        self.image = temp_image

    def save(self, output_folder: str, file_name: str) -> None:
        """Save the image."""
        self.__print_debug(f"save: {output_folder}, {file_name}")
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        file_path = os.path.join(output_folder, file_name)
        self.image.save(f"{file_path}.png", quality=100)

    def __remove_pixels_line(self, row: int, axis: int) -> None:
        """Remove pixels in a line."""
        self.__print_debug(f"remove_pixels_line: {row}, {axis}")
        temp_image: Image.Image = self.image
        array_image: np.NDArray[np.Any] = np.array(temp_image)
        array_image = np.delete(array_image, row, axis)
        temp_image = Image.fromarray(array_image)
        self.image = temp_image
        self.__set_size(self.image.size)

    def __add_pixels_line(self, row: int, axis: int) -> None:
        """Add pixels in a line."""
        self.__print_debug(f"add_pixels_line: {row}, {axis}")
        temp_image: Image.Image = self.image
        array_image: np.NDArray[np.Any] = np.array(temp_image)
        array_image = np.insert(array_image, row, 255, axis)
        temp_image = Image.fromarray(array_image)
        self.image = temp_image
        self.__set_size(self.image.size)

    def shake(self, factor: int = 2) -> None:
        """Shake the image."""
        self.__print_debug(f"shake: {factor}")
        for _ in range(factor):
            temp_image: SardineImg = SardineImg(self.image.copy(), debug=self.__debug)

            self.__remove_pixels_line(0, 0)
            self.__add_pixels_line(-1, 0)
            self.__remove_pixels_line(0, 1)
            self.__add_pixels_line(-1, 1)

            temp_image.__remove_pixels_line(-1, 0)
            temp_image.__add_pixels_line(0, 0)
            temp_image.__remove_pixels_line(-1, 1)
            temp_image.__add_pixels_line(0, 1)

            self.superpose(temp_image.get_image())
        self.__set_size(self.image.size)

    def resize(self, factor: int) -> None:
        """Resize the image."""
        self.__print_debug(f"resize: {factor}")
        temp_image: Image.Image = self.image
        temp_image = temp_image.resize((self.width // factor, self.height // factor))
        self.image = temp_image
        self.__set_size(self.image.size)