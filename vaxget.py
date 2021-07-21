#!/usr/bin/python3
# COVID-19 vax getter

import yaml

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from datetime import date
from random import uniform as random

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36'
chrome_options = webdriver.ChromeOptions()
chrome_options.set_capability("browserVersion", "71")
chrome_options.set_capability("platformName", "Linux")
chrome_options.add_argument('--headless')
chrome_options.add_argument(f'--user-agent={user_agent}')
#options.add_argument("disable-dev-shm-usage")
chrome_options.add_argument("no-sandbox")

driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub', options=chrome_options)

def fill(friend, debug = 1):
    page = int(driver.find_element_by_xpath("/html/body/div/form/input[2]").get_attribute("value"))
    
    if page == 0: # info
        pass
    elif page == 1: # vaccineret før?
        elem = driver.find_element_by_xpath("//form/div[1]/div")
        elem.find_element_by_xpath(f"//label[contains(text(),'Ja')]").click()
    elif page == 2: # hvilken vaccine? Pfizer, Moderna
        elem = driver.find_element_by_xpath("//form/div[1]/div")
        elem.find_element_by_xpath(f"//label[contains(text(),'{friend['vaccine']}')]").click()
    elif page == 3:
        elem = driver.find_element_by_xpath("//input[@type='text']")
        elem.send_keys(friend['name'])
    elif page == 4:
        elem = driver.find_element_by_xpath("//input[@type='text']")
        elem.send_keys(friend['age'])
    elif page == 5:
        elem = driver.find_element_by_xpath("//input[@type='text']")
        elem.send_keys(friend['address'])
    elif page == 6:
        elem = driver.find_element_by_xpath("//input[@type='text']")
        elem.send_keys(friend['postnoby'])
    elif page == 7:
        elem = driver.find_element_by_xpath("//input[@type='text']")
        elem.send_keys(friend['tlf'])
    elif page == 8:
        elem = driver.find_element_by_xpath("//form/div[1]/div")
        elem.find_element_by_xpath(f"//label[contains(text(),'{friend['vaccinested']}')]").click()
    elif page == 9: # gdpr
        pass
    elif page == 10: # submit
        pass
    
    if debug == 1:
        #driver.save_screenshot("screenshot.png")
        print(f"Finished page {page}, continuing")
    time.sleep(random(0.5, 2))
    driver.find_element_by_class_name("next-button").click()
    if page == 10:
        print(f"{date.today()}: Finished vaxxing {friend['name']}.")
        vaxlist[name]['lastvax'] = str(date.today())

if __name__ == "__main__":
    with open("/home/pi/covid19-autofill/vaxlist.yaml", 'r') as stream:
    try:
        # list of fields:
        # name, vaccineret, age, address, postnoby, tlf, vaccinested
        vaxlist = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

    for name in vaxlist:
        friend = vaxlist[name]
        if friend['lastvax'] == str(date.today()):
            print(f"{friend['name']} was already vaxxed {date.today()}")
            continue
        else:
            driver.get("https://www.survey-xact.dk/LinkCollector?key=JPH8ZGHNL21N")
            while driver.current_url == "https://www.survey-xact.dk/servlet/com.pls.morpheus.web.pages.CoreRespondentCollectLinkAnonymous": 
                fill(friend)
            vaxlist[friend['lastvax']] = str(date.today())
            time.sleep(random(4,8))

    with open('/home/pi/covid19-autofill/vaxlist.yaml', 'w') as outfile:
        yaml.dump(vaxlist, outfile, default_flow_style=False, allow_unicode=True)
