from selenium import webdriver


browser = webdriver.Chrome(executable_path='/usr/lib/chromium-browser/chromedriver')
browser.get('http://localhost:8080')

assert 'Django' in browser.title