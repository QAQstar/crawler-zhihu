# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog

import pymongo

from .Ui_config import Ui_Dialog

collection = pymongo.MongoClient(host='localhost', port=27017).zhihu.setting

class Dialog(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(Dialog, self).__init__(parent)
        self.setupUi(self)
        self._load_setting(user_index=1)

    def _load_setting(self, user_index=1):
        setting = collection.find_one({'_id': user_index})
        self.spinBox.setValue(setting['hot_list_thread'])
        self.spinBox_2.setValue(setting['answer_thread'])
        self.lcdNumber.display(setting['answer_num'])
        self.horizontalSlider.setValue(setting['answer_num'])
        self.spinBox_3.setValue(setting['search_thread'])
        self.doubleSpinBox.setValue(1/setting['x_axis_scale'])
        self.textEdit.setText(' '.join(setting['sensitive_words']))

    def _save_setting(self):
        pre_setting = collection.find_one({'_id': 1})
        pre_setting['hot_list_thread'] = self.spinBox.value()
        pre_setting['answer_thread'] = self.spinBox_2.value()
        pre_setting['answer_num'] = int(self.lcdNumber.value())
        pre_setting['search_thread'] = self.spinBox_3.value()
        pre_setting['x_axis_scale'] = 1/self.doubleSpinBox.value()
        sensitive_words = self.textEdit.toPlainText().strip().split(' ')
        if sensitive_words[0] == '':
            pre_setting['sensitive_words'] = []
        else:
            pre_setting['sensitive_words'] = sensitive_words
        collection.update_one({'_id': 1}, {'$set': pre_setting})

    # def _display_setting(self):
    #     self.spinBox.setValue(self.hot_list_thread)
    #     self.spinBox_2.setValue(self.answer_thread)
    #     self.lcdNumber.display(self.answer_num)
    #     self.horizontalSlider.setValue(self.answer_num)
    #     self.doubleSpinBox.setValue(1 / self.x_axis_scale)
    #     self.textEdit.setText(' '.join(self.sensitive_words))

    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        self._load_setting(user_index=0)
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self._save_setting()
        self.close()
    
    @pyqtSlot(int)
    def on_horizontalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        self.lcdNumber.display((value//10)*10)
