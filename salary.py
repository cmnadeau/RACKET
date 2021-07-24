from selenium import webdriver
from bs4 import BeautifulSoup as bsoup
import pandas as pd

"""
A web scraper to return payroll data from FY 2020 at
the University of Rhode Island

Written by Christopher Nadeau
"""

#Driver configuration
driver = webdriver.Firefox()

year = []
employer = []
name = []
title = []
annual_wages = []
source = []
pages = [x for x in range(1,32)] #Number of pages of information

"""
Parser for payroll information, iterating over the each page of results

"""
for page in pages:
        driver.get(f"https://www.openthebooks.com/rhode-island-state-employees/?Year_S=2020&Emp_S=University%20of%20Rhode%20Island&pg={page}")

        content = driver.page_source
        soup = bsoup(content, features='lxml')

        flag = True #skip first tr because it returns NoneType

        for tr in soup.find_all('tr'):
                if flag:
                        flag = False
                        pass
                else:
                        yr = tr.find('td')
                        employer2 = yr.next_sibling.next_sibling
                        employee = employer2.next_sibling.next_sibling
                        job = employee.next_sibling.next_sibling
                        salary = job.next_sibling.next_sibling
                        src = salary.next_sibling.next_sibling

                        year.append(yr.text.lstrip())
                        employer.append(employer2.text.lstrip())
                        name.append(employee.text.lstrip())
                        title.append(job.text.lstrip())
                        annual_wages.append(salary.text.lstrip())
                        source.append(src.text.lstrip())

frame = pd.DataFrame({'Year':year, 'Name':name, 'Title':title, "Salary":annual_wages})
frame.to_csv('2020salaries.csv', index=False, encoding='utf8')
