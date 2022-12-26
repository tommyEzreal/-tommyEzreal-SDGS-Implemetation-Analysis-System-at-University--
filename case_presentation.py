import argparse
import pandas as pd
import numpy as np
import os

from sklearn.feature_extraction.text import TfidfVectorizer
from sentence_transformers import SentenceTransformer, util

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

def listToString(str_list):
    result = ""
    for s in str_list:
        result += s + " "
    return result.strip()

def case_presentation(config):
    
    ab_ext = pd.read_csv(config.load_path, 'extractive_summarization_PEGASUS.csv')
    ab_gen = pd.read_csv(config.load_path, 'abstractive_summarization_TextRank.csv')

    path = config.load_path

    # 해외전체대학 5분류 키워드 가져오기
    ab_file_list = os.listdir(path)
    ab_file_list_py = [file for file in ab_file_list if file.startswith('해외대학_textrank')]
    ab_file_list_py.sort()

    # csv 파일들마다 DataFrame 할당하기
    ab_kw_dfs = []

    for i in ab_file_list_py:
        globals()['ab_kw'+i.split('.')[0][-4]] = pd.read_csv(path + i) # Dataframe 할당
        print('ab_kw'+i.split('.')[0][-4]) # Dataframe 이름 확인
        ab_kw_dfs.append(globals()['ab_kw'+i.split('.')[0][-4]])
    
    # 국내개별대학 5분류 키워드 가져오기
    kr_file_list = os.listdir(path)
    kr_file_list_py = [file for file in kr_file_list if file.startswith('한양_textrank')]
    kr_file_list_py.sort()
    print(kr_file_list_py)

    # csv 파일들마다 DataFrame 할당하기
    kr_kw_dfs = []

    for i in kr_file_list_py:
        globals()['kr_kw'+i.split('.')[0][-4]] = pd.read_csv(path + i) # Dataframe 할당
        print('kr_kw'+i.split('.')[0][-4]) # Dataframe 이름 
        kr_kw_dfs.append(globals()['kr_kw'+i.split('.')[0][-4]])
    
    # 해외 키워드 및 국내개별대학 키워드 리스트 생성

    ab_kw_list_dfs = []
    kr_kw_list_dfs = []

    for i in range(5):
        globals()['ab_kw_list'+str(i+1)] = []
        globals()['kr_kw_list'+str(i+1)] = []

        for kw in ab_kw_dfs[i]['키워드']:
            globals()['ab_kw_list'+str(i+1)].append(kw)
        ab_kw_list_dfs.append(globals()['ab_kw_list'+str(i+1)]) # ab_kw_list_dfs 리스트에 합치기

        for kw in kr_kw_dfs[i]['키워드']:
            globals()['kr_kw_list'+str(i+1)].append(kw)
        kr_kw_list_dfs.append(globals()['kr_kw_list'+str(i+1)]) # kr_kw_list_dfs 리스트에 합치기

    # 겹치는 키워드 확인 

    intersection_all = []

    for i in range(5):
        globals()['intersection'+str(i+1)] = list(set(ab_kw_list_dfs[i]).intersection(kr_kw_list_dfs[i]))
        print(globals()['intersection'+str(i+1)])
        intersection_all.append(globals()['intersection'+str(i+1)])

    # 해외전체대학 키워드 - 국내개별대학 키워드 리스트 생성

    save_idx = []
    ab_kw_left_dfs = []

    for idx, intersection in enumerate(intersection_all):
        if len(intersection) != 0: # 겹치는 키워드가 존재한다면
            globals()['ab_kw_left_df'+str(idx+1)] = list(set(ab_kw_list_dfs[idx]).difference(kr_kw_list_dfs[idx]))
            ab_kw_left_dfs.append(globals()['ab_kw_left_df'+str(idx+1)])
            save_idx.append(idx+1)
    
    # 키워드 응집문장 생성
    key_sent_list = []

    for idx, df in enumerate(ab_kw_left_dfs):
        key_sent = listToString(df)
        key_sent_list.append(key_sent)
    
    # 해외대학데이터_추출요약 분류별 데이터프레임 할당
    ab_ext_dfs = []

    for i in range(1, 6):
        if i in save_idx:
            globals()['ab_ext'+str(i)] = ab_ext[(ab_ext['5분류']==i)]
            globals()['ab_ext'+str(i)].reset_index(drop=True, inplace=True)
            globals()['ab_ext'+str(i)].to_csv(f'/content/drive/MyDrive/[해외사례제시]/intersection_not exist_random/추출요약랜덤제시{i}번.csv')
            ab_ext_dfs.append(globals()['ab_ext'+str(i)])

    # 해외대학데이터_생성요약 분류별 데이터프레임 할당
    ab_gen_dfs = []

    for i in range(1, 6):
        if i in save_idx:
            globals()['ab_gen'+str(i)] = ab_gen[(ab_gen['5분류']==i)]
            globals()['ab_gen'+str(i)].reset_index(drop=True, inplace=True)
            globals()['ab_gen'+str(i)].to_csv(f'/content/drive/MyDrive/[해외사례제시]/intersection_not exist_random/생성요약랜덤제시{i}번.csv')
            ab_gen_dfs.append(globals()['ab_gen'+str(i)])
    
    # 키워드 문장 상단에 삽입

    key_sent_ext_list = []
    key_sent_gen_list = []

    for idx, key_sent in enumerate(key_sent_list):
        key_sent_ext = ['0', '0', '0', '0', '0', key_sent, 0, save_idx[idx]+1]
        key_sent_gen = ['0', '0', '0', '0', key_sent, 0, save_idx[idx]+1]
        
        key_sent_ext_list.append(key_sent_ext)
        key_sent_gen_list.append(key_sent_gen)

    for idx, df in enumerate(ab_ext_dfs):
        df.loc[0] = key_sent_ext_list[idx]

    for idx, df in enumerate(ab_gen_dfs):
        df.loc[0] = key_sent_gen_list[idx]

def ext_sum_similarity(config):

    ab_ext_doc_list = []

    for idx, df in enumerate(ab_ext_dfs):
        globals()['ab_ext_doc'+str(idx+1)] = df['추출요약'].to_list()
        print(globals()['ab_ext_doc'+str(idx+1)])
        ab_ext_doc_list.append(globals()['ab_ext_doc'+str(idx+1)])

    # 객체 생성
    tfidf_vectorizer = TfidfVectorizer()

    for idx, df in enumerate(ab_ext_dfs):
        for sent in df['추출요약']:
            sent = (key_sent_list[idx], sent)
            # 문장 벡터화 진행
            tfidf_matrix = tfidf_vectorizer.fit_transform(sent)
            # 각 단어
            text = tfidf_vectorizer.get_feature_names_out()
            # 각 단어의 벡터 값
            idf = tfidf_vectorizer.idf_
    
    model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    embeddings_ext_all = []
    cosine_scores_ext_all = []

    for idx, doc_list in enumerate(ab_ext_doc_list):
        globals()['embeddings_ext'+str(idx+1)] = model.encode(doc_list, convert_to_tensor=True)
        globals()['cosine_scores_ext'+str(idx+1)] = util.pytorch_cos_sim(globals()['embeddings_ext'+str(idx+1)], globals()['embeddings_ext'+str(idx+1)])

        embeddings_ext_all.append(globals()['embeddings_ext'+str(idx+1)])
        cosine_scores_ext_all.append(globals()['cosine_scores_ext'+str(idx+1)])

    # 키워드 응집문장
    embeddings_tar_all = []
    cosine_scores_tar_all = []

    for idx, key_sent in enumerate(key_sent_list):
        globals()['embeddings_tar'+str(idx+1)] = model.encode(key_sent, convert_to_tensor=True)
        globals()['cosine_scores_tar'+str(idx+1)] = util.pytorch_cos_sim(globals()['embeddings_tar'+str(idx+1)], globals()['embeddings_tar'+str(idx+1)])

        embeddings_tar_all.append(globals()['embeddings_tar'+str(idx+1)])
        cosine_scores_tar_all.append(globals()['cosine_scores_tar'+str(idx+1)])

    # 정렬
    org = 0

    temp_ext_all = []
    sim_index_ext_all = []
    sim_sent_ext_all = []

    for idx, cosine_scores_ext in enumerate(cosine_scores_ext_all):
        globals()['temp_ext'+str(idx+1)] = cosine_scores_ext[org]
        globals()['temp_ext'+str(idx+1)].argsort(descending=True)[0:100]
        
        globals()['sim_index'+str(idx+1)] = []
        globals()['sim_sent'+str(idx+1)] = []

        sim_index_ext_all.append(globals()['sim_index'+str(idx+1)])
        sim_sent_ext_all.append(globals()['sim_sent'+str(idx+1)])

        for i in globals()['temp_ext'+str(idx+1)].argsort(descending=True)[0:100]:
            print(f"{i}. {ab_ext_doc_list[idx][i]} \nScore: {cosine_scores_ext[org][i]:.4f}\n")
            globals()['sim_index'+str(idx+1)].append(i)
            globals()['sim_sent'+str(idx+1)].append(ab_ext_doc_list[idx][i])

    # 데이터프레임 생성
    extract_dfs = []

    for idx, df in enumerate(ab_ext_dfs):
        globals()['extract'+str(idx+1)] = df.loc[sim_index_ext_int_all[idx], ['국가', '대학교명', '내용', '번역', '영한_재번역', '추출요약', '분류', '5분류']]
        extract_dfs.append(globals()['extract'+str(idx+1)])

    # csv 파일로 내보내기
    for idx, df in enumerate(extract_dfs):
        df.to_csv(config.save_path, f'{save_idx[idx]}번.csv')

def abs_sum_similarity(config):

    ab_gen_doc_list = []

    for idx, df in enumerate(ab_gen_dfs):
        globals()['ab_gen_doc'+str(idx+1)] = df['요약번역'].to_list()
        print(globals()['ab_gen_doc'+str(idx+1)])
        ab_gen_doc_list.append(globals()['ab_gen_doc'+str(idx+1)])

    # 객체 생성
    tfidf_vectorizer = TfidfVectorizer()

    for idx, df in enumerate(ab_gen_dfs):
        for sent in df['요약번역']:
            sent = (key_sent_list[idx], sent)
            # 문장 벡터화 진행
            tfidf_matrix = tfidf_vectorizer.fit_transform(sent)
            # 각 단어
            text = tfidf_vectorizer.get_feature_names_out()
            # 각 단어의 벡터 값
            idf = tfidf_vectorizer.idf_
            print(dict(zip(text, idf)))

    model = SentenceTransformer('paraphrase-distilroberta-base-v1')

    embeddings_gen_all = []
    cosine_scores_gen_all = []

    for idx, doc_list in enumerate(ab_gen_doc_list):
        globals()['embeddings_gen'+str(idx+1)] = model.encode(doc_list, convert_to_tensor=True)
        globals()['cosine_scores_gen'+str(idx+1)] = util.pytorch_cos_sim(globals()['embeddings_gen'+str(idx+1)], globals()['embeddings_gen'+str(idx+1)])

        embeddings_gen_all.append(globals()['embeddings_gen'+str(idx+1)])
        cosine_scores_gen_all.append(globals()['cosine_scores_gen'+str(idx+1)])
    
    # 키워드 응집문장
    embeddings_tar_all = []
    cosine_scores_tar_all = []

    for idx, key_sent in enumerate(key_sent_list):
        globals()['embeddings_tar'+str(idx+1)] = model.encode(key_sent, convert_to_tensor=True)
        globals()['cosine_scores_tar'+str(idx+1)] = util.pytorch_cos_sim(globals()['embeddings_tar'+str(idx+1)], globals()['embeddings_tar'+str(idx+1)])

        embeddings_tar_all.append(globals()['embeddings_tar'+str(idx+1)])
        cosine_scores_tar_all.append(globals()['cosine_scores_tar'+str(idx+1)])

    # 정렬
    org = 0

    temp_gen_all = []
    sim_index_gen_all = []
    sim_sent_gen_all = []

    for idx, cosine_scores_gen in enumerate(cosine_scores_gen_all):
        globals()['temp_gen'+str(idx+1)] = cosine_scores_gen[org]
        globals()['temp_gen'+str(idx+1)].argsort(descending=True)[0:100]
        
        globals()['sim_index'+str(idx+1)] = []
        globals()['sim_sent'+str(idx+1)] = []

        sim_index_gen_all.append(globals()['sim_index'+str(idx+1)])
        sim_sent_gen_all.append(globals()['sim_sent'+str(idx+1)])

        for i in globals()['temp_gen'+str(idx+1)].argsort(descending=True)[0:100]:
            print(f"{i}. {ab_gen_doc_list[idx][i]} \nScore: {cosine_scores_gen[org][i]:.4f}\n")
            globals()['sim_index'+str(idx+1)].append(i)
            globals()['sim_sent'+str(idx+1)].append(ab_gen_doc_list[idx][i])
    
    # 데이터프레임 생성
    generate_dfs = []

    for idx, df in enumerate(ab_gen_dfs):
        globals()['generate'+str(idx+1)] = df.loc[sim_index_gen_int_all[idx], ['국가', '대학교명', '내용', '요약', '요약번역', '분류', '5분류']]
        generate_dfs.append(globals()['generate'+str(idx+1)])

    # csv 파일로 내보내기
    for idx, df in enumerate(generate_dfs):
        df.to_csv(f'/content/drive/MyDrive/[해외사례제시]/intersection_exist/생성요약제시/생성요약_한양_{save_idx[idx]}번.csv')

if __name__ == '__main__':
    config = define_argparser()
    case_presentation(config)
    ext_sum_similarity(config)
    abs_sum_similarity(config)