# TODO add janglo jobs to here and make cronjob to update this once a day
# problem - janglo has unpredictable size, how do you differentiate jobs?
# cronjob can be done in windows with task scheduler
# TODO don't add duplicate records! namely, add a primary key
# -*- coding: utf-8 -*-
import csv
import datetime
import urllib.request
import sqlite3

import bs4
from dateutil import parser

"""
Scrapes Secret Tel Aviv jobs board, adds new jobs into a database
"""


def update_db():
    """
    Calls subfunctions for scraping, exporting to excel and RDB
    """
    with sqlite3.connect('jobs.db') as con:
        # call the scraping functions
        soup = scrape_secret()
        jobs = clean_jobs(soup)
        result = organise(jobs)
        excel_data = data_cleanser(result)
        export_to_excel(excel_data)

        # after exporting to csv (just in case) we delete the title row and the last row (it's not a job)
        # and convert nested lists into tuples (necessary for the sqlite3 import)
        del excel_data[0]
        del excel_data[200]
        new_result = [tuple(l) for l in excel_data]
        # only necessary once
        # con.execute('''CREATE TABLE jobs (Title, Company, Location, Type, Date Posted)''')

        con.executemany("""
            INSERT INTO 
                jobs 
            VALUES (?, ?, ?, ?, ?)""", new_result)


def remove_value_from_list(the_list, val):
    """
    removes multiple occurrences of a given term
    """
    return [value for value in the_list if value != val]


def length_enforcer(the_list, length):
    """
    remove from list of tuples those which go above a given length
    """
    return [value for value in the_list if len(value) == length]


def scrape_secret():
    """
    hit the website and scrape the first page
    """
    url = "https://jobs.secrettelaviv.com/"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req)
    # jobs are in spans
    parse_only = bs4.SoupStrainer('span')
    return bs4.BeautifulSoup(page, "lxml", parse_only=parse_only)


def clean_jobs(soup):
    """
    tidy the data - first steps
    """
    jobs = [span.get_text().strip() for span in soup.findChildren()]
    # remove extraneous elements
    rem_list = ['',
                'Subscribe to our EVENTS Newsletter',
                'Join our facebook GROUP']
    for removal_string in rem_list:
        jobs.remove(removal_string)
    jobs = remove_value_from_list(jobs, '')
    return remove_value_from_list(jobs, 'new')


def organise(jobs):
    """
    make list of lists
    """
    result = []
    new_list = []
    for job in jobs:
        if len(new_list) == 7:
            a = list(new_list)
            result.append(a)
            new_list = [job]
        else:
            new_list.append(job)
    result.append(new_list)
    return length_enforcer(result, 7)


def data_cleanser(result):
    """
    complete data cleaning, add headers
    """
    for i in result:
        del i[1]
        del i[2]
        try:
            i[4] = parser.parse(i[4])
        except ValueError:
            pass
    result.insert(0,["Title", "Company", "Location", "Type", "Date Posted"])
    return result


def export_to_excel(result):
    """
    writes data to csv and saves as such
    """
    csvfile = "secret_today" + datetime.datetime.today().strftime('%m-%d') + ".csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(result)


if __name__ == '__main__':
    update_db()
