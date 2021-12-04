import os

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
proxies = {
    'https':'https://140.227.239.66:3128'
}

def get_indexes():
    dir = 'NarouData'
    files = os.listdir(dir)
    files = [f.split('.')[0] for f in files]
    print(f'get indexes at {len(files)}')
    print(files[:10])
    return files

def build_narou_query():
    urls = list()
    years = list(range(2019, 2015, -1))
    url_header = "https://yomou.syosetu.com/search.php?type=re&minfirstup={year1}%2F{month1}%2F{day1}&maxfirstup={year2}%2F{month2}%2F{day2}&genre=102-307&order=hyoka"
    for year in years:
        url1 = url_header.format(year1 = year, month1 = "04", day1 = "01", year2 =   year , month2 = "09", day2 = "30")
        urls.append(url1)
        if year != 2021:
            url2 = url_header.format(year1 = year, month1 = "10", day1 = "01", year2 =   year + 1 , month2 = "03", day2 = "31")
            urls.append(url2)
    return urls

def get_index():
    urls = build_narou_query()
    for url in urls:
        sleep(1.0)
        for page in range(1, 101):
            sleep(1.0)
            url_page = url + f"&p={page}"
            print(f' index url : {url_page}')
            response = requests.get(url_page, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')
            novel_hs = soup.find_all(class_='novel_h')
            if novel_hs == None:
                break
            hrefs = list()
            for h in novel_hs:
                href = h.find('a').get('href')
                hrefs.append(href)
            print(f'length of hrefs {len(hrefs)}')
            yield hrefs

if __name__=='__main__':
    get_index()
