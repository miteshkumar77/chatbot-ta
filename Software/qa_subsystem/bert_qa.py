from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
# from transformers import RobertaTokenizer, RobertaForQuestionAnswering, pipeline
import transformers

tokenizer : transformers.BertTokenizerFast = None
model : transformers.BertForQuestionAnswering = None
qa_pipeline = None

"""
def bert_setup():
    global tokenizer
    global model
    global qa_pipeline
    if tokenizer is None:
        tokenizer = RobertaTokenizer.from_pretrained('deepset/roberta-base-squad2')
    if model is None:
        model = RobertaForQuestionAnswering.from_pretrained('deepset/roberta-base-squad2')
    
    if qa_pipeline is None:
        qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)
"""

def bert_setup():
    global tokenizer
    global model
    global qa_pipeline
    if tokenizer is None:
        tokenizer = AutoTokenizer.from_pretrained('deepset/bert-base-cased-squad2')
    if model is None:
        model = AutoModelForQuestionAnswering.from_pretrained('deepset/bert-base-cased-squad2')
    
    if qa_pipeline is None:
        qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)

def manual_answer_question(question : str, context : str) -> str:
    global tokenizer
    global model
    inputs = tokenizer(question, context, return_tensors='pt')
    outputs = model(**inputs)
    start_scores = outputs.start_logits
    end_scores = outputs.end_logits
    start_idx = int(start_scores[0].argmax())
    end_idx = int(end_scores[0, start_idx:].argmax()) + start_idx
    return tokenizer.convert_tokens_to_string(tokenizer.convert_ids_to_tokens(inputs['input_ids'][0][start_idx : end_idx + 1]))

def get_annotated_context(start, end, context):
    return [context[0:start], context[start:end+1], context[end+1:]]

def answer_question(question : str, context : str) -> str:
    d = 512
    s = 0
    score = -1.0
    answer = ''
    best_context = ''
    best_start = -1
    best_end = -1
    global qa_pipeline

    while s + 512 < len(context):
        tmp_ans = qa_pipeline(question=question, context=context[s : s + 512])
        if tmp_ans['score'] > score:
            best_context = context[s : s + 512]
            best_start = tmp_ans['start']
            best_end = tmp_ans['end']
            score = tmp_ans['score']
            answer = tmp_ans['answer']
        s += d
        print('[' + str(s) + ' | ' + str(len(context)) + ']')

    tmp_ans = qa_pipeline(question=question, context=context[s :])
    if tmp_ans['score'] > score:
        best_context = context[s : s + 512]
        best_start = tmp_ans['start']
        best_end = tmp_ans['end']
        score = tmp_ans['score']
        answer = tmp_ans['answer']

    return (answer, get_annotated_context(best_start, best_end, best_context))

if __name__ == '__main__':
    bert_setup()
    print(answer_question('What is Capstone?', 'welcome to Capstone, a class that provides an introductory experience to team based engineering and documentation.'))



