from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from time import sleep

driver = webdriver.Remote(
command_executor="http://selenium-svc:4444/wd/hub",
options=webdriver.ChromeOptions()
)

while True:
  driver.get("http://flask1-svc:5001/endpoint1")
  sleep(2)
  driver.get("http://flask2-svc:5002/endpoint1")
  sleep(2)
  driver.get("http://flask3-svc:5003/endpoint1")
  sleep(2)
  driver.get("http://flask4-svc:5004/endpoint1")
  sleep(2)
  driver.get("http://flask5-svc:5005/endpoint1")
  sleep(2)
  driver.get("http://flask6-svc:5006/endpoint1")
  sleep(2)
  driver.get("http://flask7-svc:5007/endpoint1")
  sleep(2)
  driver.get("http://flask8-svc:5008/endpoint1")
  sleep(2)
  driver.get("http://flask11-svc:5011/endpoint1")
  sleep(2)
driver.quit()
