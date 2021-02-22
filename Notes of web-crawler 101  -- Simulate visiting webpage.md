# Notes of web-crawler 101  -- Simulate visiting webpage

Author: Mingzhe Hu                                                                 To be continued

0. First in first

   Check the robots.txt of the webpage and get to know what information and user-agent are available. 

1. Requests

   The Requests module is easy to handle and friendly to a newcomer in the era of web-crawler. For a rather simple HTTP Get/Post request, by calling `requests.get/post` function with headers and data, you can get the source code of the requested web page. Through accessing the text of the response, you can get the string format of the source code. Transforming the reponse into a json format is also an option, as you can parser the response to a more readable one. The key of this basic request function is the settings of the parameters -- data and header. The data, like user name and password, is inevitable in a classic login action. The header, should contain user-agent (simulate you are using browser), referer (locate the previous URL), cookies, etc.

   For a classic login action, user name and password should be passed into the request body. Inspect the webpage to ensure what kind of data a request needs. There are two possibilities: **Form Data** and **Request Payload**. No obvious difference between these two, the major difference is that these two submit the content differently: one in x-www-form-urlencoded, one in json. Frankly speaking, if the content is Form Data, the request's parameter should be `data`, otherwise it should be `json`.

   Once successfully logged in, cookies may be produced to maintain the login status. The explanation of the existence of cookies could be: a TCP end-to-end connection is time-consuming, so once the connection is built, we can set the connection in a **keep-alive** status and attach an expired date to the connection to save time. The key facts of the connection could be stored as cookies. Typically for a login action, SessionId will be stored to simplify latter requests, especially when you frequently access the information only available after logging in. The cookies are stored in the browser. That means when you log in through Chrome, the cookies won't help for Microsoft Edge. To leverage the cookies, we need to create a session. Make full use of class `requests.Session()` to avoid entering repeated personal information at all times.

   A straightforward way to load cookies is to manully transfer it to a string format. However, there is a more elegant way, thanks to `http.cookiejar`. Cookies could be saved in a local text file in either Mozilla or LWP format (Personally recommend). Cooperating with `urllib.request`, post/get request can export & import cookies implicitly instead of storing it in variables. The following code shows how it works:

   ```python
   cookies = http.cookiejar.LWPCookieJar()
   handler = urllib.request.HTTPCookieProcessor(cookies)
   opener = urllib.request.build_opener(handler)
   response = opener.open(url)
   cookies.save(ignore_discard=True, ignore_expires=True)
   
   cookies.load(filename, ignore_discard=True, ignore_expires=True)
   req = request.Request(url)  # Init, This can be replaced by session
   opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookies))
   response = opener.open(req)
   ```

   One tip for grasping the login URL is to type incorrect password to prevent page jump.

   A more popular opensource module is `requests-html`, available through pip install. Similar to requests, session can be created via class HTMLSession(). Also, elements can be find with response.html.find() and its css selector.

2. Selenium

   This module is recognized as a less efficient but more authentic way of visiting webpage with browser.

   Start with the proxy. Use `browsermobproxy` even though selenium does have its server module.

   Submodule `webdriver` is of great importance.

   Issue 1: Dealing with unofficial CA certificates.

   There is no denying that more and more platforms like Apple Store demands their product to be HTTPs instead of mere HTTP. Based on such fact, certificate authentication has to be proceed before a webpage is opened. If you are confronted with a warning, declaring the web's certificate is not trustworthy, and you insist on visiting it, you need to ignore the warning. This is not a risk, sometimes. The reason why such issue happens is that the certificate may be authenticated by the platform itself. There are a lot of commands that can ignore this warning. In selenium, just add an argument: `'--ignore-certificate-errors'`, everything will be fine.
   
   Issue 2: Dealing with uninteractive elements.
   
   Another annoying fact is that when you intend to click something, like a button, you may get an error, saying the request element is not interactable. This is because the element is hidden unless you put your mouse on the right place. Simulating this action is the solution to this problem. First find the element, then excuate `ActionChains(driver).move_to_element(element).perform()`. Everything will be fine.