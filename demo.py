from browsermobproxy import Server
from selenium import webdriver
import time
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs


server = Server(r"browsermob-proxy-2.1.4-bin\browsermob-proxy-2.1.4\bin\browsermob-proxy")
server.start()
proxy = server.create_proxy()
chrome_options = Options()
chrome_options.add_argument('--proxy-server={0}'.format(proxy.proxy))
chrome_options.add_argument('--ignore-certificate-errors')
sel = webdriver.Chrome(executable_path=r'Google\Chrome\Application\chromedriver.exe', chrome_options=chrome_options)
login_url = ''  # to be filled
proxy.new_har("demo", options={'captureHeaders': True, 'captureContent': True})
sel.get(login_url)
time.sleep(2)
result = proxy.har

content = sel.page_source
soup = bs(content, 'html.parser')
time.sleep(10)
processed_data = soup.find('xxx', attrs={'class': 'xxx'})  # to be filled
time.sleep(2)
Icon = processed_data['xxx']
print(Icon)

time.sleep(2)
server.stop()
sel.quit()
