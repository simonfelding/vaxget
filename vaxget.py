#!/usr/bin/python3

# COVID-19 vax getter

# 1. get survey link

from bs4 import BeautifulSoup
import requests
from datetime import date

URL = 'https://www.regionh.dk/presse-og-nyt/pressemeddelelser-og-nyheder/Sider/Tilmelding-til-at-modtage-overskydende-vaccine-mod-COVID-19.aspx'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
survey = soup.find('a', href=True, text='Tilmeld dig dagens liste')['href']
print(f"{date.today()}: today url is {survey}")
# 2. get friends

##name
##age
##address
##postnoby
##tlf
##vaccinested

import yaml

with open("/home/pi/covid19-autofill/vaxlist.yaml", 'r') as stream:
    try:
        vaxlist = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

# 3. fill out survey

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from random import uniform as randint

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

for name in vaxlist:
    friend = vaxlist[name]
    if friend['lastvax'] == str(date.today()):
        print(f"{friend['name']} was already vaxxed {date.today()}")
        continue
    else:
        vaxlist[name]['lastvax'] = str(date.today())
        with open('/home/pi/covid19-autofill/vaxlist.yaml', 'w') as outfile:
            yaml.dump(vaxlist, outfile, default_flow_style=False, allow_unicode=True)


    driver.get(survey)
    # assert "Tilmelding til at modtage overskydende vaccine mod COVID-19"

    # 1 page: info
    elem = driver.find_element_by_class_name("next-button")
    time.sleep(randint(0.4, 1.8))
    elem.send_keys(Keys.RETURN)
    # 2 page: name
    elem = driver.find_element_by_xpath("//input[@type='text']")
    elem.send_keys(friend['name'])
    time.sleep(randint(2, 4))
    # <input size="60" type="text" name="t50100775" id="t50100775" value="" maxlength="4096">
    elem.send_keys(Keys.RETURN)

    # 3: age
    elem = driver.find_element_by_xpath("//input[@type='text']")
    elem.send_keys(friend['age'])
    time.sleep(randint(0.8,2))
    #<input size="3" type="text" name="n35965768" id="n35965768" value="" maxlength="4096">
    elem.send_keys(Keys.RETURN)

    # 4. address
    elem = driver.find_element_by_xpath("//input[@type='text']")
    elem.send_keys(friend['address'])
    time.sleep(randint(2,5))
    #<input size="60" type="text" name="t50088645" id="t50088645" value="" maxlength="4096">
    elem.send_keys(Keys.RETURN)

    # 5. postno & by
    elem = driver.find_element_by_xpath("//input[@type='text']")
    elem.send_keys(friend['postnoby'])
    time.sleep(randint(2.5,5))
    #<input size="40" type="text" name="t50088674" id="t50088674" value="" maxlength="4096">
    elem.send_keys(Keys.RETURN)

    # 6. tlf
    elem = driver.find_element_by_xpath("//input[@type='text']")
    elem.send_keys(friend['tlf'])
    time.sleep(randint(1,2.5))
    elem.send_keys(Keys.RETURN)

    # 7. radio buttons vax sted
    # Ballerup,
    # Bella Center
    # Bornholm
    # Hillerød
    # Ishøj
    # Øksnehallen
    # Snekkerstenhallen

    time.sleep(randint(2.8,5))
    element = driver.find_element_by_xpath("//form/div[1]/div")
    element = element.find_element_by_xpath(f"//label[contains(text(),'{friend['vaccinested']}')]")
    element.click()
    if element:
        elem = driver.find_element_by_class_name("next-button")
        elem.send_keys(Keys.RETURN)
    else:
        print(f"didnt find {friend['vaccinested']} in form!!")

    # 8. dine data
    time.sleep(randint(0.4,1.5))
    elem = driver.find_element_by_class_name("next-button")
    elem.send_keys(Keys.RETURN)

    # 9. submit
    time.sleep(randint(0.5,1.5))
    # <input type="submit" class="next-button" name="next" value="Afslut">
    elem = driver.find_element_by_class_name("next-button")
    if elem.get_attribute("value") == "Afslut":
        elem.send_keys(Keys.RETURN)
        print(f"{date.today()}: Finished vaxxing {friend['name']}.")
        time.sleep(10)
    else:
        print(f"{date.today()}: didn't find finish page for {friend['name']}!!!!")

