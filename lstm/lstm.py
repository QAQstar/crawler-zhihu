# -*- coding: utf-8 -*-
import re
import jieba
from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM
from keras.layers.core import Dense, Dropout, Activation
import sklearn.model_selection
import numpy as np
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
        if sentence != '':
            result.append(jieba.lcut(sentence))

    return result

# 文本转为索引数字模式
def text_to_index_array(index_dict, sentences_list):
    new_sentences = []
    for sentence in sentences_list:
        new_sentence = []
        for word in sentence:
            new_sentence.append(index_dict.get(word, 0))  # 单词转索引数字，索引字典里没有的词转为数字0
        new_sentences.append(new_sentence)
    return np.array(new_sentences)

def retrain(train_rounds, sentences_and_labels_path='sentences_and_labels.pkl', vec_path='vec_lstm.pkl',
            model_path='lstmModel.pkl'):
    # 从之前转储的文件中读取词语的索引字典和分词后的词向量
    # 词向量是之前已经训练好的，代码不在这里
    with open(vec_path, 'rb') as f:
        index_dict = pickle.load(f) # 索引字典，{单词: 索引数字}
        word_vectors = pickle.load(f) # 词向量

    print("Setting up Arrays for Keras Embedding Layer...")
    n_symbols = len(index_dict) + 1  # 索引数字的个数，因为有的词语索引为0(不存在)，所以+1
    embedding_weights = np.zeros((n_symbols, vocab_dim))  # 创建一个n_symbols * vocab_dim的0矩阵
    for w, index in index_dict.items():  # 从索引为1的词语开始，用词向量填充矩阵
        embedding_weights[index, :] = word_vectors[w]  # 词向量矩阵，第一行是0向量（没有索引为0的词语，未被填充）

    # 读取语料分词文本，转为分词集列表（句子为分词集的列表）
    # 读取语料类别标签，0表示消极，1表示积极
    with open(sentences_and_labels_path, 'rb') as f:
        allsentences = pickle.load(f)
        labels = pickle.load(f)

    # 划分训练集和测试集，此时都是list列表
    X_train_l, X_test_l, y_train_l, y_test_l = \
        sklearn.model_selection.train_test_split(allsentences, labels, test_size=0.2)

    # 转为数字索引形式
    test_sentences = text_to_index_array(index_dict, X_test_l)
    print("测试集shape： ", test_sentences.shape)
    # 转numpy数组
    test_sentences_label = np.array(y_test_l)
    # 将句子截取相同的长度maxlen，不够的补0
    test_sentences = sequence.pad_sequences(test_sentences, maxlen=maxlen)

    # train_sentences 是把句子列表转换成单词索引列表后的训练数据
    # train_sentences_label 是对这些句子进行标记
    train_sentences = text_to_index_array(index_dict, allsentences)
    train_sentences = sequence.pad_sequences(train_sentences, maxlen=maxlen)
    train_sentences_label = np.array(labels)

    #指定训练轮数进行训练
    model = get_model(n_symbols, embedding_weights, train_sentences, train_sentences_label, test_sentences,
                      test_sentences_label, n_epoch=train_rounds)
    # dump_model(model, model_path)

def get_model(p_n_symbols, p_embedding_weights, complete_train, complete_train_tag, test, test_label, n_epoch=5):
    print('创建模型...')
    model = Sequential()
    model.add(Embedding(output_dim=vocab_dim, # 输出的维度
                        input_dim=p_n_symbols, # 输入的维度
                        mask_zero=True,
                        weights=[p_embedding_weights], # 提前训练好的词向量
                        input_length=maxlen)) # 输入长度
    model.add(LSTM(output_dim=50,
                   activation='sigmoid', # 激活函数sigmoid
                   inner_activation='hard_sigmoid'))
    model.add(Dropout(0.5)) # 随机失活
    model.add(Dense(1))  # 隐藏层，全连接层数为1
    # model.add(Activation('sigmoid'))
    print('编译模型...')
    model.compile(loss='binary_crossentropy', # 损失函数，二分类
                  optimizer='adam', # 优化器
                  metrics=['accuracy']) # 准确率
    print("训练...")
    model.fit(complete_train, complete_train_tag, batch_size=batch_size, epochs=n_epoch,
              validation_data=(test, test_label))
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
    test_sentences = to_train_vec2(test)
    X_test2 = sequence.pad_sequences(text_to_index_array(index_dict, test_sentences), maxlen=maxlen)
    print("评估...")
    result_temp = model.predict(X_test2, batch_size=None, verbose=0, steps=None)
    result = [item[0] for item in result_temp]
    return result

if __name__ == "__main__":
    print(get_result(['老大真强', '今天天气特别好', '今天天气特别差', '我好菜啊', '我终于写完实验啦！！！']))
    # retrain(5)