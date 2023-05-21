import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor as Executor

from Image_Scrape import downloadLink


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

def fetchPages():
    html = requests.get(SCRAPE_PAGE_URL, headers=headers).text
    bs = BeautifulSoup(html, 'html.parser')
    list = bs.select(IMG_PAGE_SELECTOR)

    links = []
    for node in list:
        link =  urljoin(SCRAPE_PAGE_URL, node.attrs['href'])
        links.append(link)
    return links

def fetchImgLink(pageUrl):
    html = requests.get(pageUrl, headers=headers).text
    bs = BeautifulSoup(html, 'html.parser')
    link = bs.select('picture[data-testid="hero-picture"] source')[-1].attrs['srcset']
    return link

IMG_PAGE_SELECTOR = 'div[data-testid="gallery-items-container"] > div a'
IMG_SELECTOR = 'picture[data-testid="hero-picture"] source:last-child'
SCRAPE_PAGE_URL = input("Enter getty search page url: \n")

imgPages = fetchPages()

with Executor(max_workers=5) as exec:
    imgLinks = []

    for pageUrl in imgPages:
        exec.submit(imgLinks.append(fetchImgLink(pageUrl)))

for link in imgLinks:
    id_start = 33
    id_end = link.index('/', 34)
    title = link[id_start:id_end] + ".jpg"
    downloadLink(link, title)
