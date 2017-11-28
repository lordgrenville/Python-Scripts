import urllib.request
from bs4 import BeautifulSoup
import csv
import datetime

#function to remove multiple occurences of one term ('new')
def remove_values_from_list(the_list, val):
   return [value for value in the_list if value != val]

#hit the website and scrape the first page
secret = "https://jobs.secrettelaviv.com/"
req = urllib.request.Request(secret, headers={'User-Agent': 'Mozilla/5.0'})
page = urllib.request.urlopen(req)

soup = BeautifulSoup(page, "html.parser")

#job are in 'spans'
all_spans = soup.find_all("span")
jobs = []
for span in all_spans:
    jobs.append(span.get_text().strip())

#remove extraneous elements
jobs.remove('')
jobs.remove('Subscribe to our EVENTS Newsletter')
jobs.remove('Join our facebook GROUP')
jobs = remove_values_from_list(jobs, 'new')

#make list of lists
result = [["Title", "Company", "Location", "Type", "Date Posted"]]
new_list = []
for job in jobs:
    if len(new_list) == 6:
        a = list(new_list)
        result.append(a)
        new_list = [job]
    else:
        new_list.append(job)
result.append(new_list)

#export as CSV
csvfile = "secret_today" + datetime.datetime.today().strftime('%m-%d') + ".csv"
with open(csvfile, "w") as output:
    writer = csv.writer(output, dialect='excel')
    writer.writerows(result)
