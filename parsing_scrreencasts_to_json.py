import requests
import json
from bs4 import BeautifulSoup
from selenium import webdriver
import os
import urllib
from time import sleep
import atexit

Username = ""
Password = ""
browser = webdriver.Chrome()

def saveToJSON():
    global browser
    prettyScreencast = json.dumps(Screencasts, sort_keys=True, indent=2, separators=(',', ': '))
    with open("screencasts.json", "w") as json_file:
        json_file.write(prettyScreencast)

atexit.register(saveToJSON)

def sign_in():
    global browser,Username,Password
    sign_in_url = "http://www.codeschool.com/users/sign_in"
    browser.get(sign_in_url)
    browser.find_element_by_id("user_login").clear()
    browser.find_element_by_id("user_login").send_keys(Username)
    browser.find_element_by_id("user_password").clear()
    browser.find_element_by_id("user_password").send_keys(Password)
    browser.find_element_by_xpath("//div[@id='sign-in-form']/form/div/div/button").click()

def readAScreenCast(link):
    global browser
    browser.get('https://codeschool.com' + link)
    sleep(2)
    html = browser.page_source
    soup = BeautifulSoup(html ,'lxml')
    return soup.find('a',{'class','tag'}).text, soup.find('span',{'class','has-tag--heading tci'}).text , soup.find('video')["src"]
    
def getScreenCastLinks():
    global browser
    Links = []
    shows = ['https://www.codeschool.com/screencasts']
    for show in shows:
        browser.get(show)
        sleep(2)
        html = browser.page_source
        soup = BeautifulSoup(html, 'lxml')
        pages = soup.findAll('a',{'class','video-page-link'})
      	for pagination in range(0, len(pages)-1):
            for link in soup.findAll('a',{'class','twl'}):
                Links.append(link['href'])
            browser.find_element_by_css_selector('a.video-page-link:last-of-type').click()
            sleep(2)
            html = browser.page_source
            soup = BeautifulSoup(html, 'lxml')
    
    return Links

sign_in()
Links = getScreenCastLinks()

Screencasts = []
for index, link in enumerate(Links):
    screencast = {
    "name":"",
    "url":"",
    "path":""
    }
    screencast['path'], screencast['name'], screencast['url'] = readAScreenCast(link)

    if screencast['path'] == "HTML/CSS":
        screencast['path'] = "HTML&CSS"
    elif screencast['path'] == ".NET":
        screencast['path'] = "dot NET"

    print screencast['name']
    Screencasts.append(screencast)
