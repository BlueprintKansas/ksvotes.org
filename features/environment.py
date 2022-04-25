from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")
chrome_options.add_argument("--lang=en")


def before_all(context):
  context.browser = webdriver.Chrome(options=chrome_options)
  context.browser.set_page_load_timeout(time_to_wait=200)


def after_all(context):
  context.browser.quit()
