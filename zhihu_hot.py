# -*- coding: utf-8 -*-
import requests
import re
import time
from bs4 import BeautifulSoup
from urllib.parse import urlencode
from concurrent.futures import ThreadPoolExecutor, wait, as_completed
from match_algorithm import BM, AC
import pymongo

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
             'Chrome/74.0.3729.131 Safari/537.36'
cookie = '...' # 此处填入登陆后的cookie

db = pymongo.MongoClient(host='localhost', port=27017).zhihu

class Answer:
    def __init__(self, question_index, answer_index, author, gender, voteup_count, comment_count, content):
        self.question_index = question_index
        self.answer_index = answer_index
        self.author = author
        self.gender = gender
        self.voteup_count = voteup_count
        self.comment_count = comment_count
        self.content = content

    def save(self):
        collection = db['question_'+str(self.question_index)]
        answer = {
            '_id': self.answer_index,
            'author': self.author,
            'gender': self.gender,
            'voteup_count': self.voteup_count,
            'comment_count': self.comment_count,
            'content': self.content,
        }
        collection.insert_one(answer)

class Question:
    def __init__(self, rank, index, heat, save_answer=False):
        # 请求头
        self.headers = {
            'User-Agent': user_agent,
            'Cookie': cookie,
            'X-Requested-With': 'fetch'
        }
        # 热榜中的排名
        self.rank = rank
        # 问题索引
        self.index = index
        # 热度
        self.heat = heat
        url = 'https://www.zhihu.com/api/v4/questions/'+str(index)+\
              '?include=created_time%2Cdetail%2Canswer_count%2Cfollower_count%2Cvisit_count'
        data = requests.get(url, headers=self.headers, timeout=10).json()
        # 问题
        self.title = data['title']
        # 问题描述
        text = ''
        if data['detail'] != '':
            soup = BeautifulSoup(data['detail'].replace('<br/>', '\n'), 'lxml')
            for node in soup.find(name='body'):
                if node.name == 'p' and node.text != '\n':
                    text += node.text + '\n'
                elif node.name == 'figure':
                    text += ' [图片]\n'
                elif node.name == 'blockquote':
                    text += '  ' + node.text
                elif node.name == 'ul':
                    for child in node.children:
                        if child.text == '': continue
                        text += '  ·' + child.text + '\n'
        self.detail = text
        # 问题创建时间
        self.created_time = int(data['created'])
        # 回答总数
        self.answer_count = int(data['answer_count'])
        # 浏览数
        self.visitor_count = int(data['visit_count'])
        # 关注数
        self.follower_count = int(data['follower_count'])
        if save_answer:
            get_answers(self.index)

    def save(self):
        question_collection = db.question
        trend_collection = db.question_trend
        now_time = time.time()

        if question_collection.find_one({'_id': self.index}) is not None: # 问题已存在
            question = {
                'title': self.title,
                'content': self.detail,
                'record_time': now_time
            }
            question_collection.update_one({'_id': self.index}, {'$set': question})
            trend = trend_collection.find_one({'_id': self.index})
            trend['time'].append(time.time())
            trend['rank'].append(self.rank)
            trend['heat'].append(self.heat)
            trend['answer_count'].append(self.answer_count)
            trend['visitor_count'].append(self.visitor_count)
            trend['follower_count'].append(self.follower_count)
            trend['record_time'] = now_time
            trend_collection.update_one({'_id': self.index}, {'$set': trend})
        else: # 问题新登上热榜
            question = {
                '_id': self.index,
                'title': self.title,
                'content': self.detail,
                'created_time': self.created_time,
                'record_time': now_time
            }
            trend = {
                '_id': self.index,
                'time': [now_time,],
                'rank': [self.rank,],
                'heat': [self.heat,],
                'answer_count': [self.answer_count,],
                'visitor_count': [self.visitor_count,],
                'follower_count': [self.follower_count,],
                'record_time': now_time
            }
            question_collection.insert_one(question)
            trend_collection.insert_one(trend)

    def __str__(self):
        if self.detail != '':
            return self.title + '\n' \
                   + '    问题概述: ' + self.detail + '\n' \
                   + '    热度: ' + str(self.heat) + '万'
        else:
            return self.title + '\n' \
                   + '    热度: ' + str(self.heat) + '万'


class Hot_List:
    def __init__(self, save_answer=False):
        self._save_answer = save_answer
        self.headers = {
            'User-Agent': user_agent,
            'Cookie': cookie
        }
        self.question_list = self._get_hot_question_list()
        # self.save()

    def save(self):
        collection = db.hot_list
        hot_list= {
            '_id': time.time(),
            'index': [question[1].index for question in self.question_list]
        }
        result = collection.insert_one(hot_list)
        return result

    def _get_hot_question_list(self):
        setting = db.setting.find_one({'_id': 1})
        hot_list_thread = setting['hot_list_thread']  # 解析热榜所用线程数量
        print('解析热榜线程数：'+str(hot_list_thread))

        start = time.perf_counter()

        response = requests.get('https://www.zhihu.com/hot', headers=self.headers, timeout=10)
        soup = BeautifulSoup(response.text, 'lxml')
        hot_node = soup.find(name='div', attrs={'class': 'Topstory-hot HotList'}).children
        question_url = re.compile('https://www.zhihu.com/question/\d+')

        executor = ThreadPoolExecutor(max_workers=hot_list_thread)
        fs = [executor.submit(self._analysis_hot_list_html, child, question_url) for child in hot_node]
        # question_list = [future.result() for future in as_completed(fs)]
        question_list = []
        for future in as_completed(fs):
            new_question = future.result()
            if new_question is not None:
                question_list.append(new_question)

        question_list.sort(key=lambda rank_and_question_tuple: rank_and_question_tuple[0])

        end = time.perf_counter()
        print('总用时：'+str(end-start)+'s')

        return question_list

    def _analysis_hot_list_html(self, node, question_url):
        rank = int(node.find(name='div', attrs={'class': 'HotItem-index'}).find(name='div').text)
        hotItem_content = node.find(name='div', attrs={'class': 'HotItem-content'})
        a = hotItem_content.find(name='a')
        index_str = a['href']
        if not re.match(question_url, index_str):
            return None
        index = int(index_str[index_str.rindex('/') + 1:])
        heat = float(re.match('(\d+).*', hotItem_content.find(name='div').text).group(1))
        question = Question(rank, index, heat, save_answer=self._save_answer)
        question.save()
        return rank, question

    def __str__(self):
        hot_list = ''
        for question in self.question_list:
            hot_list = hot_list + '-------------------------------\n' + str(question[1]) + '\n'
        return hot_list

def get_answers(question_index, limit=10, exec_delete=False):
    if exec_delete:
        db['question_' + str(question_index)].delete_many({}) # 先清空原有的答案

    start = time.perf_counter()

    setting = db.setting.find_one({'_id': 1})
    answer_thread = setting['answer_thread']  # 爬取答案所用线程数量
    answer_num = setting['answer_num']  # 爬取答案数
    sensitive_words = setting['sensitive_words'] # 敏感词

    headers = {
        'User-Agent': user_agent,
        'Cookie': cookie,
        'X-Requested-With': 'fetch'
    }
    url = 'https://www.zhihu.com/api/v4/questions/'+str(question_index)+'?include=answer_count'
    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            answer_count = int(response.json()['answer_count']) # 获得答案数
        else:
            print('获取页面信息错误')
            return
    except requests.ConnectionError as e:
        print('Error', e.args)
        return

    print('爬取答案线程数：' + str(answer_thread))
    # print('回答总数：'+str(answer_count)+'\n设置最大爬取回答数：'+str(answer_num))
    print('共需要爬取'+str((min(answer_num, answer_count+limit)//limit)*limit)+'条回答')

    if len(sensitive_words) == 1:
        algorithm = BM(sensitive_words[0])
    elif len(sensitive_words) > 1:
        algorithm = AC(sensitive_words)
    else:
        algorithm = None

    fs = []
    executor = ThreadPoolExecutor(max_workers=answer_thread)
    for offset in range(min(answer_num, answer_count+limit)//limit):
        future = executor.submit(get_some_answers, question_index, headers, offset*10, algorithm)
        fs.append(future)
    wait(fs)

    end = time.perf_counter()

    print('总用时：'+str(end-start)+'s')

def get_some_answers(question_index, headers, offset, filter_algorithm=None, limit=10):
    base_url = 'https://www.zhihu.com/api/v4/questions/' + str(question_index) + '/answers?include=data%5B%2A%5D.is_normal' \
               '%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail' \
               '%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%' \
               '2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission' \
               '%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt' \
               '%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled' \
               '%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A' \
               '%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&'
    answer_index = offset
    params = {
        'limit': limit,
        'offset': offset,
        'platform': 'desktop',
        'sort_by': 'default'
    }
    s = requests.Session()

    url = base_url + urlencode(params)
    try:
        response = s.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            answers_json = response.json()['data']
        else:
            return
    except requests.ConnectionError as e:
        print('Error', e.args)
        return

    for answer in answers_json:
        content = answer['content'].replace('<br/>', '\n')
        if filter_algorithm is not None and filter_algorithm.find(content) != -1:
            continue
        soup = BeautifulSoup(content, 'lxml')
        text = ''
        for node in soup.find(name='body'):
            if node.name == 'p' and node.text != '\n':
                text += node.text + '\n'
            elif node.name == 'figure':
                text += ' [图片]\n'
            elif node.name == 'blockquote':
                text += '  ' + node.text
            elif node.name == 'ul':
                for child in node.children:
                    if child.text == '': continue
                    text += '  ·' + child.text + '\n'
        author = answer['author']['name']
        gender = answer['author']['gender']
        voteup_count = int(answer['voteup_count'])
        comment_count = int(answer['comment_count'])

        collection = db['question_' + str(question_index)]
        answer = {
            '_id': answer_index,
            'author': author,
            'gender': gender,
            'voteup_count': voteup_count,
            'comment_count': comment_count,
            'content': text,
        }
        collection.insert_one(answer)
        answer_index = answer_index + 1

def clear_cache():
    Hot_List()
    setting = db.setting.find_one({'_id': 1})
    interval = setting['interval']
    if interval == 86400:
        print('将清理1天之前的数据...')
    elif interval == 604800:
        print('将清理7天之前的数据...')
    else:
        print('将清理30天之前的数据...')
    long_long_ago = time.time()-interval
    db.hot_list.delete_many({'_id':{'$lt':long_long_ago}})
    db.question.delete_many({'record_time':{'$lt':long_long_ago}})
    db.question_trend.delete_many({'record_time':{'$lt':long_long_ago}})

if __name__ == "__main__":
    get_answers(328401813)
    get_answers(328401813)
    get_answers(328401813)