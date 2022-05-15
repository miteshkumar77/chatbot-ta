import json
import re
from numpy import array2string
from tqdm import tqdm
import io
from kwd import get_keywords, kwd_setup, get_closest_word_vector


def clean_characters(txt : str) -> str:
    """
        Remove all non ascii characters, then replace sequences of new line with just a single new line.
    """
    t1 = re.sub('\n+', '\n', txt)
    return re.sub('[^\x00-\x7F]+', '', t1)


def go(input_file : str, output_file : str, output_keyword_file : str):
    """
        Fix text formatting on scraper output. Add 'keyword' field of important keywords from the text.
        Output url -> {context, keywords} dictionary as json to output file.
        input_file: Input file name (unmodified)
        output_file: Output file name for cleaned input_file
        output_keyword_file: Output file for keyword to url mapping
    """
    kwd_setup()

    with open(input_file, 'r') as if_:
        in_str = if_.read()
        in_json = json.loads(in_str)
        out_json = {}
        out_kwd_json = {}
        for in_pg in tqdm(in_json):
            # remove extraneous characters in 'content' and 'lis' field, and then concatenate them with a single new line.
            # remove duplicate new line resulting from concatenation (if applicable).
            out_pg = dict()
            out_pg['content'] = re.sub('\n+', '\n', clean_characters(in_pg['content']) + '\n' + clean_characters(in_pg['lis']))

            # add 'keywords' field
            out_pg['keywords'] = list(set(get_keywords(out_pg['content']) + get_keywords(in_pg['url'].split('/')[-1])))

            # add new page entry to the output structure
            out_json[in_pg['url']] = out_pg

            for kwd in out_pg['keywords']:
                if kwd not in out_kwd_json:
                    out_kwd_json[kwd] = set()
                out_kwd_json[kwd].add(in_pg['url'])

        tmp = {k:list(v) for k,v in out_kwd_json.items()}
        out_kwd_json = {'vec2url' : {}, 'word2vec' : {}}
        for word, urls in tmp.items():
            if word in out_kwd_json['word2vec']:
                wv_str = out_kwd_json['word2vec'][word]
            else:
                try:
                    wv_str = str(get_closest_word_vector(word).tolist())
                except KeyError:
                    print("Skipped: " + word + " <--> " + re.sub('[^a-z]+', '', word.lower()))
                    continue
                out_kwd_json['word2vec'][word] = wv_str
            out_kwd_json['vec2url'][wv_str] = urls

        out_str = json.dumps(out_json)
        with open(output_file, 'w') as of_:
            of_.write(out_str)
        
        out_kwd_str = json.dumps(out_kwd_json)
        with open(output_keyword_file, 'w') as of_:
            of_.write(out_kwd_str)
        

    

if __name__ == '__main__':
    input = 'scraper_output.json'
    output = 'preprocessed-scraper_output.json'
    output_kwd = 'keyword-scraper_output.json'
    go(input, output, output_kwd)
