import urllib.request
from bs4 import BeautifulSoup
#http://www.janglo.net/index.php?option=com_adsmanager&page=show_category&catid=77&order=0&expand=-1&Itemid=160
janglo = "http://www.janglo.net/index.php?option=com_adsmanager&page=show_category&catid=77&order=0&expand=-1&Itemid=160" \
         "ad_jobtag,/mn_adprice,0/mx_adprice,0/ad_nrooms,/expand,1/Itemid,160/limit,20/limitstart,20/"

page = urllib.request.urlopen(janglo)

soup = BeautifulSoup(page, "html.parser")
all_links = soup.find_all("a")
for link in all_links:
    if link.get("href")[:31] == 'index.php?option=com_adsmanager':
        print (link.get_text().rstrip())
