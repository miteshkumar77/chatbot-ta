from rtree import index
import sqlite3
import json
import numpy as np

def build_content_index(content_json_file : str):
    db = sqlite3.connect('./storage/content.db')
    cursor = db.cursor()
    cursor.execute(
        '''DROP TABLE IF EXISTS content_table;'''
    )
    cursor.execute(
        '''CREATE TABLE content_table (
                url TEXT PRIMARY KEY,
                content TEXT
            );'''
    )
    db.commit()
    with open(content_json_file, 'r') as rfp:
        js = json.loads(rfp.read())
        for k, v in js.items():
            cursor.execute(
                f'''INSERT INTO content_table (url, content)
                    VALUES(?,?);''', (k, v['content'])
            )
            db.commit()
    cursor.close()

def build_keyword_index(spatial_json_file : str):
    with open(spatial_json_file, 'r') as rfp:
        p = index.Property()
        js = json.load(rfp)
        p.dat_extension = 'data'
        p.idx_extension = 'index'
        p.dimension = np.asarray(json.loads(next(iter(js['vec2url'].keys())))).shape[0]
        p.overwrite = True
        
        idxnd = index.Index('./storage/keyword_index', properties=p)
        with open('./storage/keyword_index.json', 'w') as wfp:
            p.overwrite = False
            json.dump(p.as_dict(), wfp)
        id_cnt = 0
        for wv_str, urls in js['vec2url'].items():
            wv_ndarr = np.asarray(json.loads(wv_str))
            wv_coord = tuple(np.concatenate((wv_ndarr, wv_ndarr)))
            idxnd.insert(id=id_cnt, coordinates=wv_coord, obj=urls)
            id_cnt += 1


        


if __name__ == '__main__':
    build_content_index('./preprocessed-scraper_output.json')
    build_keyword_index('./keyword-scraper_output.json')