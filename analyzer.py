import re
import collections
import argparse

import nltk
import pandas as pd
import fasttext as ft
from nltk.sentiment.vader import SentimentIntensityAnalyzer

from tqdm import tqdm

from preprocess import pre_process
from words import new_words
from plot import Plot


def read_dataset():
    return pd.read_json("result.json")


def initialize():
    PRETRAINED_MODEL_PATH = 'lid.176.bin'
    model = ft.load_model(PRETRAINED_MODEL_PATH)

    analyzer = SentimentIntensityAnalyzer()
    analyzer.lexicon.update(new_words)

    nltk.downloader.download('vader_lexicon', quiet=True)

    return model, analyzer


def execute():
    model, analyzer = initialize()

    df = read_dataset()
    processed_msgs = pre_process(df)

    print("Evaluating sentiments...")
    lines = collections.defaultdict(list)
    for msg, date in tqdm(zip(processed_msgs["Msg"], processed_msgs["Date"])):
        predictions = model.predict(msg)
        if predictions[0][0] == "__label__en":
            msg = re.sub(r"(.)\1\1+", r"\1\1", msg)
            vs = analyzer.polarity_scores(msg)
            lines[date].append(vs["compound"])
    print("Completed")

    op = []
    for k, v in lines.items():
        op.append([k, round(sum(v) / len(v), 4), len(v)])

    return pd.DataFrame(op, columns=['Date', 'Avg sentiment', 'Number of Msgs'])


if __name__ == "__main__":
    # CMD Line argument
    parser = argparse.ArgumentParser()
    parser.add_argument('--show', dest='show', action='store_const', const=True, default=False,
                        help='Show the plots (default: False)')
    args = parser.parse_args()

    # Where the fun happens
    output = execute()

    # Display plot if enabled via --show cmd line argument
    if args.show:
        Plot(output).show()
