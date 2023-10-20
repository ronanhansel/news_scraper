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

    i = 0
    SLEEP_TIME = 1;
    SCROLL_TIME = 15;
    while i < SCROLL_TIME:
        html = driver.find_element(By.TAG_NAME, 'html')
        html.send_keys(Keys.END)
        time.sleep(SLEEP_TIME)
        i += 1
        print(f'Scrolling {i}')
    elems = driver.find_elements(By.XPATH, "//a[@href]")
    links = []
    for no in range(len(elems)):
      elem = elems[no]
      try:
        link = [a for a in elem.get_attribute("href").split('/') if a != '']
      except StaleElementReferenceException:
        print('Stale Element. Retrying...')
        elems = driver.find_elements(By.XPATH, "//a[@href]")
        elem = elems[no]
        link = [a for a in elem.get_attribute("href").split('/') if a != '']
      if len(link) > 3:
        if link[1] in ['finance.yahoo.com'] and link[2] in ['news', 'm']:
          link[0] = link[0] + '/'
          links.append('/'.join(link))
    
    print(f'{len(links)} available.')
    
    for l in links:
      driver.get(l)
      c = Content(
        author=driver.find_element(By.CLASS_NAME, 'caas-author-byline-collapse').text,
        title=driver.find_element(By.CLASS_NAME, 'caas-title-wrapper').text,
        article=''.join([a for a in driver.\
                                    find_element(By.CLASS_NAME, "caas-body").\
                                    get_attribute('textContent')])
      )
      print(c.author, c.title, c.article[:50])
      writer.writerow([c.author, c.title, c.article])
      
    