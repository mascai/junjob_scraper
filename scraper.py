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

URL = "http://127.0.0.1:8001"

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
        vacancy_href = vacancy.h1.a["href"] # e.g. '/vacancy/1/'
        # print(vacancy_href)
        link = URL + vacancy_href
        links.append(link)
    return links


def get_vacancy(driver, link):
    ''' Returns Vacancy object '''
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
login("admin", "********", driver)
vacancies = []

for i in range(1, 4):
    url = get_page_url(i)
    driver.get(url)
    html = driver.page_source # html code of the page
    links = parse_page_to_links(html) # all links to vacancies
    for link in links:
        vacancy = get_vacancy(driver, link)
        vacancies.append(vacancy)

for vacancy in vacancies:
    print(vacancy)

'''
EXAMPLE OF OUTPUT

LOG: START LOGIN
START
LOG: END LOGIN
http://127.0.0.1:8001
http://127.0.0.1:8001/?vacancy=2
http://127.0.0.1:8001/?vacancy=3
C++ developer;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/1/
Go developer;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/2/
C++ quant;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/3/
C++ QT developer;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/4/
C++ quant;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/5/
C / C++ engeneer;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/6/
Java developer;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/7/
C++ quant;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/8/
Analyst;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/9/
Java;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/10/
C++ quant;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/11/
SAS analyst;40.000;Company1;Москва;http://127.0.0.1:8001/vacancy/12/

'''
