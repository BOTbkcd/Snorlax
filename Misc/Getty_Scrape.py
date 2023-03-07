import requests
import shutil
from urllib.parse import urljoin
from bs4 import BeautifulSoup

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

imgLinks = []
for pageUrl in imgPages:
    imgLinks.append(fetchImgLink(pageUrl))

print(imgLinks)
for link in imgLinks:
    title = link[33:43] + ".jpg"
    downloadLink(link, title)