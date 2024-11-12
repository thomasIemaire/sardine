import fitz

from .sardinepage import SardinePage

class SardinePdf:

    __debug: bool

    pdf_path: str
    
    pdf_pages: list[SardinePage]

    def __init__(self, pdf_path: str, debug: bool = False) -> None:
        self.__debug = debug
        
        self.pdf_path = pdf_path
        self.pdf_pages = []

        self.__open()

        self.__print_debug("SardinePdf initialized")

    def __print_debug(self, message: str) -> None:
        """Print debug message."""
        if self.__debug: print(f"[SardinePdf]\t {message}")

    def __open(self) -> None:
        """Open the PDF."""
        self.__print_debug("open")
        with fitz.open(self.pdf_path) as pdf:
            self.pdf_pages = [SardinePage(page, debug=self.__debug) for page in pdf]

    def get_pages(self) -> list[SardinePage]:
        """Get all pages."""
        self.__print_debug("get_pages")
        return self.pdf_pages
    
    def get_page_by_number(self, page_number: int) -> SardinePage:
        """Get a page by its number."""
        self.__print_debug(f"get_page_by_number: {page_number}")
        return self.pdf_pages[page_number]