import logging
import time

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from bookstw.ocr import BaseOCR, OCRError


class LoginError(Exception):
    """
    Error when login failed.
    """

    pass


class DailySignInError(Exception):
    """
    Error when daily sign in failed.
    """

    pass


class BooksTWRunner:
    """
    Selenium runner for books.com.tw.
    """

    LOGIN_URL = "https://cart.books.com.tw/member/login"
    DAILY_SIGN_IN_URL = (
        "https://myaccount.books.com.tw/myaccount/myaccount/memberReadMileage"
    )

    def __init__(self, ocr: BaseOCR, webdriver: WebDriver):
        self.driver = webdriver
        self.ocr = ocr
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)

    def login(
        self,
        username: str,
        password: str,
        allow_manual_retry: bool = True,
        ocr_retry: int = 3,
        retry_delay: int = 5,
    ):
        """
        Login to books.com.tw.

        Captcha is solved using OCR.

        Args:
            username(str): Username.
            password(str): Password.
            ocr_retry(int): Number of retries for OCR.
            retry_delay(int): Delay between retries in seconds.
        """
        self.logger.info(f"Logging in on {self.LOGIN_URL} ...")
        self.driver.get(self.LOGIN_URL)

        self.logger.info("Filling in login form...")
        self.driver.find_element(By.ID, "login_id").send_keys(username)
        self.driver.find_element(By.ID, "login_pswd").send_keys(password)

        retry = 0
        self.logger.info("Solving captcha...")
        while True:
            time.sleep(retry_delay)

            if self.driver.current_url != self.LOGIN_URL:
                break

            if retry > 0:
                self.logger.warning(
                    f"Failed to solve captcha. Retrying... ({retry}/{ocr_retry})"
                )

            img = self.driver.find_element(By.ID, "captcha_img").find_element(
                By.TAG_NAME, "img"
            )

            try:
                captcha_bytes = img.screenshot_as_png
                captcha = self.ocr.get_ocr(captcha_bytes)
                self.driver.find_element(By.ID, "captcha").send_keys(captcha)
                self.driver.find_element(By.ID, "books_login").click()
            except OCRError:
                retry = -1
                break

            if retry == ocr_retry:
                retry = -1
                break

            retry += 1

        if retry == -1:
            if not allow_manual_retry:
                self.logger.error("Failed to solve captcha by OCR.")
                raise LoginError("Failed to solve captcha by OCR.")

            self.logger.error("Failed to solve captcha by OCR. Please try manually.")

            import os
            import tempfile

            temp = tempfile.NamedTemporaryFile(suffix=".png")

            with temp:
                while True:
                    time.sleep(retry_delay)
                    if self.driver.current_url != self.LOGIN_URL:
                        break

                    if retry >= 0:
                        self.logger.warning("Failed to validate captcha. Retrying...")

                    img = self.driver.find_element(By.ID, "captcha_img").find_element(
                        By.TAG_NAME, "img"
                    )
                    captcha_bytes = img.screenshot_as_png

                    temp.seek(0)
                    temp.write(captcha_bytes)

                    os.startfile(temp.name)
                    self.logger.info("Enter captcha manually here.")
                    captcha = input("Captcha: ")
                    self.driver.find_element(By.ID, "captcha").send_keys(captcha)
                    self.driver.find_element(By.ID, "books_login").click()

                    retry += 1

        self.logger.info("Logged in successfully.")

    def daily_sign_in(self):
        """
        Daily sign in to get Read Mileage.
        """
        self.logger.info("Signing in...")
        self.driver.get(self.DAILY_SIGN_IN_URL)

        if self.driver.current_url.startswith(self.LOGIN_URL):
            self.logger.error("Not logged in. Please login first.")
            return

        try:
            self.driver.find_element(By.CLASS_NAME, "btn-sign-in").click()
            self.logger.info("Signed in successfully.")
        except NoSuchElementException:
            self.logger.error("Failed to sign in. You might already signed in today.")
            raise DailySignInError(
                "Failed to sign in. You might already signed in today."
            )
