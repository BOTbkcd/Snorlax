from urllib.request import urlopen
from urllib.parse import urljoin
from bs4 import BeautifulSoup
from rich.prompt import Confirm
import pdfkit   # pdfkit is just a python wrapper Wkhtmltopdf, so latter has to be installed on the system 

def fetchLinks() -> list:
    html = urlopen(SCRAPE_PAGE_URL)
    bs = BeautifulSoup(html, 'html.parser')
    list = bs.select(SCRAPE_SELECTOR)

    links = []
    for node in list:
        link =  urljoin(SCRAPE_PAGE_URL, node.attrs['href'])
        title = node.getText().strip()
        links.append([title, link])
    return links

def downloadLink(link, outputFile):
    opts = {
        'page-size': 'A4',
        'margin-top': '0.75in',
        'margin-right': '0.75in',
        'margin-bottom': '0.75in',
        'margin-left': '0.75in',
        'minimum-font-size': "16",
    }
    
    pdfkit.from_url(link, outputFile, options=opts)


SCRAPE_PAGE_URL = input("Enter url of page to be be scraped: \n")
SCRAPE_SELECTOR = input("\nEnter css selector for urls to be scraped: \n")

links = fetchLinks()

print("\nFollowing links have been fetched: \n")
for link in links:
    print(link[1])

validate = Confirm.ask("\nDo you wish to proceed?")
if(validate):
    isIndex = Confirm.ask("\nDo you want the output files to be indexed?")
    if(isIndex):
        for index, link in enumerate(links):
            link[0] = f"{index:02d} - " + link[0]

    for link in links:
        print(link)
        downloadLink(link[1], (link[0] + ".pdf"))


