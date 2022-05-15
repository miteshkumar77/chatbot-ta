import bert_qa as qa
import searcher as s
from multiprocessing import Process, Manager

iidx : s.InvertedIndex = None
question_answerer = None

def qa_setup():
    qa.bert_setup()
    global iidx
    if iidx is None:
        iidx = s.InvertedIndex('./storage/content.db', './storage/keyword_index')

def chatbot_response(question : str):
    relevant_docs = iidx.retrieve_relevant_documents(question, topn=5, k=20)
    def helper(url, context, question, idx, ret_list):
        answer, context_hl = qa.answer_question(question, context)
        tmp = {'heading': url.split('/')[-1],
                'url': url,
                'answer_text': answer,
                'surrounding_context_text': context_hl}
        print(f'Finishing: {idx}, {tmp}')
        ret_list[idx] = tmp
    
    mgr = Manager()
    jobs = []
    ret_list = mgr.list([None for _ in relevant_docs])
    for url, content in relevant_docs:
        p = Process(target=helper, args=(url, content, question, len(jobs), ret_list))
        jobs.append(p)
        p.start()
    
    for p in jobs:
        p.join()

    return list(ret_list)

    # return [
    #     helper(url, content)
    #     for url, content in relevant_docs
    # ]



if __name__ == '__main__':
    qa_setup()
    print(chatbot_response('Where can I find a CPU or microcontroller?'))