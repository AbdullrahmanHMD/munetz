import os
import time

from selenium import webdriver
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.support.relative_locator import locate_with
from pathlib import Path
from zipfile import ZipFile
from dotenv import load_dotenv


class Scraping:

    def __init__(self):
        load_dotenv()
        self.driver = None

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        if not os.getenv("LOCAL"):
            # Flags required to run Chrome on the EC2 instance
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")
            options.add_argument("enable-automation")
            options.add_argument("--disable-infobars")
            options.add_argument("--disable-dev-shm-usage")
        options.add_experimental_option('prefs', {
            "download.default_directory": str(Path(os.getcwd()) / "temp"),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True
        })
        self.driver = webdriver.Chrome(options=options)

    def shutdown_driver(self):
        self.driver.quit()

    def get_page(self, url):
        self.driver.get(url)
        # TODO: change to wait for all relevant elements to be loaded instead
        self.driver.implicitly_wait(5)
        boxes = self.driver.find_elements(By.CLASS_NAME, "mt-4")
        info_locator = locate_with(By.CLASS_NAME, "keyvalue-row").below({By.ID: "sectionheader-info"})
        details = dict()
        try:
            rows = self.driver.find_elements(info_locator)
            for row in rows:
                details[row.find_element(By.CLASS_NAME, "keyvalue-key").text] = row.find_element(By.CLASS_NAME, "keyvalue-value").text
        except JavascriptException:
            # TODO: fix error for some types of pages (https://risi.muenchen.de/risi/sitzungsvorlage/detail/8322280?dokument=v8482514)
            pass

        doc_locator = locate_with(By.PARTIAL_LINK_TEXT, ".pdf")
        docs = self.driver.find_elements(doc_locator)
        links = [(doc.text, doc.get_attribute('href')) for doc in docs]
        return details, links

# TODO scrape html file as well


if __name__ == "__main__":
    scraping = Scraping()
    scraping.setup_driver()
    details, links = scraping.get_page("https://risi.muenchen.de/risi/antrag/detail/6261018?dokument=v6486171")
    scraping.shutdown_driver()
    print(details)
    print(links)
