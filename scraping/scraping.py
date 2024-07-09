import json
import os
from pathlib import Path

from dotenv import load_dotenv
from selenium import webdriver
from selenium.common import NoSuchElementException
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
            "plugins.always_open_pdf_externally": True,
            'profile.managed_default_content_settings.javascript': 2,
            'profile.managed_default_content_settings.image': 2
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
        return links, self.driver.page_source

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

    def get_helppage(self, url):
        self.driver.get(url)
        WebDriverWait(self.driver, 5).until(lambda d: d.execute_script("return document.readyState") == "complete")
        header = self.driver.find_element(By.ID, "sectionheader-hilfeueberschrift").text
        content = self.driver.find_element(By.CLASS_NAME, "card-body").text
        return header, content

    def scrape_helppages(self, links):
        help_items = dict()
        for link in links:
            try:
                header, content = self.get_helppage(link)
            except NoSuchElementException:
                continue
            help_items[header] = content
        return help_items

    def get_linktree(self, url, sub=False):
        self.driver.get(url)
        links = []
        elems = self.driver.find_elements(by=By.XPATH, value="//a[@href]")
        for elem in elems:
            link = elem.get_attribute("href")
            if sub is False or (sub is True and url in link):
                links.append(link)
        return links


if __name__ == "__main__":
    scraping = Scraping()
    scraping.setup_driver()
    links = scraping.get_linktree("https://risi.muenchen.de/risi/service/hilfe", sub=True)
    print(links)
    help_items = scraping.scrape_helppages(links)
    print(json.dumps(help_items, ensure_ascii=False))
    scraping.shutdown_driver()
