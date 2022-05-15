from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
import time

chrome_options = webdriver.ChromeOptions();
chrome_options.headless = True
chrome_options.add_argument("log-level=3")
chrome_options.add_experimental_option("excludeSwitches", ['enable-automation']);
driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
driver2 = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

wiki_links = "https://designlab.eng.rpi.edu/edn/projects/capstone-support-dev/wiki"
driver.get(wiki_links)
time.sleep(1)

wikipages = driver.find_elements_by_xpath('//a[@class="wiki-page"]')
count = 1
for page in wikipages:
	print("{}: {}".format(count, page.get_attribute('textContent')))
	link = page.get_attribute('href')
	driver2.get(link)
	paragraphs = driver2.find_elements_by_xpath('//p')
	for p in paragraphs: print(p.text)
	count += 1
driver.quit()
driver2.quit()