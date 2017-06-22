import os
from bs4 import BeautifulSoup
import urllib.request


def search(dirname):
    f=open('gov_list.txt', 'w')
    filenames = os.listdir(dirname)
    for filename in filenames:
        full_filename = os.path.join(dirname, filename)
        print(full_filename)
        if full_filename.split('.')[1] == 'html':
            parse_html(full_filename, f)
    f.close()


def parse_html(url, f):
    page_url = 'file://'+url
    url_open = urllib.request.urlopen(page_url)
    soup = BeautifulSoup(url_open, 'html.parser', from_encoding='utf-8')
    content = soup.find('ul', attrs={'class':'gov-web'})
    page_list = content.findAll('li')

    for page in page_list:
        info = page.find('dt')
        link = info.find('a')

        f.write(link.text + ',' + link['href'] + '\n')
        print(link.text, link['href'])

search('/home/hknam/Documents/keyword/gov/')