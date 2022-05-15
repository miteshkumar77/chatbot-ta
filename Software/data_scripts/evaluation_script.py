from transformers import AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import transformers

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


def get_metrics(eval_set):
    """
    tokenizer = AutoTokenizer.from_pretrained('deepset/bert-base-cased-squad2')
    model = AutoModelForQuestionAnswering.from_pretrained('deepset/bert-base-cased-squad2')
    qa_pipeline = pipeline('question-answering', model=model, tokenizer=tokenizer)
    return qa_pipeline(eval_set)
    """

    eval_set = eval_set["validation"]
