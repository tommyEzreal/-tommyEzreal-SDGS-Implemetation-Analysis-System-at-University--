from konlpy.tag import Hannanum
from tqdm import tqdm
import re
import argparse
import pandas as pd
from pandas import DataFrame 
import numpy as np
import csv
from pprint import pprint

import pyLDAvis.gensim_models as gensimvis
import pyLDAvis
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt

from gensim.models.ldamodel import LdaModel
from gensim.models.callbacks import CoherenceMetric
from gensim import corpora
from gensim.models.callbacks import PerplexityMetric

import logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

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

def clean_text(text):
    text = text.replace(".", "").strip()
    text = text.replace("·", " ").strip()
    pattern = '[^ ㄱ-ㅣ가-힣|0-9]+'
    text = re.sub(pattern=pattern, repl='', string=text)
    return text

def get_nouns(tokenizer, sentence):
    tagged = tokenizer.pos(sentence, ntags=22) # ntag = 22로 지정
    nouns = [s for s, t in tagged if t in ['NC', 'NQ', 'PV', 'PA'] and len(s) > 1] # 보통명사, 고유명사, 동사, 형용사
    return nouns

def tokenize(df):
    tokenizer = Hannanum()
    processed_data = []
    for sent in tqdm(df['번역_전처리']):
        sentence = clean_text(str(sent).replace("\n", "").strip())
        processed_data.append(get_nouns(tokenizer, sentence))
    return processed_data

def save_processed_data(processed_data):
    with open("tokenized_data_"+ "토픽모델링", 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        for data in processed_data:
            writer.writerow(data)

def save_tokenized_data(config):
    df = pd.read_csv(config.load_path)
    df.columns=['국가', '대학교명', '내용', '번역', '분류', '번역_전처리']
    df.dropna(how='any')
    processed_data = tokenize(df)
    save_processed_data(processed_data)

def modeling():
    processed_data = [sent.strip().split(",") for sent in tqdm(open("tokenized_data_"+ "토픽모델링",'r',encoding='utf-8').readlines())]
    processed_data = DataFrame(processed_data)
    processed_data[0] = processed_data[0].replace("", np.nan)
    processed_data = processed_data[processed_data[0].notnull()]
    processed_data = processed_data.values.tolist()
    processed_data2=[]

    for i in processed_data:
        i = list(filter(None, i))
        processed_data2.append(i)
    processed_data = processed_data2
    processed_data

    dictionary = corpora.Dictionary(processed_data)
    corpus = [dictionary.doc2bow(text) for text in processed_data]

    num_topics = 5
    chunksize = 2000
    passes = 20
    iterations = 400
    eval_every = None

    temp = dictionary[0]
    id2word = dictionary.id2token

    model = LdaModel(
        corpus=corpus,
        id2word=id2word,
        chunksize=chunksize,
        alpha='auto',
        eta='auto',
        iterations=iterations,
        num_topics=num_topics,
        passes=passes,
        eval_every=eval_every
    )

    top_topics = model.top_topics(corpus) 

    avg_topic_coherence = sum([t[1] for t in top_topics]) / num_topics
    print('Average topic coherence: %.4f.' % avg_topic_coherence)
    pprint(top_topics)

    data = data.drop(columns='분류')
    lda_visualization = gensimvis.prepare(model, corpus, dictionary, sort_topics=False)
    pyLDAvis.save_html(lda_visualization, 'file_name.html')

if __name__ == '__main__':
    config = define_argparser()
    save_tokenized_data(config)
    modeling()