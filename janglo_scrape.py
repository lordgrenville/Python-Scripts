import urllib.request
from bs4 import BeautifulSoup

janglo = "http://www.janglo.net/component/option,com_adsmanager/page,show_category/catid,77/text_search,/order,0/" \
         "ad_jobtag,/mn_adprice,0/mx_adprice,0/ad_nrooms,/expand,1/Itemid,160/limit,20/limitstart,20/"

page = urllib.request.urlopen(janglo)

soup = BeautifulSoup(page, "html.parser")
all_links = soup.find_all("a")
for link in all_links:
    if link.get("href")[:31] == 'index.php?option=com_adsmanager':
        print (link.get_text().rstrip())


