import socket
from fastapi import FastAPI
import question_answer as qa
from typing import List, Tuple
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
from datetime import datetime
from tree_searcher import TreeSearcher
from get_tasks_dates import Assignment, Class
import uvicorn

app = FastAPI()

ts = TreeSearcher('storage/rule_spec.json', 'storage/expanded_rule_spec.json')


origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    
)

class AskArgument(BaseModel):
    question: str

class AskAnswer(BaseModel):
    heading: str
    url: str
    answer_text: str
    surrounding_context_text: List[str] # question text, answer text, question text continued.

class AskResponse(BaseModel):
    answers: List[AskAnswer]

class TreeGetArgument(BaseModel):
    node_id: str

class TreeNextArgument(BaseModel):
    question: str
    node_id: str

class NodeDisplay(BaseModel):
    prompt: str
    links: List[str]
    description: str

class TreeNextResponse(BaseModel):
    node_id: str
    display: NodeDisplay

class AssignResponse(BaseModel):
    assignments: List[Assignment]

class ClassResponse(BaseModel):
    classes: List[Class]


invalid_display = NodeDisplay.construct(
    prompt="We did not find what you were looking for...",
    links=[],
    description="The chatbot-ta isn't capable of answering that question at the time. Please try the search feature."
)

invalid_node = TreeNextResponse.construct(
    node_id="error",
    display=invalid_display
)



@app.on_event("startup")
async def setup():
    qa.qa_setup()


@app.get('/fetch_search/')
async def fetch_data():
    con = sqlite3.connect('./logging/query_logs.db')
    cur = con.cursor()
    results = cur.execute('''SELECT * FROM query_logs''')
    return [
        {'query': row[0], 'timestamp': row[1] }
        for row in results.fetchall()
        ]
@app.get('/fetch_chat/')
async def fetch_data():
    con = sqlite3.connect('./logging/chat_logs.db')
    cur = con.cursor()
    results = cur.execute('''SELECT * FROM chat_logs''')
    return [
        {'start_node': row[0], 'end_node': row[1], 'message': row[2], 'timestamp': row[3] }
        for row in results.fetchall()
        ]


@app.post('/ask/')
def ask_endpoint(argument : AskArgument) -> AskResponse:
    answers = qa.chatbot_response(argument.question.lower())
    print(answers)
    con = sqlite3.connect('./logging/query_logs.db')
    cur = con.cursor()
    cur.execute('''INSERT INTO query_logs VALUES(?, ?)''', (argument.question, datetime.now()))
    con.commit()
    return AskResponse.construct(answers=answers)
    
@app.post('/tree_get/')
def tree_get_endpoint(argument : TreeGetArgument) -> NodeDisplay:
    return ts.get_node(argument.node_id)
@app.post('/tree_next/')
def tree_next_endpoint(argument : TreeNextArgument) -> TreeNextResponse:
    time_now = datetime.now()
    tmp = ts.get_next_node(argument.question, argument.node_id)
    con = sqlite3.connect('./logging/chat_logs.db')
    cur = con.cursor()
    if tmp == {}:
        cur.execute('''INSERT INTO chat_logs VALUES(?,?,?,?)''', (str(argument.node_id), None, str(argument.question), time_now))
        print('executed with data: ' + str(argument.node_id) + " " + str(argument.question) + " " + str(time_now))
        return invalid_node
    else:
        cur.execute('''INSERT INTO chat_logs VALUES(?,?,?,?)''', (str(argument.node_id), tmp['node_id'], str(argument.question), time_now))
        print('executed with data: ' + str(argument.node_id) + " " + str(tmp['node_id']) + " " + str(argument.question) + " " + str(time_now))
    con.commit()
    return tmp
@app.post('/tree_assignments/')
def tree_assignments_endpoint(argument: AskArgument) -> AssignResponse:
    return AssignResponse(assignments=ts.get_assignments(argument.question))
@app.post('/tree_classes/')
def tree_classes_endpoint(argument: AskArgument) -> ClassResponse:
    return ClassResponse(classes=ts.get_classes(argument.question))

if __name__ == "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip = s.getsockname()[0]

    s.close()
    port = 8000

    print(f'Running on {ip}:{port}')
    uvicorn.run("api:app", host=ip, port=port)



