from PyQt5 import QtCore, QtGui, QtWidgets
import threading
from bs4 import BeautifulSoup
from urllib.request import urlopen
from urllib.parse import urlparse
from threading import Thread, current_thread
import threading
import json
import os

class Ui_Dialog(object):

    stop_flag = False
    spider_generated_flag = False
    crawled_pages = 0

    def url_key(self, urlString):
        if urlString[-1] == '/':
            urlString = urlString[:-1]
        parsed_url = urlparse(urlString)
        if parsed_url is not None and parsed_url.scheme == "https":
            urlString = urlString.replace("https", "http")
        return urlString

    def checkpoint_spider(self, data):
        directory = 'Snapshots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open('Snapshots/Spider_Snapshot@' + str(len(data)) + '.json', 'w') as outfile:
            json.dump(data, outfile)

    def checkpoint_url_queue(self, spider, data):
        directory = 'Snapshots'
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open('Snapshots/Queue_Snapshot@' + str(len(spider)) + '.json', 'w') as outfile:
            json.dump(data, outfile)

    def serialize_spider_final(self, data):
        directory = 'Crawler'
        if not os.path.exists(directory):
            os.makedirs('Crawler')
        with open('Crawler/Spider.json', 'w') as outfile:
            json.dump(data, outfile)

    def serialize_queue_final(self):
        pass

    def apply_url_filter(self):
        pass

    def text_urls_from_html(self, conn):
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

    def update_spider_for_url(self, spider, current_url, content, a_tags_content, base_domain, queue):
        out_links = []
        for a_tag in a_tags_content:
            if 'href' in a_tag.attrs:
                url_extracted = a_tag['href']
                parsed_url = urlparse(url_extracted)
                if parsed_url.hostname is not None and base_domain in parsed_url.hostname and self.url_key(
                        url_extracted) != current_url:
                    out_links.append(url_extracted)
                    if url_extracted not in spider:
                        queue.append(url_extracted)

        spider[self.url_key(current_url)] = {'text': content,
                                        'out_links': out_links}

    def is_file_valid_for_spider(self, conn):

        for header in conn.headers._headers:
            if 'content-type' in header[0].lower():
                content_type = header[1]
                break
        if 'html' in content_type:
            return True
        return False

    def crawler(self, spider, queue):

        base_domain = "uic.edu"

        while len(spider) <= 3000:

            if self.stop_flag:
                if self.spider_generated_flag is False:
                    self.serialize_spider_final(spider)
                    print("saved spider")
                    self.label.setText("Crawler Successfully generated spider with {0} urls".format(len(spider)))
                    self.spider_generated_flag = True
                break
            try:
                current_url = queue.pop(0)
                current_url = self.url_key(current_url)
                if current_url not in spider:
                    try:
                        with urlopen(current_url) as conn:
                            if self.is_file_valid_for_spider(conn):
                                content, a_tags_content = self.text_urls_from_html(conn)
                                if content.strip() != '':
                                    if self.stop_flag:
                                        if self.spider_generated_flag is False:
                                            self.serialize_spider_final(spider)
                                            print("saved spider")
                                            self.label.setText(
                                                "Crawler Successfully generated spider with {0} urls".format(
                                                    len(spider)))
                                            self.spider_generated_flag = True
                                        break

                                    if len(spider) >= 3000:
                                        if self.spider_generated_flag is False:
                                            self.serialize_spider_final(spider)
                                            print("saved spider")
                                            self.label.setText(
                                                "Crawler Successfully generated spider with {0} urls".format(
                                                    len(spider)))
                                            self.spider_generated_flag = True
                                        break

                                    self.update_spider_for_url(spider, current_url, content, a_tags_content, base_domain,
                                                          queue)
                                    print("crawling page {0}".format(len(spider)))
                                    crawled_pages = len(spider)
                                    self.label.setText("Pages Crawled: {0}".format(len(spider)))
                                    if len(spider) % 1000 == 0:
                                        self.checkpoint_spider(spider)
                                        self.checkpoint_url_queue(spider, queue)

                                    # print(current_thread())
                    except Exception as ex:
                        pass
            except Exception as ex:
                pass

    def main(self):
        spider = {}
        queue = []
        base_url = "https://www.cs.uic.edu"
        queue.append(base_url)
        threads = []
        #self.crawler(spider,queue)
        for ii in range(10):
            process = Thread(target=self.crawler, args=[spider, queue])
            process.start()
            threads.append(process)

        for process in threads:
            process.join()
            process.st

        self.serialize_spider_final(spider)

    def execute_crawler(self):

        if self.stop_flag is True:
            self.stop_flag = False
            self.pushButton.setText("Stop Crawler")
        else:
            self.stop_flag = True
            self.spider_generated_flag = False
            self.pushButton.setText("Run Crawler")
            return
        #self.main()

        thread = threading.Thread(target=self.main, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

        #crawler.main()


    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(499, 360)
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(185, 140, 131, 41))
        self.pushButton.setObjectName("pushButton")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(60, 190, 391, 20))
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setIndent(-1)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(160, 40, 101, 61))
        self.label_2.setStyleSheet("image: url(uic.PNG);")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(245, 40, 101, 61))
        self.label_3.setStyleSheet("color: rgb(47, 35, 205);\n"
                                   "font: 18pt \"Arial\";")
        self.label_3.setObjectName("label_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        self.pushButton.clicked.connect(self.execute_crawler)


    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.pushButton.setText(_translate("Dialog", "Run Crawler"))
        self.label.setText(_translate("Dialog", "Pages Crawled: 0"))
        self.label_3.setText(_translate("Dialog", "CRAWLER"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

