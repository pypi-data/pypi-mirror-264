from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, Optional


class OCRArgs(ABC):
    """
    API arguments.
    """

    def _to_str(self, value: Any):
        """
        Convert value to string.
        """
        if isinstance(value, bool):
            return str(value).lower()
        return str(value)

    def __str__(self) -> str:
        return "&".join([f"{k}={self._to_str(v)}" for k, v in self.__dict__.items()])


class OCRError(Exception):
    """
    OCR error.
    """

    pass


@dataclass
class BaseOCR(ABC):
    """
    Base OCR class.
    """

    proxy: Dict[str, str]

    @abstractmethod
    def get_ocr(self, image: bytes, args: Optional[OCRArgs] = None) -> str:
        """
        Retrieve OCR from image.
        """
        pass
