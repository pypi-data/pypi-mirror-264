import base64
from dataclasses import dataclass
from typing import Optional
from urllib.parse import quote_plus as urlquote

import requests

from bookstw.ocr import BaseOCR, OCRArgs, OCRError


@dataclass
class BaiduHandwritingOCR(BaseOCR):
    """
    Baidu OCR API.
    """

    @dataclass
    class BaiduOCRArgs(OCRArgs):
        """
        API arguments for Baidu OCR.
        """

        detect_direction: bool = False
        probability: bool = False
        detect_alteration: bool = False

    api_key: str
    secret_key: str

    def _get_access_token(self):
        """
        Retrieve access token from Baidu API.
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
        }
        return str(
            requests.post(url, params=params, proxies=self.proxy)
            .json()
            .get("access_token")
        )

    def get_ocr(self, image: bytes, args: Optional[OCRArgs] = None):
        """
        Retrieve OCR from image.
        """
        url = (
            "https://aip.baidubce.com/rest/2.0/ocr/v1/handwriting?access_token="
            + self._get_access_token()
        )
        payload = f"image={urlquote(base64.b64encode(image).decode('utf8'))}" + (
            f"&{args}" if args else ""
        )
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        response = requests.post(url, headers=headers, data=payload, proxies=self.proxy)
        if response.status_code != 200:
            raise OCRError(f"Error {response.status_code}: {response.text}")

        json = response.json()
        if "error_code" in json:
            raise OCRError(f"Error {json['error_code']}: {json['error_msg']}")

        try:
            result: str = response.json()["words_result"][0]["words"]
        except (KeyError, IndexError):
            raise OCRError("No words found in response")

        return result.replace(" ", "")
