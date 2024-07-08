import json
import os
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common.exceptions import JavascriptException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.relative_locator import locate_with
from selenium.webdriver.support.wait import WebDriverWait


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
        WebDriverWait(self.driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")
        # Locate all PDFs
        doc_locator = locate_with(By.PARTIAL_LINK_TEXT, ".pdf")
        docs = self.driver.find_elements(doc_locator)
        links = [(doc.text, doc.get_attribute('href')) for doc in docs]
        return links

    def get_details(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")
        if "sitzungsvorlage" in url:
            # Sitzungsvorlagen have a slightly different header ID than other document types
            info_locator = locate_with(By.CLASS_NAME, "keyvalue-row").below({By.ID: "sectionheader-informationen"})
        else:
            info_locator = locate_with(By.CLASS_NAME, "keyvalue-row").below({By.ID: "sectionheader-info"})
        details = dict()
        try:
            rows = self.driver.find_elements(info_locator)
            for row in rows:
                details[row.find_element(By.CLASS_NAME, "keyvalue-key").text] = row.find_element(By.CLASS_NAME, "keyvalue-value").text
        except JavascriptException:
            pass
        return json.dumps(details)

# TODO scrape html file as well


if __name__ == "__main__":
    scraping = Scraping()
    scraping.setup_driver()
    details, links = scraping.get_page("https://risi.muenchen.de/risi/antrag/detail/6261018?dokument=v6486171")
    scraping.shutdown_driver()
    print(details)
    print(links)
