import urllib.request
from bs4 import BeautifulSoup


def janglo_scraper():
    janglo = "http://www.janglo.net/index.php?option=com_adsmanager&page=show_category&catid=77&order=0&expand=-1" \
             "&Itemid=160ad_jobtag,/mn_adprice,0/mx_adprice,0/ad_nrooms,/expand,1/Itemid,160/limit,20/limitstart,20/"

    page = urllib.request.urlopen(janglo)
    jobs = []
    soup = BeautifulSoup(page, "html.parser")
    all_links = soup.find_all("a")
    for link in all_links:
        if link.get("href")[:31] == 'index.php?option=com_adsmanager':
            jobs.append(link.get_text().rstrip())
    return jobs


if __name__ == '__main__':
    janglo_scraper()
