# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore

from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from match_algorithm import BM, AC
from pyqtgraph import PlotWidget, AxisItem
from time import localtime
import zhihu_hot
import pymongo
import webbrowser


from ui.Ui_question import Ui_MainWindow

db = pymongo.MongoClient(host='localhost', port=27017).zhihu

class MainWindow(QMainWindow, Ui_MainWindow):
    """
    Class documentation goes here.
    """
    def __init__(self, index, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.index = index
        self.setWindowTitle('Question '+str(index))
        x_axis_scale = db.setting.find_one({'_id':1})['x_axis_scale']
        self._load_analysis(x_axis_scale)
        zhihu_hot.get_answers(index)
        self._load_high_quality_answer()

    def closeEvent(self, event):
        db.drop_collection('question_'+str(self.index)) # 关闭时清空原有的答案

    def _load_analysis(self, x_axis_scale):
        this_question = db.question.find_one({'_id':self.index})
        title = this_question['title']
        content = this_question['content']
        time_tuple = localtime(this_question['created_time'])
        question_created_time = "%d-%d-%d %d:%d:%d" % (
        time_tuple.tm_year, time_tuple.tm_mon, time_tuple.tm_mday, time_tuple.tm_hour, time_tuple.tm_min,
        time_tuple.tm_sec)
        if content != '':
            self.textEdit.setText(title+'\n\n   提问时间：'+question_created_time+'\n   问题描述：\n'+content)
        else:
            self.textEdit.setText(title+'\n\n   提问时间：'+question_created_time)

        trend = db.question_trend.find_one({'_id':self.index})

        time_trend = trend['time']
        str_time = []
        for num_time in time_trend:
            local_time = localtime(num_time)
            str_time.append("%d-%d\n%d:%d\n"%(local_time.tm_mon,local_time.tm_mday,local_time.tm_hour,local_time.tm_min))
        ticks = [(i, j) for i, j in zip(time_trend, str_time)]

        rank_trend = trend['rank']
        convert_rank = [51 - i for i in rank_trend]
        rank_ticks = [(i, j) for i, j in zip(convert_rank, rank_trend)]
        rankAxis = AxisItem(orientation='left')
        rankAxis.setTicks([rank_ticks, ])
        strAxis = AxisItem(orientation='bottom', maxTickLength=5)
        strAxis.setTicks([ticks, ])
        rank_plot = PlotWidget(axisItems={'bottom':strAxis, 'left':rankAxis}, background=None)
        rank_plot.setObjectName("tab")
        rank_plot.plot(x=time_trend, y=convert_rank, pen=(0, 255, 0), symbol='o')
        rank_plot.enableAutoRange('x', x_axis_scale)
        self._add_analysis_tab(rank_plot, '排名')

        heat_trend = trend['heat']
        # strAxis.setStyle(autoExpandTextSpace=True)
        strAxis = AxisItem(orientation='bottom', maxTickLength=5)
        strAxis.setTicks([ticks, ])
        heat_plot = PlotWidget(axisItems={'bottom':strAxis}, background=None)
        heat_plot.setObjectName("tab")
        heat_plot.plot(x=time_trend, y=heat_trend, pen=(255,0,0), symbol='o')
        heat_plot.enableAutoRange('x', x_axis_scale)
        self._add_analysis_tab(heat_plot, '热度')

        answer_count_trend = trend['answer_count']
        strAxis = AxisItem(orientation='bottom', maxTickLength=5)
        strAxis.setTicks([ticks, ])
        answer_count_plot = PlotWidget(axisItems={'bottom': strAxis}, background=None)
        answer_count_plot.setObjectName("tab")
        answer_count_plot.plot(x=time_trend, y=answer_count_trend, pen=(0, 0, 255), symbol='o')
        answer_count_plot.enableAutoRange('x', x_axis_scale)
        self._add_analysis_tab(answer_count_plot, '回答量')

        follower_count_trend = trend['follower_count']
        strAxis = AxisItem(orientation='bottom', maxTickLength=5)
        strAxis.setTicks([ticks, ])
        follower_count_plot = PlotWidget(axisItems={'bottom': strAxis}, background=None)
        follower_count_plot.setObjectName("tab")
        follower_count_plot.plot(x=time_trend, y=follower_count_trend, pen=(19, 234, 201), symbolBrush=(19, 234, 201),
                        symbol='o', symbolPen='w')
        follower_count_plot.enableAutoRange('x', x_axis_scale)
        self._add_analysis_tab(follower_count_plot, '关注数')

        visitor_count_trend = trend['visitor_count']
        strAxis = AxisItem(orientation='bottom', maxTickLength=5)
        strAxis.setTicks([ticks, ])
        visitor_count_plot = PlotWidget(axisItems={'bottom': strAxis}, background=None)
        visitor_count_plot.setObjectName("tab")
        visitor_count_plot.plot(x=time_trend, y=visitor_count_trend, pen=(195, 46, 212), symbolBrush=(195, 46, 212),
                        symbol='t', symbolPen='w')
        visitor_count_plot.enableAutoRange('x', x_axis_scale)
        self._add_analysis_tab(visitor_count_plot, '浏览量')

    def _add_analysis_tab(self, plot_widget, title='page'):
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(plot_widget.sizePolicy().hasHeightForWidth())
        plot_widget.setSizePolicy(sizePolicy)
        self.tabWidget.addTab(plot_widget, title)

    def _load_high_quality_answer(self):
        answer_collection = db['question_' + str(self.index)]
        answer = None
        for answer in answer_collection.find(sort=[('_id',pymongo.ASCENDING)]):
            # answer = answer_collection.find_one({'_id':i})
            if answer['content'] is not None:
                break
        text = '作者：'+answer['author']
        if answer['author'] != '匿名用户':
            if answer['gender'] == 1:
                text += '\n性别：男'
            elif answer['gender'] == -1:
                text += '\n性别：女'
        text += '\n点赞数：'+str(answer['voteup_count'])+'\n评论数：'+str(answer['comment_count'])+'\n\n'+answer['content']
        self.textEdit_2.setText(text)
    
    @pyqtSlot()
    def on_pushButton_clicked(self):
        """
        Slot documentation goes here.
        """
        webbrowser.open('https://www.zhihu.com/question/'+str(self.index))
    
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        """
        Slot documentation goes here.
        """
        self.tabWidget_2.clear()
        self.tabWidget_2.addTab(self.tab_3, '高赞回答')

        search_thread = db.setting.find_one({'_id':1})['search_thread']
        words = self.lineEdit.text().strip().split(' ')
        if len(words) == 1 and words[0] != '':
            algorithm = BM(words[0])
            print('开始查找，采用BM算法，线程数：'+str(search_thread))
        elif len(words) > 1:
            algorithm = AC(words)
            print('开始查找，采用AC算法，线程数：'+str(search_thread))
        else:
            return

        executor = ThreadPoolExecutor(max_workers=10)
        fs = []
        for answer in db['question_' + str(self.index)].find():
            fs.append(executor.submit(self._add_search_tab, algorithm, answer))
        tab_index = 1
        for future in as_completed(fs):
            text = future.result()
            if text is not None:
                tab = QtWidgets.QWidget()
                textEdit = QtWidgets.QTextEdit(tab)
                textEdit.setGeometry(QtCore.QRect(0, 0, 781, 241))
                textEdit.setText(text)
                self.tabWidget_2.addTab(tab, str(tab_index))
                tab_index += 1

    def _add_search_tab(self, algorithm, answer):
        is_find = algorithm.find(answer['content'])
        if is_find != -1:
            text = '作者：' + answer['author']
            if answer['author'] != '匿名用户':
                if answer['gender'] == 1:
                    text += '\n性别：男'
                elif answer['gender'] == -1:
                    text += '\n性别：女'
            text += '\n点赞数：' + str(answer['voteup_count']) + '\n评论数：' + str(answer['comment_count']) + '\n\n' + answer[
                'content']
            return text
        return None