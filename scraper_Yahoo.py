from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

options = Options()
# options.add_argument("--headless=new")
options.page_load_strategy = 'eager'

from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.remote_connection import LOGGER, logging
LOGGER.setLevel(logging.WARNING)

import csv, time

class Content:
  def __init__(self, author, title, article):
    self.author = author
    self.title = title
    self.article = article

driver = webdriver.Chrome(options=options)

with open('Yahoo_output_all.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Author', 'Title', 'Content'])
    driver.get('https://finance.yahoo.com/topic/economic-news')

    # i = 0
    # SLEEP_TIME = 1;

    # while i < 3:
    #     html = driver.find_element(By.TAG_NAME, 'html')
    #     html.send_keys(Keys.END)
    #     time.sleep(SLEEP_TIME)
    #     i += 1
    #     print(f'Scrolling {i}')
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    links = []
    for elem in elems:
      link = [a for a in elem.get_attribute("href").split('/') if a != '']
      if len(link) > 3:
        if link[1] in ['finance.yahoo.com'] and link[2] in ['news', 'm']:
          link[0] = link[0] + '/'
          links.append('/'.join(link))
    
    driver.get(links[0])
    read_more = driver.find_element(By.TAG_NAME, 'button').\
                                    find_element(By.CLASS_NAME, 'collapse-button')
    read_more.click()
    c = Content(
      author=driver.find_element(By.CLASS_NAME, 'caas-author-byline-collapse').text,
      title=driver.find_element(By.CLASS_NAME, 'caas-title-wrapper').text,
      article='\n'.join([a.text for a in driver.\
                                   find_element(By.CLASS_NAME, "caas-body").\
                                   find_elements(By.TAG_NAME, 'p')])
    )
    print(c.author, c.title, c.article)
    
    