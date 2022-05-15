import spacy
from functools import lru_cache
import gensim.downloader
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
import re

nlp : spacy.Language = None
word2vec = None
spacy_lang : str = 'en_core_web_sm'

def kwd_setup():
    global nlp
    global word2vec
    if nlp is None:
        nlp = spacy.load(spacy_lang)
    if word2vec is None:
        word2vec = KeyedVectors.load_word2vec_format('./models/SO_vectors_200.bin', binary=True)
    # word2vec = gensim.downloader.load('glove-wiki-gigaword-300')


@lru_cache(maxsize=None)
def wv_helper(word : str, to_str=True):
    try:
        if to_str:
            wv_str = str(get_closest_word_vector(word).tolist())
        else:
            wv_str = get_closest_word_vector(word).tolist()
    except KeyError:
        wv_str = None
    return wv_str

def get_closest_word_vector(word : str) -> np.ndarray:
    return word2vec[word2vec.most_similar(re.sub('[^a-z]+', '', word.lower()), topn=1)[0][0]]

def get_keywords(text):
    global nlp
    return [w.text for w in nlp(text) if w.pos_ in ('NOUN', 'VERB')]


if __name__ == '__main__':
    kwd_setup()
    print(get_closest_word_vector('Capstone').shape)
    print(get_keywords("Where is the statement of work submitted?"))
