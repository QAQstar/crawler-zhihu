# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QMessageBox
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QListWidgetItem

import zhihu_hot
import pymongo

from time import localtime
from ui.Ui_MainWindow import Ui_MainWindow
from ui.question import MainWindow as question_window
from ui.config import Dialog as Dialog_config
from ui.Ui_about import Ui_Dialog as Dialog_about

db = pymongo.MongoClient(host='localhost', port=27017).zhihu

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        time_tuple = localtime(db.hot_list.find_one(sort=[('_id',pymongo.DESCENDING)])['_id'])
        self.label.setText('上次爬取热榜时间：%d-%d-%d %d:%d:%d'%(time_tuple.tm_year, time_tuple.tm_mon,
                            time_tuple.tm_mday, time_tuple.tm_hour, time_tuple.tm_min, time_tuple.tm_sec))
    def load_data(self):
        self.listWidget.clear()

        hot_index = db.hot_list.find_one(sort=[('_id', -1)])['index']

        for hot in hot_index:
            question = db.question.find_one({'_id': hot})
            item = QListWidgetItem()
            str = '\n' + question['title'] + '\n'
            item.setData(1, hot)  # 编号为1的数据存放该问题的索引
            item.setText(str)
            self.listWidget.addItem(item)

    @pyqtSlot(QListWidgetItem)
    def on_listWidget_itemDoubleClicked(self, item):
        """
        Slot documentation goes here.

        @param item DESCRIPTION
        @type QListWidgetItem
        """
        index = item.data(1)
        question_ui = question_window(index=index, parent=self)
        question_ui.show()
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self.load_data()

    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        zhihu_hot.Hot_List(save_answer=False)
        time_tuple = localtime(db.hot_list.find_one(sort=[('_id', pymongo.DESCENDING)])['_id'])
        self.label.setText('上次爬取热榜时间：%d-%d-%d %d:%d:%d' % (time_tuple.tm_year, time_tuple.tm_mon,
                            time_tuple.tm_mday, time_tuple.tm_hour, time_tuple.tm_min, time_tuple.tm_sec))
        self.load_data()

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        zhihu_hot.clear_cache()
        self.load_data()
        time_tuple = localtime(db.hot_list.find_one(sort=[('_id', pymongo.DESCENDING)])['_id'])
        self.label.setText('上次爬取热榜时间：%d-%d-%d %d:%d:%d'%(time_tuple.tm_year, time_tuple.tm_mon,
                            time_tuple.tm_mday, time_tuple.tm_hour, time_tuple.tm_min, time_tuple.tm_sec))
        QMessageBox.information(self, '提示', '清理完成')

    @pyqtSlot()
    def on_action_triggered(self):
        """
        Slot documentation goes here.
        """
        config_ui = Dialog_config(parent=self)
        config_ui.show()

    @pyqtSlot()
    def on_action_2_triggered(self):
        """
        Slot documentation goes here.
        """
        about_ui = Dialog_about()
        about_dialog = QtWidgets.QDialog(parent=self)
        about_ui.setupUi(about_dialog)
        about_dialog.show()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
