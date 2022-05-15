import requests
import json

def ask_question(url, question):
    res = requests.api.post(url, json={"question":question})
    return res.text

if __name__ == '__main__':

    url = "http://127.0.0.1:8000/ask"
    # url = "http://128.113.216.70:8000/ask"
    question = "What is Capstone?"

    tmp_url = input("Endpoint URL (empty for default):")
    if tmp_url != "":
        url = tmp_url

    tmp_question = input("Question (empty for default 'What is Capstone?'")
    if tmp_question != "":
        question = tmp_question

    print(ask_question(url, question))


