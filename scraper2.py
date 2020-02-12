    # -*- coding: utf-8 -*-


import bs4

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, random
import time
import random


URL = "http://127.0.0.1:8001"
USE_SLEEP = 1
USE_SHUFFLE = 1
USE_SEARCH = 1
USE_CONTACT = 1

def random_sleep(min=1, max=10):
    time.sleep(random.randrange(min, max, 1))


class Vacancy:
    def __init__(self, name, salary, company_name, city, link):
        self.name = name
        self.salary = salary
        self.company_name = company_name
        self.city = city
        self.link = link
        
    def __str__(self):
        return "{};{};{};{};{}".format(self.name, self.salary, self.company_name, self.city, self.link)


def get_page_url(id):
    if id == 1:
        page_url = URL
    else:
        page_url = URL + "/?vacancy=" + str(id)
    print(page_url)
    return page_url   
   
    
def parse_page_to_links(html):
    ''' Returns list of links to vacancies '''
    links = []
    soup = bs4.BeautifulSoup(html, 'html.parser')
    vacancies = soup.findAll("div", {"class": "card"})
    for vacancy in vacancies:
        vacancy_href = vacancy.h2.a["href"] # e.g. '/vacancy/1/'
        link = URL + vacancy_href
        links.append(link)
    return links


def get_vacancy(driver, link):
    ''' Returns Vacancy object '''
    if USE_SLEEP:
        print("LOG: START SLEEP")
        random_sleep()
        print("LOG: STOP SLEEP")
        
        
    driver.get(link)
    vacancy_html = driver.page_source
    soup = bs4.BeautifulSoup(vacancy_html, 'html.parser')
    vacancy_code = soup.findAll("div", {"class": "container"})
    vacancy = vacancy_code[1]
    return Vacancy(vacancy.h1.text, vacancy.h2.text, vacancy.h3.text, vacancy.p.text, link)


def login(username, password, driver):
    print("LOG: START LOGIN")
    driver.get("http://127.0.0.1:8001/accounts/login/")
    time.sleep(2)
    print("START")
    driver.find_element_by_name("username").send_keys(username)
    time.sleep(2)
    driver.find_element_by_name("password").send_keys(password)
    time.sleep(2)
    
    driver.find_element_by_css_selector("#page-content > div > form > div:nth-child(5) > button").click() # It works
    print("LOG: END LOGIN")
 
 ####################################################################
 
driver = webdriver.Firefox()
login("virus1", "hofide93", driver)
vacancies = []

for i in range(1, 3):
    if USE_SEARCH:
        prev_url = driver.current_url
        driver.get(URL)
        time.sleep(4)
        buttons = driver.find_elements_by_xpath("/html/body/div/div/div/div[1]/div[1]/form/div/div[3]/button")
        buttons[0].click()
        driver.get(prev_url)
    url = get_page_url(i)
    driver.get(url)
    html = driver.page_source # html code of the page
    links = parse_page_to_links(html) # all links to vacancies
    if USE_SHUFFLE:
        random.shuffle(links)
    for link in links:
        #print(i, links)
        vacancy = get_vacancy(driver, link)
        vacancies.append(vacancy)

for vacancy in vacancies[:-1]:
    print(vacancy)
