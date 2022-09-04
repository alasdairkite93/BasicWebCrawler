
import requests
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

from bs4 import BeautifulSoup

from urllib.parse import urlparse, urlsplit, urljoin

internal_link=[]

def urlExtractor(input_url):
    temp_urls = set()
    soup = BeautifulSoup(requests.get(input_url).content, "html.parser")
    current_url = urlparse(input_url).netloc
    for anchor in soup.findAll("a"):
        href = anchor.attrs.get("href")
        if(href != "" or href != None):
            href = urljoin(input_url, href)
            href_parsed = urlparse(href)
            href = href_parsed.scheme
            href += "://"
            href += href_parsed.netloc
            href += href_parsed.path
            final_parsed_href = urlparse(href)
            is_valid = bool(final_parsed_href.scheme) and bool(
                final_parsed_href.netloc)
            if is_valid:
                if current_url in href and href not in internal_link:
                    print(href)
                    internal_link.append(href)
                    temp_urls.add(href)
    return temp_urls

def localRepository(internal_links):
    with open('output.txt', 'w') as f:
        for link in internal_links:
            f.write(link)
            f.write("\n")

def queue(lines):
    for url in lines:
        queue = []
        queue.append(url)
        for j in range(3):
            for count in range(len(queue)):
                url = queue.pop(0)
                urls = urlExtractor(url)
                for i in urls:
                    queue.append(i)

if __name__ == '__main__':
    file1 = open("seeds.txt", "r")
    lines = file1.readlines()

    queue(lines)
    localRepository(internal_link)
