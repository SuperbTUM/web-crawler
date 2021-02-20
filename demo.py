from browsermobproxy import Server
from selenium import webdriver
import time
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options


server = Server(r"browsermob-proxy")
server.start()
proxy = server.create_proxy()
chrome_options = Options()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
sel = webdriver.Chrome(executable_path=r'chromedriver.exe', chrome_options=chrome_options)
login_url = ''
proxy.new_har("demo", options={'captureHeaders': True, 'captureContent': True})
sel.get(login_url)
time.sleep(2)
result = proxy.har
print(result)


server.stop()
sel.quit()

