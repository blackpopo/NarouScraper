import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep
import  os

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
url_header = 'https://ncode.syosetu.com'
proxies = {
    'https':'https://140.227.239.66:3128'
}


def get_text(url, gyokan=False):
    # response = requests.get(url, headers=headers, proxies=proxies, verify='certs.pem')
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    text = soup.find(id='novel_honbun')
    texts = [line.text for line in text.find_all('p')]
    texts = [line.replace('\u3000', '') for line in texts]
    if not gyokan:
        texts = [line for line in texts if line != '']
    return texts

def get_page(ncode='n3170ed', gyokan=False):
    url =  url_header+ '/' + ncode + '/'
    print(f'url : {url}')
    # response = requests.get(url, headers=headers, proxies=proxies, verify='certs.pem')
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    print(soup)
    indices = soup.find(class_='index_box')
    if indices == None:
        lines = get_text(url, gyokan)
        with open(ncode + '.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))
    else:
        hrefs = [a['href'] for a in indices.find_all('a')]
        hrefs = sorted(hrefs, key=lambda x: int(x.split('/')[-2]))
        print(f'length of hrefs {len(hrefs)}')
        for href in tqdm(hrefs):
            print(f'Start {href}')
            url = url_header + href
            lines = get_text(url, gyokan)
            sleep(2.0)
            with open(os.path.join(r"F:\Narou",  ncode + '.txt'), 'a', encoding='utf-8') as f:
                f.write('\n'.join(lines))



if __name__=='__main__':
    get_page(ncode='n3170ed', gyokan=False)