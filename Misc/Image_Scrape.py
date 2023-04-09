import requests
import shutil
from urllib.parse import urljoin
from bs4 import BeautifulSoup

from rich.prompt import Confirm
from rich.table import Table, Column
from rich.console import Console
from rich.prompt import Prompt


headers = requests.utils.default_headers()
headers.update({
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
})

def fetchLinks(pageUrl, selector) -> list:
    html = requests.get(pageUrl, headers=headers).text
    bs = BeautifulSoup(html, 'html.parser')
    list = bs.select(selector)

    links = []
    for node in list:
        link =  urljoin(pageUrl, node.attrs[SCRAPE_MODE])
        # link = link.replace("thumb_", "")

        index = str(link).rindex('/')
        title = str(link)[index+1:]
        
        links.append([title, link])
    return links

def downloadLink(url, file_name) -> None:
    print("\nDownloading: ", file_name)
    res = requests.get(url, stream = True)
    if res.status_code == 200:
        with open(file_name,'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully downloaded: ',file_name)
    else:
        print('Image couldn\'t be retrieved')
    return

if __name__ == "__main__":
    SCRAPE_PAGE_URL = input("Enter url of page to be be scraped: \n")
    SCRAPE_SELECTOR = input("\nEnter css selector for urls to be scraped: \n")
    SCRAPE_MODE	= Prompt.ask("Enter selection mode: ", choices=["src",	"href"])

    table = Table(Column(header="Links Extracted", justify="center"), show_lines=True)

    links = fetchLinks(SCRAPE_PAGE_URL, SCRAPE_SELECTOR)

    for link in links:
        table.add_row(link[1])

    Console().print(table)

    validate = Confirm.ask("\nDo you wish to proceed?")
    if(validate):
        for link in links:
            print(link)
            downloadLink(link[1], (link[0]))
