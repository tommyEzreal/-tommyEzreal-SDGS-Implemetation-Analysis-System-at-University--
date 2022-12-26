import re
import argparse
import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize
from konlpy.tag import Okt, Komoran, Kkma, Hannanum, Mecab


def define_argparser():
    p = argparse.ArgumentParser()

    p.add_argument(
        "--load_path",
        required=True,
        help="Path to load data file."
    )
    p.add_argument(
        "--save_path",
        required=True,
        help="Path to save preprocessed dataset."
    )

    config = p.parse_args()

    return config

def pagerank(x, df=0.85, max_iter=30):
    assert 0 < df < 1

    # initialize
    A = normalize(x, axis=0, norm='l1') 
    R = np.ones(A.shape[0]).reshape(-1,1) 
    bias = (1 - df) * np.ones(A.shape[0]).reshape(-1,1) 

    # iteration
    for _ in range(max_iter): 
        R = df * (A * R) + bias

    return R

def ext_summarization(config):

    data = pd.read_csv(config.load_path)

    total_text = []
    for text in data['번역']:
        total_text.append(text)

    for i, text in enumerate(total_text):
        sentences = re.split("[\.?!]\S+", text)

        globals()[f'data{i}'] = []

        for sentence in sentences:
            if (sentence == "" or len(sentence) == 0):
                continue
            temp_dict = dict()
            temp_dict['sentence'] = sentence
            temp_dict['token_list'] = sentence.split()

            globals()[f'data{i}'].append(temp_dict)

        globals()[f'df{i}'] = pd.DataFrame(globals()[f'data{i}'])

    df_list = [globals()[f'df{i}'] for i in range(7070)]
    df_list = [data for data in df_list]

    total_summary_list = []

    for k, df in enumerate(df_list):

        globals()[f'similarity_matrix{k}'] = []

        for i, row_i in df.iterrows():
            i_row_vec = []
            for j, row_j in df.iterrows():
                if i == j:
                    i_row_vec.append(0.0)
                else:
                    try:
                        intersection = len(set(row_i['token_list']) & set(row_j['token_list']))
                        log_i = math.log(len(set(row_i['token_list'])))
                        log_j = math.log(len(set(row_j['token_list'])))
                        similarity = intersection / (log_i + log_j)
                    except:
                        pass
                    i_row_vec.append(similarity)
            globals()[f'similarity_matrix{k}'].append(i_row_vec)


        weightedGraph = np.array(globals()[f'similarity_matrix{k}'])

        R = pagerank(weightedGraph)

        R = R.sum(axis=1) 
        indexs = R.argsort()[-1:] # 해당 rank 값을 정렬, 값이 높은 1개의 문장 index를 반환

        str_ = []
        for index in sorted(indexs):
            str_.append(df['sentence'][index])
        str_ = " ".join(str_)

        total_summary_list.append(str_)

        data['추출요약'] = total_summary_list

        data.to_csv(config.save_path, 'extractive_summarization_TextRank.csv')

def morphs(df):

    okt = Okt()
    komoran = Komoran()
    kkma = Kkma()
    hannanum = Hannanum()
    mecab = Mecab()

    token_data_okt = []
    token_data_komoran = []
    token_data_kkma = []
    token_data_hannanum = []
    token_data_mecab = []

    for i, row in df.iterrows():
        sentence = row['sentence']
        # okt
        token_list_okt = komoran.nouns(sentence)
        token_data_okt.append(token_list_okt)
        # komoran
        token_list_komoran = komoran.nouns(sentence)
        token_data_komoran.append(token_list_komoran)
        # kkma
        token_list_kkma = komoran.nouns(sentence)
        token_data_kkma.append(token_list_kkma)
        # hannanum
        token_list_hannanum = komoran.nouns(sentence)
        token_data_hannanum.append(token_list_hannanum)
        # mecab
        token_list_mecab = komoran.nouns(sentence)
        token_data_mecab.append(token_list_mecab)

if __name__ == "__main__":
    config = define_argparser()
    ext_summarization(config)