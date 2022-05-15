from bs4 import BeautifulSoup
from collections import defaultdict
import requests
import preprocess
from urllib.parse import urlparse, urljoin, urlsplit, urlunsplit, urlunparse
import json

def get_dfl_check_allowed(root_url):
    rp = urlparse(root_url)
    def check_allowed(url : str) -> bool:
        up = urlparse(url)

        rstr = rp.hostname + '/' + rp.path
        ustr = up.hostname + '/' + up.path

        # print(f'rstr: {rstr}\nustr: {ustr}')

        return len(ustr) >= len(rstr) and (ustr[:len(rstr)] == rstr)

    return check_allowed

class WebCrawler():

    
    def __init__(self, root_url, check_allowed=None):
        self.graph = defaultdict((lambda : []))
        self.content_map = dict()
        self.root_url = root_url
        self.host_url = urlunsplit(tuple(list(urlsplit(root_url)[:2]) + [''] * 3))
        if check_allowed is None:
            self.check_allowed = get_dfl_check_allowed(self.root_url)
        else:
            self.check_allowed = check_allowed
        self.crawl(None, self.root_url)


    
    def crawl(self, parent, url):
        
        if url not in self.content_map:
            print(f'URL: {url}')
            res = requests.get(url)
            if not res.ok:
                return

            soup = BeautifulSoup(res.content, features='html5lib')
            text = preprocess.clean_characters(soup.get_text())
            self.content_map[url] = text
            if parent is not None:
                self.graph[parent].append(url)
            for link in soup.findAll('a'):
                if link.has_attr('href'):
                    true_url = urljoin(self.host_url, urlparse(link.get('href')).path)
                    if self.check_allowed(true_url):
                        self.crawl(url, true_url)


if __name__ == '__main__':
    root_url = 'https://designlab.eng.rpi.edu/edn/projects/capstone-support-dev/wiki'
    wc = WebCrawler(root_url)
    with open('storage/rules/wiki-content.json', 'w') as content_f, \
        open('storage/rules/wiki-graph.json', 'w') as graph_f:
        json.dump(wc.content_map, content_f)
        json.dump(wc.graph, graph_f)