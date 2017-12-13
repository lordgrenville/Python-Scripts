#TODO add janglo jobs to here and make cron job to update this once a day
#TODO don't add duplicate records!

import csv
import datetime
import urllib.request
import sqlite3
# from sqlite3 import Error
from bs4 import BeautifulSoup

"""
Scrapes Secret Tel Aviv jobs board, adds new jobs into a database
"""

def update_db():
    """
create a database connection and save it
    """ 
    try:
        conn = sqlite3.connect('jobs.db')
        c=conn.cursor()
    except Error as e:
        print(e)
    
    #call the scraping functions
    soup = scrape_secret()
    jobs = clean_jobs(soup)
    result = organise(jobs)
    export(result)

    #after exporting to csv (just in case) we delete the title row and convert nested lists to tuples
    del result[0]
    new_result = [tuple(l) for l in result]
    # only necessary once
    # c.execute('''CREATE TABLE jobs (Title, Company, Location, Duplicate, Type, Date Posted)''')

    c.executemany("INSERT INTO jobs VALUES (?,?,?,?,?,?)", new_result)
    conn.commit()
    conn.close()
 
#function to remove multiple occurences of one term ('new')
def remove_values_from_list(the_list, val):
    return [value for value in the_list if value != val]

def length_enforcer(the_list, length):
    return [value for value in the_list if len(value) == length]

#hit the website and scrape the first page
def scrape_secret():
    URL = "https://jobs.secrettelaviv.com/"
    req = urllib.request.Request(URL, headers={'User-Agent': 'Mozilla/5.0'})
    page = urllib.request.urlopen(req)
    return BeautifulSoup(page, "html.parser")

def clean_jobs(soup):
    #jobs are in 'spans'
    all_spans = soup.find_all("span")
    jobs = []
    for span in all_spans:
        jobs.append(span.get_text().strip())
    #remove extraneous elements
    jobs.remove('')
    jobs.remove('Subscribe to our EVENTS Newsletter')
    jobs.remove('Join our facebook GROUP')
    jobs = remove_values_from_list(jobs, '')
    return remove_values_from_list(jobs, 'new')

def organise(jobs):
    #make list of lists
    result = [["Title","Company","Location","Duplicate", "Type", "Date Posted"]]
    new_list = []
    for job in jobs:
        if len(new_list) == 6:
            a = list(new_list)
            result.append(a)
            new_list = [job]
        else:
            new_list.append(job)
    result.append(new_list)
    result = length_enforcer(result,6)
    return result

def export(result):
    #export as CSV
    csvfile = "secret_today" + datetime.datetime.today().strftime('%m-%d') + ".csv"
    with open(csvfile, "w") as output:
        writer = csv.writer(output, lineterminator='\n')
        writer.writerows(result)

if __name__ == '__main__':
    update_db()