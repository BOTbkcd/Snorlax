import pdfkit   # pdfkit is just a python wrapper Wkhtmltopdf, so latter has to be installed on the system 
import requests
from urllib.parse import urljoin
from bs4 import BeautifulSoup
import sys

from rich.prompt import Confirm
from rich.table import Table, Column
from rich import box
from rich.console import Console


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

def fetchLinks() -> list:
    html = requests.get(SCRAPE_PAGE_URL, headers=headers).text
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
    print("Downloading: ", outputFile)
    pdfkit.from_url(link, outputFile, options=opts)


SCRAPE_PAGE_URL = input("Enter url of page to be be scraped: \n")
SCRAPE_SELECTOR = input("\nEnter css selector for urls to be scraped: \n")

if(len(SCRAPE_SELECTOR) > 0):
    table = Table(Column(header="Links Extracted", justify="center"), show_lines=True)

    links = fetchLinks()
    for link in links:
        table.add_row(link[1])

    Console().print(table)
else:
    html = requests.get(SCRAPE_PAGE_URL, headers=headers).text
    bs = BeautifulSoup(html, 'html.parser')
    title = bs.title.string + ".pdf"

    downloadLink(SCRAPE_PAGE_URL, title)
    sys.exit()

validate = Confirm.ask("\nDo you wish to proceed?")
if(validate):
    isIndex = Confirm.ask("\nDo you want the output files to be indexed?")
    if(isIndex):
        for index, link in enumerate(links):
            link[0] = f"{index:02d} - " + link[0]

    for link in links:
        downloadLink(link[1], (link[0] + ".pdf"))


