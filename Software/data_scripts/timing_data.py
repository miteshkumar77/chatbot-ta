from regex import D
import requests
from urllib.parse import urljoin
import json
import numpy as np

import pandas as pd

def time_question(question, ask_endpoint):
    return requests.post(url=ask_endpoint, data=json.dumps({'question': question})).elapsed.total_seconds()

if __name__ == '__main__':

    questions = [
    "What are vendors of microcontrollers?",
    "Where can I find microcontrollers or CPUs?",
    "What is SVN?",
    "What is the final deliverable in capstone?",
    "Where are the templates for design reports located?",
    "How do I order parts?",
    "How do I resolve an issue?",
    "How do I upload to the repository?",
    "What are the learning goals of capstone?"
    ]
    server_url = "http://45.77.102.63:8000"
    ask_endpoint = urljoin(server_url, 'ask')
    timings = list(map(lambda q : time_question(q, ask_endpoint), questions))
    d = [[questions[i], timings[i]] for i in range(len(questions))]
    df = pd.DataFrame(data=d, columns=('question', 'time'), dtype=('str', 'float'))
    with open('timing_table.csv', 'w') as fp:
        fp.write(df.to_csv())

