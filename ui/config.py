# -*- coding: utf-8 -*-

"""
Module implementing Dialog.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog, QMessageBox

from lstm.lstm import retrain
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
        self.lcdNumber_2.display(setting['lstm_round'])
        self.horizontalSlider_2.setValue(setting['lstm_round'])
        self.spinBox_3.setValue(setting['search_thread'])
        self.spinBox_4.setValue(setting['fuzzy_search_tab'])
        self.spinBox_4.setMaximum(setting['answer_num'])
        interval = setting['interval']
        self.textEdit.setText(' '.join(setting['sensitive_words']))
        if interval == 86400:
            self.radioButton.setChecked(True)
        elif interval == 604800:
            self.radioButton_2.setChecked(True)
        else:
            self.radioButton_3.setChecked(True)
        self.doubleSpinBox.setValue(1/setting['x_axis_scale'])

    def _save_setting(self):
        pre_setting = collection.find_one({'_id': 1})
        pre_lstm_round = pre_setting['lstm_round']
        cur_lstm_round = self.horizontalSlider_2.value()
        if pre_lstm_round != cur_lstm_round:
            reply = QMessageBox.question(self, '提示', '你修改了训练轮数，即将重新训练模型，这可能需要一点时间，是否继续？',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.Yes:
                import sys
                retrain(cur_lstm_round, sample_path=sys.path[0] + '/lstm/sampleTest.txt',
                        vec_path=sys.path[0] + '/lstm/vec_lstm.pkl', model_path=sys.path[0] + '/lstm/lstmModel.pkl')
            else:
                self.horizontalSlider_2.setValue(pre_lstm_round)
                return False
        pre_setting['hot_list_thread'] = self.spinBox.value()
        pre_setting['answer_thread'] = self.spinBox_2.value()
        pre_setting['answer_num'] = int(self.lcdNumber.value())
        pre_setting['lstm_round'] = cur_lstm_round
        pre_setting['search_thread'] = self.spinBox_3.value()
        pre_setting['fuzzy_search_tab'] = self.spinBox_4.value()
        sensitive_words = self.textEdit.toPlainText().strip().split(' ')
        if sensitive_words[0] == '':
            pre_setting['sensitive_words'] = []
        else:
            pre_setting['sensitive_words'] = sensitive_words
        if self.radioButton.isChecked():
            pre_setting['interval'] = 86400
        elif self.radioButton_2.isChecked():
            pre_setting['interval'] = 604800
        else:
            pre_setting['interval'] = 2592000
        pre_setting['x_axis_scale'] = 1/self.doubleSpinBox.value()
        collection.update_one({'_id': 1}, {'$set': pre_setting})

        return True

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
        if self._save_setting() is True:
            self.close()
    
    @pyqtSlot(int)
    def on_horizontalSlider_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        new_value = (value//10)*10
        self.lcdNumber.display(new_value)
        self.spinBox_4.setMaximum(new_value)

    @pyqtSlot(int)
    def on_horizontalSlider_2_valueChanged(self, value):
        """
        Slot documentation goes here.
        
        @param value DESCRIPTION
        @type int
        """
        self.lcdNumber_2.display(value)
