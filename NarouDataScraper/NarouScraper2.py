import os.path

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
from time import sleep

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36'}
url_header = 'https://ncode.syosetu.com'
proxies = {
    'https':'https://140.227.239.66:3128'
}


def get_text(url):
    try:
        # response = requests.get(url, headers=headers, proxies=proxies, verify='certs.pem')
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')
        text = soup.find(id='novel_honbun')
        texts = [line.text for line in text.find_all('p')] #1文1文はp tagで囲まれている
        print(f'length of text {len(texts)}')
        texts = [line.replace('\u3000', '') for line in texts] #空白文字列の削除
        texts = [line for line in texts if line != ''] #行間をすべて飛ばす
        res_texts = list()
        temp_lines = list()

        def check_conversation(line):
            if line.lstrip('「').lstrip('『').lstrip('」').lstrip('』') == '':
                return False
            elif line.startswith('「') and line.endswith('」'):
                return True
            elif line.startswith('『') and line.endswith('』'):
                return True
            return False

        for text in texts:
            conversation = check_conversation(text)
            if not conversation and temp_lines != []:
                if len(temp_lines) > 1: #2行以上の会話を保存
                    res_texts.append('\n'.join(temp_lines) + '\n')
                temp_lines = list()
            elif conversation:
                text = text.lstrip('「').lstrip('『').lstrip('」').lstrip('』')
                temp_lines.append(text)
            elif not conversation:
                temp_lines = list()
            else:
                pass
    except:
        sleep(3.0)
        res_texts = get_text(url)
    return res_texts

def get_page(url, ncodes):
    print(f'url : {url}')
    ncode = os.path.basename(os.path.dirname(url))
    if ncode in ncodes:
        print(f'ncodes: {ncode} are already found...')
        return None
    url_header = 'https://ncode.syosetu.com'
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    indices = soup.find(class_='index_box')
    print('ncode : ' , ncode)
    hrefs = [a['href'] for a in indices.find_all('a')]
    hrefs = sorted(hrefs, key=lambda x: int(x.split('/')[-2]))
    print(f'length of hrefs {len(hrefs)}')
    for href in tqdm(hrefs):
        print(f'Start {href}')
        url = url_header + href
        sleep(1.0)
        lines = get_text(url)
        if lines != []:
            with open(os.path.join(r"C:\Users\Atsuya\PycharmProjects\NarouScraping\NarouData",  ncode + '.txt'), 'a', encoding='utf-8') as f:
                f.write('\n'.join(lines))
        else:
            print('No conversation found...')
