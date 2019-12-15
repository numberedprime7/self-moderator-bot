
#this is your captcha bypass URL
#obtain this url from https://bitcointalk.org/captcha_code.php
login_url = 'captcha_url_goes_here'

#enter your username here. It must be in quotes
username = 'username_goes_here'

#this is taking your forum password to allow you to login on line 57. 
#you can optionally comment out line 12, uncomment line 13, and enter your password inside the quotes
#if your password has 'single quotes' you must use "double quotes" around your password and vice versa if you decide to hard code your pw
password = input('enter your forum password')
#password = 

#this is the thread number you are moderating
#do not use quotes
thread_number = 
#enter the UID of each person you do not want posting in your thread, seperate each UID by a comma
#do not use quotes
banned_users = []

#enter how frequently you wish to review your thread for banned posters, in seconds, minimum 1
frequency = 10

#mac
chrome_driver_path = '/usr/local/bin/chromedriver'
#linux 
#chrome_driver_path = '/usr/bin/chromedriver'
#windows
#chrome_driver_path = 'chromedriver.exe'

from splinter import Browser
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import numpy as np
from datetime import datetime
import time
import warnings

#ignore warnings
warnings.filterwarnings("ignore")

#get_ipython().system('which chromedriver')
#if you are not sure where your chromedriver is, you can run this code in a jupyter notebook

#use this if you are running on a mac or linux computer/machine
executable_path = {'executable_path': chrome_driver_path}
browser = Browser('chrome', **executable_path, headless=False)

#access captcha bypass login page
browser.visit(login_url)

#login
browser.fill('user', username)
browser.fill('passwrd', password)
browser.check('cookieneverexp')
active_web_element = browser.driver.switch_to_active_element()
active_web_element.send_keys(Keys.ENTER)



def window(page_posts):
    for post in np.arange(0, len(page_posts)):
        try:
            meta = page_posts[post].find('td', class_='poster_info')
            uid = meta.find('a')
            uid = str(uid)
            uid = uid.split('href="')[1].split('u=')[1].split('"')[0]
            uid = int(uid) #uid is the UID of the poster
            tme = page_posts[post].find_all('div', class_='smalltext')[1]
            tme = str(tme)
            today_check = tme.split('Today')
            today_check_len = len(today_check)
            if today_check_len ==1: #this means the post was not made 'today'
                tme = tme.split(', ')[2].split('<')[0]
            if today_check_len == 2:
                tme = tme.split('at ')[1].split('<')[0]
            timestamp = datetime.strptime(tme, '%I:%M:%S %p')#this escapes out of the ad-blocker css fake posts
            #if the script is viewing a fake post, an error will be thrown, and the 'try' function will move on to the next post
            for user in banned_users:
                if user == uid:
                    delete_link = page_posts[post].find('a', onclick="return confirm('Remove this message?');")
                    delete_link = str(delete_link)
                    delete_link = delete_link.split('href="')[1].split('" onclick=')[0]  
                    browser.visit(delete_link)
            
            #end of function
        except Exception as e:
        #when a fake post is reviewed, the script will move on to the next one



def page_visit():
    thread_url = f'https://bitcointalk.org/index.php?topic={thread_number}.0'
    browser.visit(thread_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
    page_posts = soup.find_all('td', class_='windowbg')
    page_posts2 = soup.find_all('td', class_='windowbg2')
    window(page_posts)
    window(page_posts2)
    page_num = 0
    time.sleep(1)
    last_page = False
    while last_page == False:

        try:
            browser.click_link_by_partial_href(f'.org/index.php?topic={url}.{page_num}')
            html = browser.html
            soup = BeautifulSoup(html, 'html.parser')
            page_posts = soup.find_all('td', class_='windowbg')
            page_posts2 = soup.find_all('td', class_='windowbg2')
            window(page_posts)
            window(page_posts2)
            page_num = page_num + 20
            time.sleep(1)
        except:
            last_page = True



continue_checking = True
while continue_checking == True:
    page_visit()
    time.sleep(frequency)

