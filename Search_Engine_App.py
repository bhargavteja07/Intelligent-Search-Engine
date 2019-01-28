

from PyQt5 import QtCore, QtGui, QtWidgets
import page_rank_graph as pr
import vector_model as vm
import utilities as ut

class Ui_Dialog(object):

    search_result = []
    current_page = 1

    def retrieve_docs_for_query_v2(self, ref_query_tokens):
        spider = vm.get_spider()
        doc_weights = {}
        for doc in spider:
            doc_weights[doc] = vm.compute_cosine_sim(ref_query_tokens, doc)
        return doc_weights

    def execute_query_intelligent_v2(self, query):
        query_tokens = query.split()
        refined_query_tokens = ut.tokenize_data_for_valid_nodes(query_tokens)
        docs_for_query = self.retrieve_docs_for_query_v2(refined_query_tokens)
        sorted_similarity = sorted(docs_for_query, key=docs_for_query.get, reverse=True)
        docs_based_on_page_rank = pr.sort_docs_based_on_page_rank_v2(sorted_similarity[:100], docs_for_query)
        print("docs based on tfidf - {0}".format(sorted_similarity[:20]))
        return docs_based_on_page_rank[:100]

    def execute_query_v2(self, query):
        query_tokens = query.split()
        refined_query_tokens = ut.tokenize_data_for_valid_nodes(query_tokens)
        docs_for_query = self.retrieve_docs_for_query_v2(refined_query_tokens)
        sorted_similarity = sorted(docs_for_query, key=docs_for_query.get, reverse=True)
        return sorted_similarity[:100]

    def execute_search(self):
        query = self.plainTextEdit.toPlainText()
        self.search_result = self.execute_query_v2(query)
        self.listWidget.clear()
        result = self.search_result[:10]
        for res in result:
            self.listWidget.addItem(res)

    def execute_intelligent_search(self):
        query = self.plainTextEdit.toPlainText()
        self.search_result = self.execute_query_intelligent_v2(query)
        self.listWidget.clear()
        result = self.search_result[:10]
        for res in result:
            self.listWidget.addItem(res)

    def page_next(self):
        ll = self.search_result
        if len(self.search_result) >= (self.current_page * 10) and self.current_page < 10:
            self.current_page += 1
            self.listWidget.clear()
            result = self.search_result[(self.current_page*10)-10:self.current_page*10]
            for res in result:
                self.listWidget.addItem(res)

    def page_back(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.listWidget.clear()
            result = self.search_result[(self.current_page * 10) - 10:self.current_page * 10]
            for res in result:
                self.listWidget.addItem(res)

    def setupUi(self, Dialog):
        Dialog.setObjectName("UIC SEARCH ENGINE")
        Dialog.resize(632, 398)
        Dialog.setStyleSheet("")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(225, 20, 101, 61))
        self.label.setStyleSheet("image: url(uic.PNG);")
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Dialog)
        self.pushButton.setGeometry(QtCore.QRect(330, 130, 161, 32))
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(150, 130, 171, 32))
        self.pushButton_2.setObjectName("pushButton_2")
        self.listWidget = QtWidgets.QListWidget(Dialog)
        self.listWidget.setGeometry(QtCore.QRect(70, 180, 491, 192))
        self.listWidget.setStyleSheet("color: rgb(26, 26, 26);")
        self.listWidget.setObjectName("listWidget")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(Dialog)
        self.plainTextEdit.setGeometry(QtCore.QRect(70, 100, 491, 21))
        self.plainTextEdit.setStyleSheet("color: rgb(0, 0, 0);")
        self.plainTextEdit.setPlainText("")
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(570, 260, 51, 32))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_4 = QtWidgets.QPushButton(Dialog)
        self.pushButton_4.setGeometry(QtCore.QRect(10, 260, 51, 32))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(310, 45, 81, 16))
        self.label_2.setStyleSheet("color: rgb(47, 35, 205);\n"
"font: 18pt \"Arial\";")
        self.label_2.setObjectName("label_2")
        self.pushButton.clicked.connect(self.execute_intelligent_search)
        self.pushButton_2.clicked.connect(self.execute_search)
        self.pushButton_3.clicked.connect(self.page_next)
        self.pushButton_4.clicked.connect(self.page_back)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.SF NS Text\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>"))
        self.pushButton.setText(_translate("Dialog", "Intelligent Search "))
        self.pushButton_2.setText(_translate("Dialog", "Search "))
        self.pushButton_3.setText(_translate("Dialog", ">"))
        self.pushButton_4.setText(_translate("Dialog", "<"))
        self.label_2.setText(_translate("Dialog", "SEARCH"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    Dialog.setFixedSize(630,410)
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()

    sys.exit(app.exec_())

