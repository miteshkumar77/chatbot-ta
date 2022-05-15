import json
from functools import lru_cache
from kwd import get_closest_word_vector, kwd_setup, wv_helper


    

def build_rule_index(spec_file, output_file):
    kwd_setup()
    with open(spec_file, 'r') as rp, open(output_file, 'w') as wp:
        spec : dict = json.load(rp)
        indices : dict = dict()
        for id, data in spec.items():
            idx = dict()
            for child_id in data['children']:
                idx[child_id] = {
                    'keywords': list(filter(lambda x : x is not None, 
                        map(wv_helper, spec[child_id]['keywords'])))
                }
            indices[id] = idx
        json.dump(indices, wp)


if __name__ == '__main__':
    build_rule_index('storage/rule_spec.json', 'storage/expanded_rule_spec.json')

