import argparse
import pandas as pd
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

tokenizer = AutoTokenizer.from_pretrained("google/pegasus-xsum")
model = AutoModelForSeq2SeqLM.from_pretrained("google/pegasus-xsum")

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

def abs_summarization(config):
    df = pd.read_csv(config.load_path)

    summary_decode_list = []

    for text in df['내용']:
        tokens = tokenizer(text, truncation=True, padding="longest", return_tensors="pt")
        summary = model.generate(**tokens) 
        summary_decode = tokenizer.decode(summary[0]) 
        summary_decode = summary_decode.replace("<pad> ", '') 
        summary_decode = summary_decode.replace("</s>", '')
        summary_decode_list.append(summary_decode)

    summary_decode_list.to_csv(config.save_path,'abstractive_summarization_PEGASUS.csv')

if __name__ == "__main__":
    config = define_argparser()
    abs_summarization(config)