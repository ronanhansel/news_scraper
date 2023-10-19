from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER, logging
LOGGER.setLevel(logging.WARNING)

import csv

class Content:
  def __init__(self, author, title, article):
    self.author = author
    self.title = title
    self.article = article

driver = webdriver.Chrome()
start_page = 7
end_page = 8
for page in range (start_page, end_page + 1):
    with open(f'CNBC_output_{page}.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Author', 'Title', 'Content'])
        driver.get(f'https://www.cnbc.com/business/?page={page}')
        titles_el_locator = (By.CLASS_NAME, "Card-title")
        ignored_exceptions=(NoSuchElementException,StaleElementReferenceException,)
        titles_el = WebDriverWait(driver, 10, ignored_exceptions).until(
                                      EC.presence_of_all_elements_located(titles_el_locator)
                                  )
        ids = [i.get_attribute("id") for i in titles_el]
        for no in range(len(titles_el)):
            try:
              title_el = titles_el[no]
              print(title_el.text)
            except StaleElementReferenceException:
              titles_el = WebDriverWait(driver, 10, ignored_exceptions).until(
                              EC.presence_of_all_elements_located(titles_el_locator)
                          )
              print('Stale Element. Retrying...')
              title_el = titles_el[no]
            title = title_el.text
            title_el.click()
            c = Content(driver.find_element(By.CLASS_NAME, "Author-authorName").text, 
                        title, 
                        '\n'.join([a.text for a in driver.
                                   find_element(By.CLASS_NAME, "ArticleBody-articleBody").
                                   find_elements(By.TAG_NAME, 'p')]))
            writer.writerow([c.author, c.title, c.article])
            print([c.author, c.title, c.article[:50]])
            driver.back()
