import time
import os.path

from selenium import webdriver
from bs4 import BeautifulSoup

def save_laws_for_book(driver, law):
    if os.path.isfile(f"laws/{law}.md"):
        return

    url = f"https://www.gesetze-im-internet.de/{law}/"
    driver.get(url)

    soup = BeautifulSoup(driver.page_source, features="html.parser")

    link_list = soup.find_all("a")

    all_paragraphs = []

    for link in link_list:
        if link.getText().startswith("§") or link.getText().startswith("Art"):
            all_paragraphs.append(link)

    file = open(f"laws/{law}.md", "w", encoding="UTF-8")

    law_title = soup.find("h1", attrs={"class" : "headline"})
    file.write(f"# {law_title.get_text()}\n")

    for single_paragraph in all_paragraphs:
        title = single_paragraph.get_text()
        link = single_paragraph.get('href',None)
        driver.get(f"{url}{link}")
        tmp_soup = BeautifulSoup(driver.page_source, features="html.parser")
        all_lines = tmp_soup.find_all("div", attrs={"class" : "jurAbsatz"})

        if title.__contains__("weggefallen"):
            continue

        file.write(f"## {title}\n")
        print(f"writing law {title}")
        for line in all_lines:
            file.write(f"{line.get_text()}\n\n")

    file.close()

if __name__ == "__main__":
        options = webdriver.ChromeOptions()

        options.add_argument("--headless=new")

        driver = webdriver.Chrome(options=options)

        laws = ["stgb", "bgb", "tierschg", "tierschlv_2013", "tierschtrv_2009", "arbschg", "arbst_ttv_2004", "arbzg", "juschg", "jarbschg", "bdsg_2018", "stvg", "stvo_2013", "partg", "partg", "gg", "npsg", "baf_g", "bartschv_2005", "btmg_1981", "fev_2010", "b_ausbv_2004", "bbahng", "bbahnvermg", "bfdg", "bierstg_2009", "bierv", "madg", "kagb", "markeng", "moselschpv_1997", "vstg_1974"]

        for law in laws:
            save_laws_for_book(driver, law)
            time.sleep(3)

        driver.quit()

