# -*- coding: utf-8 -*-

"""
Module implementing MainWindow.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore

from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from match_algorithm import BM, AC
from pyqtgraph import PlotWidget, AxisItem, InfiniteLine
from time import localtime
import zhihu_hot
import pymongo
import webbrowser
import lstm.lstm as LSTM
import jieba
import math



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

        text = self.lineEdit.text().strip()
        search_thread = db.setting.find_one({'_id': 1})['search_thread']
        this_question = db['question_' + str(self.index)]

        if len(text) > 1 and (text[0] == ':' or text[0] == '：'): # 相关度搜索
            words = jieba.lcut_for_search(text[1:]) # 搜索引擎模式

            executor = ThreadPoolExecutor(max_workers=len(words)) # 分有多少词就用多少线程
            answer_count = this_question.find().count()
            fs = [executor.submit(self._get_BM25_part1, word, answer_count) for word in words]
            part1 = {}
            words_bm_list = []
            for future in as_completed(fs):
                result = future.result()
                part1[result[0]] = result[1]
                words_bm_list.append(result[2])

            answer_length_avg = 0
            answer_index_list = []
            for answer in this_question.find():
                answer_length_avg += len(answer['content'])
                answer_index_list.append(answer['_id'])
            answer_length_avg = answer_length_avg / answer_count
            print('开始进行模糊搜索，分词：')
            print(words)
            executor = ThreadPoolExecutor(max_workers=search_thread)
            fs = [executor.submit(self._get_BM25, words, words_bm_list, part1, answer_index, answer_length_avg) for
                  answer_index in answer_index_list]
            result = [future.result() for future in as_completed(fs)]
            result.sort(key=lambda answer_and_BM25: answer_and_BM25[1], reverse=True)

            tab_index, show_count = 0, db.setting.find_one({'_id': 1})['fuzzy_search_tab']
            while tab_index < min(show_count, len(result)):
                answer_index = result[tab_index][0]
                answer = this_question.find_one({'_id':answer_index})
                self._add_fuzzy_search_tab(tab_index+1, answer)
                tab_index += 1

        elif len(text) > 1: # 关键词精确查找
            words = text.split(' ')

            if len(words) == 1 and words[0] != '':
                algorithm = BM(words[0])
                print('开始查找，采用BM算法，线程数：'+str(search_thread))
            elif len(words) > 1:
                algorithm = AC(words)
                print('开始查找，采用AC算法，线程数：'+str(search_thread))
            else:
                return

            executor = ThreadPoolExecutor(max_workers=search_thread)
            fs = []
            for answer in this_question.find():
                fs.append(executor.submit(self._add_accurate_search_tab, algorithm, answer))
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
        else:
            return

    def _add_accurate_search_tab(self, algorithm, answer):
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

    def _add_fuzzy_search_tab(self, tab_index, answer):
        text = '作者：' + answer['author']
        if answer['author'] != '匿名用户':
            if answer['gender'] == 1:
                text += '\n性别：男'
            elif answer['gender'] == -1:
                text += '\n性别：女'
        text += '\n点赞数：' + str(answer['voteup_count']) + '\n评论数：' + str(answer['comment_count']) + '\n\n' + answer[
            'content']

        tab = QtWidgets.QWidget()
        textEdit = QtWidgets.QTextEdit(tab)
        textEdit.setGeometry(QtCore.QRect(0, 0, 781, 241))
        textEdit.setText(text)
        self.tabWidget_2.addTab(tab, str(tab_index))

    def _get_BM25_part1(self, word, answer_count):
        bm = BM(word)
        dft = 0
        for answer in db['question_' + str(self.index)].find():
            if bm.find(answer['content']) != -1:
                dft += 1
        part1 = math.log((answer_count+0.5)/(dft+0.5))
        return word, part1, bm

    def _get_BM25(self, words, words_bm_list, part1, answer_index, answer_length_avg):
        result = 0
        for i in range(len(words)):
            answer = db['question_' + str(self.index)].find_one({'_id': answer_index})
            if answer is None:
                return
            answer_content = answer['content']
            word = words[i]
            tf_td = len(words_bm_list[i].find_all(answer_content))
            word_part1 = part1[word]
            word_part2 = ((1.5+1)*tf_td)/(1.5*((1-0.75)+0.75*(len(answer_content)/answer_length_avg))+tf_td)
            word_part3 = ((1.5+1)*tf_td)/(1.5+tf_td)
            result += word_part1*word_part2*word_part3

        return answer_index, result

    @pyqtSlot()
    def on_pushButton_3_clicked(self):
        """
        Slot documentation goes here.
        """
        # answers = []
        # for answer in db['question_'+str(self.index)].find():
        #     text = answer['content'].replace('\n', '')
        #     if 5 < len(text) < 100:
        #         answers.append(text)
        answers = [answer['content'].replace('\n', '') for answer in db['question_'+str(self.index)].find()]
        Line1 = InfiniteLine(pos=0, pen=(255,0,0), angle=0, movable=False)
        Line2 = InfiniteLine(pos=0.5, pen=(0,0,255), angle=0, movable=False)
        Line3 = InfiniteLine(pos=1, pen=(0,255,0), angle=0, movable=False)
        import sys
        data = LSTM.get_result(answers, vec_path=sys.path[0] + '/lstm/vec_lstm.pkl', model_path=sys.path[0] + '/lstm/lstmModel.pkl')
        tricks = [(0, '消极'), (0.5, '中立'), (1, '积极')]
        strAxis = AxisItem(orientation='left', maxTickLength=3)
        strAxis.setTicks([tricks, ])
        visitor_count_plot = PlotWidget(axisItems={'left': strAxis}, background=None)
        visitor_count_plot.plot(y=data, pen=None, symbol='o')
        visitor_count_plot.showAxis('bottom', False)
        visitor_count_plot.addItem(Line1)
        visitor_count_plot.addItem(Line2)
        visitor_count_plot.addItem(Line3)
        visitor_count_plot.setObjectName("tab")

        # visitor_count_plot.enableAutoRange('x', x_axis_scale)
        self._add_analysis_tab(visitor_count_plot, '情感分析')
        self.pushButton_3.setEnabled(False)