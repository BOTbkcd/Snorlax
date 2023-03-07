import requests
import shutil
from urllib.parse import urljoin
from bs4 import BeautifulSoup

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
        link =  urljoin(SCRAPE_PAGE_URL, node.attrs['src'])
        link = link.replace("thumb_", "")
        title = node.attrs['alt']
        links.append([title, link])
    return links

def downloadLink(url, file_name):
    print("\nDownloading: ", file_name)
    res = requests.get(url, stream = True)
    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully downloaded: ',file_name)
    else:
        print('Image couldn\'t be retrieved')
    return

if	__name__	==	"__main__":
    SCRAPE_PAGE_URL = input("Enter url of page to be be scraped: \n")
    SCRAPE_SELECTOR = input("\nEnter css selector for urls to be scraped: \n")

    table = Table(Column(header="Links Extracted", justify="center"), show_lines=True)

    links = fetchLinks()

    for link in links:
        table.add_row(link[1])

    Console().print(table)

    validate = Confirm.ask("\nDo you wish to proceed?")
    if(validate):
        for link in links:
            print(link)
            downloadLink(link[1], (link[0] + ".jpg"))
