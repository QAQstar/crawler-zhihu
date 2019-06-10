# -*- coding: utf-8 -*-
import re
import jieba
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout, Activation
import sklearn.model_selection
# import logging
import numpy as np
# import gensim
# from gensim.models.word2vec import Word2Vec
from gensim.corpora.dictionary import Dictionary
import pickle

vocab_dim = 100  # 向量维度
maxlen = 200  # 文本保留的最大长度
batch_size = 32     # 每次梯度更新的样本数
# n_epoch = 5        # 训练模型轮数
np.random.seed(1337)  # For Reproducibility
min_count = 10
window = 5

# 文本分词
def to_train_vec2(sentence_list):
    result = []
    for i in range(len(sentence_list)):
        sentence = sentence_list[i]
        sentence = sentence.replace('\n', '')
        # sentence = re.sub('\n', '', sentence)
        if sentence != '':
            result.append(jieba.lcut(sentence))

    return result


# 创建词语字典，并返回word2vec模型中词语的索引，词向量
def create_dictionaries(p_model):
    gensim_dict = Dictionary()
    gensim_dict.doc2bow(p_model.wv.vocab.keys(), allow_update=True)
    w2indx = {}
    for k, v in gensim_dict.items():
        w2indx[v] = k + 1   # 词语的索引，从1开始编号
    w2vec = {}
    for word in w2indx.keys():
        w2vec[word] = p_model[word]
    return w2indx, w2vec

def text_to_index_array(p_new_dic, p_sen):  # 文本转为索引数字模式
    new_sentences = []
    for sen in p_sen:
        new_sen = []
        for word in sen:
            new_sen.append(p_new_dic.get(word, 0))  # 单词转索引数字，索引字典里没有的词转为数字0
        new_sentences.append(new_sen)
    return np.array(new_sentences)

def retrain(train_rounds, sentences_and_labels_path='sentences_and_labels.pkl', vec_path='vec_lstm.pkl',
            model_path='lstmModel.pkl'):
    # 读取大语料文本
    with open(vec_path, 'rb') as f: # 预先训练好的
        index_dict = pickle.load(f) # 索引字典，{单词: 索引数字}
        word_vectors = pickle.load(f)

    print("Setting up Arrays for Keras Embedding Layer...")
    n_symbols = len(index_dict) + 1  # 索引数字的个数，因为有的词语索引为0，所以+1
    embedding_weights = np.zeros((n_symbols, vocab_dim))  # 创建一个n_symbols * vocab_dim的0矩阵
    for w, index in index_dict.items():  # 从索引为1的词语开始，用词向量填充矩阵
        embedding_weights[index, :] = word_vectors[w]  # 词向量矩阵，第一行是0向量（没有索引为0的词语，未被填充）

    # 读取语料分词文本，转为句子列表（句子为词汇的列表）
    # 读取语料类别标签
    # print u"请选择语料的类别文本...（用0，1分别表示消极、积极情感）"
    with open(sentences_and_labels_path, 'rb') as f:
        allsentences = pickle.load(f)
        labels = pickle.load(f)

    # 划分训练集和测试集，此时都是list列表
    X_train_l, X_test_l, y_train_l, y_test_l = \
        sklearn.model_selection.train_test_split(allsentences, labels, test_size=0.2)
    # 转为数字索引形式
    X_train = text_to_index_array(index_dict, X_train_l)
    X_test = text_to_index_array(index_dict, X_test_l)
    print("训练集shape： ", X_train.shape)
    print("测试集shape： ", X_test.shape)
    # 转numpy数组
    y_train = np.array(y_train_l)
    y_test = np.array(y_test_l)
    # 将句子截取相同的长度maxlen，不够的补0
    print('Pad sequences (samples x time)')
    X_train = sequence.pad_sequences(X_train, maxlen=maxlen)
    X_test = sequence.pad_sequences(X_test, maxlen=maxlen)
    print('X_train shape:', X_train.shape)
    print('X_test shape:', X_test.shape)

    X_train2 = text_to_index_array(index_dict, allsentences)
    y_train2 = np.array(labels)
    X_train2 = sequence.pad_sequences(X_train2, maxlen=maxlen)

    model = get_model(n_symbols, embedding_weights, X_train2, y_train2, X_test, y_test, n_epoch=train_rounds)
    dump_model(model, model_path)

def get_model(p_n_symbols, p_embedding_weights, complete_train, complete_train_tag, p_X_test, p_y_test, n_epoch=5):
    print('创建模型...')
    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim,
                        input_dim=p_n_symbols,
                        mask_zero=True,
                        weights=[p_embedding_weights],
                        input_length=maxlen))
    model.add(LSTM(output_dim=50,
                   activation='sigmoid',
                   inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5))
    model.add(Dense(1))  # 隐藏层，全连接层数为1
    model.add(Activation('sigmoid'))
    print('编译模型...')
    model.compile(loss='binary_crossentropy',
                  optimizer='adam',
                  metrics=['accuracy'])
    print("训练...")
    model.fit(complete_train, complete_train_tag, batch_size=batch_size, epochs=n_epoch,
              validation_data=(p_X_test, p_y_test))
    return model

def get_index_dict(vet_path='vec_lstm.pkl'):
    with open(vet_path, 'rb') as f: # 预先训练好的
        index_dict = pickle.load(f)  # 索引字典，{单词: 索引数字}
    return index_dict

def dump_model(model, path='lstmModel.pkl'):
    with open(path, 'wb') as f:
        pickle.dump(model, f)

def get_result(test, vec_path='vec_lstm.pkl', model_path='lstmModel.pkl'):
    with open(model_path, 'rb') as model_file:
        model = pickle.load(model_file)
    with open(vec_path, 'rb') as f:
        index_dict = pickle.load(f)
    to_test_sentences = to_train_vec2(test)
    X_test2 = sequence.pad_sequences(text_to_index_array(index_dict, to_test_sentences), maxlen=maxlen)
    print("评估...")
    result_temp = model.predict(X_test2, batch_size=None, verbose=0, steps=None)
    result = [item[0] for item in result_temp]
    return result


if __name__ == "__main__":
    print(get_result(['老大真强', '今天天气特别好', '今天天气特别差', '我好菜啊', '我终于写完实验啦！！！']))