from selenium import webdriver
from selenium.webdriver.common.by import By

class Content:
  def __init__(self, author, article):
    self.author = author
    self.article = article

driver = webdriver.Chrome()
driver.get('https://www.cnbc.com/business/')
titles_el = driver.find_elements(By.CLASS_NAME, "Card-title")
titles = [t.text for t in titles_el]
titles_el[0].click()
article = '\n'.join([a.text for a in driver.find_element(By.CLASS_NAME, "ArticleBody-articleBody").find_elements(By.TAG_NAME, 'p')])
c = Content(driver.find_element(By.CLASS_NAME, "Author-authorName").text, article)
print(c.author, c.article)
