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
    dir = r'C:\Users\Atsuya\PycharmProjects\NarouScraping\ModernRenai'
    files = os.listdir(dir)
    files = [f.split('.')[0] for f in files]
    print(f'get indexes at {len(files)}')
    print(files[:10])
    return files

month_days = {1: 31, 2: 28, 3:31, 4:30, 5:31, 6:30, 7:31, 8:31, 9:30, 10:31, 11:30, 12:31}

def build_narou_query():
    urls = list()
    years = list(range(2010, 2005, -1))
    url_header = "https://yomou.syosetu.com/search.php?minfirstup={year1}%2F{month1}%2F{day1}&maxfirstup={year2}%2F{month2}%2F{day2}&genre=102&order=hyoka"
    for year in years:
        for month in range(1, 13):
            if year == 2021 and month in [11, 12]:
                pass
            else:
                day2 = month_days[month]
                urls.append(url_header.format(year1 = year, month1 = str(month).zfill(2), day1 = "01" , year2 =   year , month2 = str(month).zfill(2), day2 = str(day2)))
    return urls

def get_index():
    urls = build_narou_query()
    for url in urls:
        sleep(1.0)
        for page in range(1, 101):
            sleep(2.0)
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
