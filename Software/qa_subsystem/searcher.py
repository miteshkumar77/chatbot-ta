import sqlite3
from rtree import index
import json
import numpy as np
from collections import defaultdict
from kwd import kwd_setup, get_closest_word_vector, get_keywords

class InvertedIndex():

    def __init__(self, content_index_name : str, keyword_index_name : str):
        self.content_index_name = content_index_name
        self.keyword_index_name = keyword_index_name
        kwd_setup()


    def retrieve_relevant_documents(self, question: str, topn: int, k: int):
        content_db = sqlite3.connect(self.content_index_name)
        with open(self.keyword_index_name + '.json', 'r') as rfp:
            p = index.Property()
            p.initialize_from_dict(json.load(rfp))
            keyword_db = index.Index(self.keyword_index_name, properties=p)

        keywords = get_keywords(question)
        wordvectors = []
        for keyword in keywords:
            try:
                wordvectors.append(get_closest_word_vector(keyword))
            except KeyError:
                continue

        url_cnt = defaultdict(lambda : 0)
        for wv in wordvectors:
            for url_list in keyword_db.nearest(tuple(wv), num_results=k, objects='raw'):
                for url in url_list:
                    url_cnt[url] += 1
        url_cnt = sorted(list(url_cnt.items()), key=lambda x : -1 * x[1])
        url_cnt = url_cnt[:min(len(url_cnt), topn)]

        cursor = content_db.cursor()
        cursor.execute('CREATE TEMPORARY TABLE rel_urls (url TEXT);')
        cursor.executemany(
            '''INSERT INTO rel_urls (url)
                VALUES (?);''', [[x[0]] for x in url_cnt])
        cursor.execute(
            '''SELECT c.url, c.content
                FROM content_table as c, rel_urls as r
                WHERE c.url = r.url;'''
        )
        ret = cursor.fetchall()
        cursor.execute(
            '''DROP TABLE rel_urls'''
        )
        cursor.close()
        content_db.commit()
        content_db.close()
        return ret




if __name__ == '__main__':
    iidx = InvertedIndex('./storage/content.db', './storage/keyword_index')
    print(iidx.retrieve_relevant_documents('Where can I find a CPU or microcontroller?', topn=2, k=20))