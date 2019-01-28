from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
from threading import Thread, current_thread
import threading
import json
import os


stop_flag = True
spider_generated_flag = False
crawled_pages = 0


def url_key(urlString):
    if urlString[-1] == '/':
        urlString = urlString[:-1]
    parsed_url = urlparse(urlString)
    if parsed_url is not None and parsed_url.scheme == "https":
        urlString = urlString.replace("https", "http")
    return urlString


def checkpoint_spider(data):
    directory = 'Snapshots'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('Snapshots/Spider_Snapshot@' + str(len(data)) +'.json', 'w') as outfile:
        json.dump(data, outfile)


def checkpoint_url_queue(spider, data):
    directory = 'Snapshots'
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open('Snapshots/Queue_Snapshot@' + str(len(spider)) +'.json', 'w') as outfile:
        json.dump(data, outfile)


def serialize_spider_final(data):
    directory = 'Crawler'
    if not os.path.exists(directory):
        os.makedirs('Crawler')
    with open('Crawler/Spider.json', 'w') as outfile:
        json.dump(data, outfile)


def serialize_queue_final():
    pass


def apply_url_filter():
    pass


def text_urls_from_html(conn):
    soup = BeautifulSoup(conn, "html.parser")
    p_tags_content = soup.findAll('p')
    p_tags_content = [tag.text for tag in p_tags_content]
    span_tags_content = soup.findAll('span')
    span_tags_content = [tag.text for tag in span_tags_content]
    h_tags_content = soup.findAll('h')
    h_tags_content = [tag.text for tag in h_tags_content]
    a_tags_content = soup.findAll('a')
    content = ' '.join(p_tags_content) + ' ' + ' '.join(span_tags_content) + ' ' + ' '.join(h_tags_content)
    return content, a_tags_content


def update_spider_for_url(spider, current_url, content, a_tags_content, base_domain, queue):
    out_links = []
    for a_tag in a_tags_content:
        if 'href' in a_tag.attrs:
            url_extracted = a_tag['href']
            parsed_url = urlparse(url_extracted)
            if parsed_url.hostname is not None and base_domain in parsed_url.hostname and url_key(url_extracted) != current_url:
                out_links.append(url_extracted)
                if url_extracted not in spider:
                    queue.append(url_extracted)

    spider[url_key(current_url)] = {'text': content,
                                    'out_links': out_links}


def is_file_valid_for_spider(conn):

    for header in conn.headers._headers:
        if 'content-type' in header[0].lower():
            content_type = header[1]
            break
    if 'html' in content_type:
        return True
    return False


def crawler(spider, queue):
    global spider_generated_flag
    global crawled_pages

    base_domain =  "uic.edu"

    while len(spider) <= 20:

        if stop_flag:
            if spider_generated_flag is False:
                serialize_spider_final(spider)
                spider_generated_flag = True
            break
        try:
            current_url = queue.pop(0)
            current_url = url_key(current_url)
            if current_url not in spider:
                try:
                    with urlopen(current_url) as conn:
                        if is_file_valid_for_spider(conn):
                            content, a_tags_content = text_urls_from_html(conn)
                            if content.strip() != '':
                                update_spider_for_url(spider, current_url, content, a_tags_content, base_domain, queue)
                                print("crawling page {0}".format(len(spider)))
                                crawled_pages = len(spider)
                                if len(spider)%50 == 0:
                                    checkpoint_spider(spider)
                                    checkpoint_url_queue(spider, queue)
                                #print(current_thread())
                except Exception:
                    pass
        except Exception:
            pass


def main():
    spider = {}
    queue = []
    base_url = "https://www.cs.uic.edu"
    queue.append(base_url)
    threads = []
    #crawler(spider,queue)
    for ii in range(10):
        process = Thread(target=crawler, args=[spider, queue])
        process.start()
        threads.append(process)

    for process in threads:
        process.join()
        process.st

    serialize_spider_final(spider)


#main()


class StoppableThread(threading.Thread):
    """Thread class with a stop() method. The thread itself has to check
    regularly for the stopped() condition."""

    def __init__(self):
        super(StoppableThread, self).__init__()
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()
