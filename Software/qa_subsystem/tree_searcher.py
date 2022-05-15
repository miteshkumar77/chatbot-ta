import numpy as np
from collections import defaultdict
from kwd import get_closest_word_vector, kwd_setup, get_keywords, wv_helper
from get_tasks_dates import Assignment, Class
from datetime import date
import json
from math import inf


class TreeSearcher():

    def __init__(self, spec_file : str, expanded_file : str):
        kwd_setup()
        with open(spec_file, 'r') as sf, open(expanded_file, 'r') as ef:
            self.spec = json.load(sf)
            self.graph = json.load(ef)
            for node in self.graph.keys():
                for child in self.graph[node].keys():
                    self.graph[node][child]['keywords'] = list(map(
                        lambda x : np.asarray(json.loads(x)),
                        self.graph[node][child]['keywords']
                    ))
        with open('storage/rules/class-sessions.json', 'r') as class_f, \
             open('storage/rules/assignments.json', 'r')    as assign_f, \
             open('storage/rules/other-dates.json', 'r')    as other_f:
            self.classes     = [Class     .from_json_dict(c) for c in json.load(class_f)]
            self.assignments = [Assignment.from_json_dict(a) for a in json.load(assign_f)]
            self.other       = json.load(other_f)

    def get_node(self, id : str):
        return self.spec[id]['display']

    # Try 'upcoming individual assignment due dates'
    def get_assignments(self, query: str):
        kwds = set(get_keywords(query.lower()))
        # kwds = set(query.split())
        graded = 'graded' in kwds
        team = 'team' in kwds or 'group' in kwds
        indv = 'individual' in kwds
        future = 'upcoming' in kwds or 'future' in kwds
        return list(filter(lambda a: (not graded or a.graded)
                                     and (not team or a.team)
                                     and (not indv or a.indv)
                                     and (not future or
                                          ((a.due1 and a.due1 >= date.today())
                                           or (a.due2 and a.due2 >= date.today()))),
                           self.assignments))

    def get_classes(self, query: str):
        kwds = set(get_keywords(query.lower()))
        # kwds = set(query.split())
        future = 'upcoming' in kwds or 'future' in kwds
        return list(filter(lambda c: (not future or
                                      ((c.date1 and c.date1 >= date.today())
                                       or (c.date2 and c.date2 >= date.today()))),
                           self.classes))

    def get_next_node(self, query : str, id : str):
        query = query.lower()
        if id not in self.graph.keys():
            id = 'entry'
        kwds = get_keywords(query)
        wvs = list(filter(lambda x : x is not None, 
            map(lambda x : wv_helper(x, False), kwds)))
        if len(wvs) == 0:
            return {}
        closest_dist = inf
        for wv in wvs:
            for child in self.graph[id].keys():
                for wv_ in self.graph[id][child]['keywords']:
                    closest_dist = min(closest_dist, np.linalg.norm(wv - wv_))

        score = defaultdict(lambda : 0)
        for child in self.graph[id].keys():
            for wv in wvs:
                for wv_ in self.graph[id][child]['keywords']:
                    if np.linalg.norm(wv - wv_) <= closest_dist:
                        score[child] += 1
        
        score = sorted(score.items(), key=lambda x : x[1], reverse=True)
        if len(score) == 0:
            return {}
        return {'node_id': score[0][0],
            'display': self.spec[score[0][0]]['display']}
        

if __name__ == '__main__':
    ts = TreeSearcher('storage/rule_spec.json',
        'storage/expanded_rule_spec.json')
    print(ts.get_next_node('What is Capstone?', 'entry'))




"""
    def get_next_node(self, query : str, id : str):
        print(f'User Query: {query} from node: {id}')
        query = query.lower()
        if id not in self.graph.keys():
            id = 'entry'
        
        kwds = get_keywords(query)
        wvs = list(filter(lambda x : x is not None,
            map(lambda x : wv_helper(x, False), kwds)))
        
        if len(wvs) == 0:
            return {}
        
        highest_dist = float('-inf')
        for child in self.graph[id].keys():
            for wv in wvs:
                for wv_ in self.graph[id][child]['keywords']:
                    highest_dist = max(highest_dist, np.linalg.norm(wv - wv_))
        
        score = defaultdict(lambda : 0)
        for child in self.graph[id].keys():
            for wv in wvs:
                for wv_ in self.graph[id][child]['keywords']:
                    score[child] += np.tan(((highest_dist - np.linalg.norm(wv - wv_)) / highest_dist) * 2.0)

        score = sorted(score.items(), key=lambda x : x[1], reverse=True)
        if len(score) == 0:
            return {}
        return {'node_id': score[0][0],
            'display': self.spec[score[0][0]]['display']}
"""
