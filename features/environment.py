import os
import threading
from wsgiref import simple_server
from wsgiref.simple_server import WSGIRequestHandler
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from app import create_app

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument('--no-proxy-server')
chrome_options.add_argument("--proxy-server='direct://'")
chrome_options.add_argument("--proxy-bypass-list=*")


def before_all(context):
  context.server = simple_server.WSGIServer(("", 5000), WSGIRequestHandler)
  app = create_app(os.getenv('APP_CONFIG') or 'testing')
  context.server.set_app(app)
  context.pa_app = threading.Thread(target=context.server.serve_forever)
  context.pa_app.start()

  context.browser = webdriver.Chrome(options=chrome_options)
  context.browser.set_page_load_timeout(time_to_wait=200)


def after_all(context):
  context.browser.quit()
  context.server.shutdown()
  context.pa_app.join()
