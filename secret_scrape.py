# TODO add janglo jobs to here and make cronjob to update this once a day
# problem - janglo has unpredictable size, how do you differentiate jobs?
# cronjob can be done in windows with task scheduler
# TODO don't add duplicate records! namely, add a primary key
# in the meantime can use this
# SELECT DISTINCT Title, Company FROM jobs WHERE Date BETWEEN datetime('now', '-3 days') AND datetime('now', 'localtime');

# -*- coding: utf-8 -*-
import csv
import datetime
import urllib.request
import sqlite3
from sqlite3 import Error
from bs4 import BeautifulSoup
from dateutil import parser

"""
Scrapes Secret Tel Aviv jobs board, adds new jobs into a database
"""


def update_db():
    try:
        conn = sqlite3.connect('jobs.db')
        c = conn.cursor()

        # call the scraping functions
        soup = scrape_secret()
        jobs = clean_jobs(soup)
        result = organise(jobs)
        excel_data = data_cleanser(result)
        export_to_excel(excel_data)

        # after exporting to csv (just in case) we delete the title row and convert nested lists to tuples
        del excel_data[0]
        new_result = [tuple(l) for l in excel_data]
        # only necessary once
        # c.execute('''CREATE TABLE jobs (Title, Company, Location, Type, Date Posted)''')

        c.executemany("INSERT INTO jobs VALUES (?,?,?,?,?)", new_result)
        conn.commit()
        conn.close()

    except Error as e:
        print(e)


# function to remove multiple occurrences of one term ('new')
def remove_value_from_list(the_list, val):
    return [value for value in the_list if value != val]


def length_enforcer(the_list, length):
    return [value for value in the_list if len(value) == length]


# hit the website and scrape the first page
def scrape_secret():
    url = "https://jobs.secrettelaviv.com/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req)
    return BeautifulSoup(page, "html.parser")


def clean_jobs(soup):
    # jobs are in 'spans'
    all_spans = soup.find_all("span")
    jobs = [span.get_text().strip() for span in all_spans]
    # remove extraneous elements
    rem_list = ['',
                'Subscribe to our EVENTS Newsletter',
                'Join our facebook GROUP']
    for removal_string in rem_list:
        jobs.remove(removal_string)
    jobs = remove_value_from_list(jobs, '')
    return remove_value_from_list(jobs, 'new')


def organise(jobs):
    # make list of lists
    result = [["Title", "Company", "Location", "Duplicate", "Type", "Date Posted"]]
    new_list = []
    for job in jobs:
        if len(new_list) == 6:
            a = list(new_list)
            result.append(a)
            new_list = [job]
        else:
            new_list.append(job)
    result.append(new_list)
    return length_enforcer(result, 6)


def data_cleanser(result):
    for i in result:
        del i[3]
        try:
            i[4] = parser.parse(i[4])
        except ValueError:
            pass
    return result


def export_to_excel(result):
    csvfile = "secret_today" + datetime.datetime.today().strftime('%m-%d') + ".csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(result)


if __name__ == '__main__':
    update_db()
