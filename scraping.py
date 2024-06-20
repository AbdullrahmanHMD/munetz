import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from pathlib import Path


class Scraping:

    def __init__(self):
        self.driver = None

    def setup_driver(self):
        options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            "download.default_directory": str(Path(os.getcwd()) / "docs"),
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
        rows = self.driver.find_elements(info_locator)
        details = dict()
        for row in rows:
            details[row.find_element(By.CLASS_NAME, "keyvalue-key").text] = row.find_element(By.CLASS_NAME, "keyvalue-value").text

        doc_locator = locate_with(By.PARTIAL_LINK_TEXT, ".pdf").below(rows[-1])
        docs = self.driver.find_elements(doc_locator)
        for doc in docs:
            print(doc.text)
            doc.click()
        time.sleep(3)
        return details


if __name__ == "__main__":
    scraping = Scraping()
    scraping.setup_driver()
    details = scraping.get_page("https://risi.muenchen.de/risi/antrag/detail/6261018?dokument=v6486171")
    print(details)
    scraping.shutdown_driver()
