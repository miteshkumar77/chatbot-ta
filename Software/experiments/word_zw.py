#!/usr/bin/env python
# coding: utf-8

# In[1]:


pip install nltk


# In[1]:


import nltk


# In[2]:


import nltk
nltk.download()


# In[3]:


from nltk.corpus import brown
print(brown.categories())
print(len(brown.sents()))
print(len(brown.words()))


# In[4]:


###frequency
import nltk
tokens = ['I','have','a','question','about','capstone',"what","is","capstone","where","can","I","get","information",
         "about","this","course"]

#calculate the frequency
freq = nltk.FreqDist(tokens)

for key,val in freq.items():
    print(str(key) + ";" + str(val))
    
#get the most 5 common words
standard_freq = freq.most_common(5)
print(standard_freq)

freq.plot(20, cumulative = False)


# In[6]:


#remove stopwords
from nltk.corpus import stopwords
tokens = ['I','have','a','question','about','capstone',"what","is","capstone","where","can","I","get","information",
         "about","this","course"]

clean_tokens = tokens[:]
stwords = stopwords.words('english')
for token in tokens:
    if token in stwords:
        clean_tokens.remove(token)
        
print(clean_tokens)


# eliminate the words such as "have", "a"

# In[7]:


#tokenize
from nltk.tokenize import sent_tokenize
mytext = "I have a question about capstone. What is capstone? Where can I get information about this course?"
print(sent_tokenize(mytext))


# In[8]:


#saparate words
from nltk.tokenize import word_tokenize
mytext = "I have a question about capstone. What is capstone? Where can I get information about this course?"
print(word_tokenize(mytext))


# In[12]:


#stemming
from nltk.stem import PorterStemmer
porter_stemmer = PorterStemmer()
print(porter_stemmer.stem("writing"))


# In[13]:


#Lemmatization
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize("increases"))


# In[17]:


from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
print(lemmatizer.lemmatize('playing', pos="v"))
print(lemmatizer.lemmatize('playing', pos="n"))
print(lemmatizer.lemmatize('playing', pos="a"))
print(lemmatizer.lemmatize('playing', pos="r"))


# In[19]:


import nltk
text = nltk.word_tokenize("what is the capstone?")
print(text)
print(nltk.pos_tag(text))


# ADJ = adjective
# ADV = adverb
# CNJ = conjunction
# DET = determiner
# EX = existential
# FW = foreign word
# MOD = modal verb
# N = noun
# NP = proper noun
# NUM = number
# PRO = pronoun
# P = preposition
# UH = interjection
# V = verb
# VD = past tense
# VG = present participle
# VN = past participle
# WH = wh determiner

# In[20]:


#get the definition
from nltk.corpus import wordnet
syn = wordnet.synsets("capstone")
print(syn[0].definition())
print(syn[0].examples())


# In[22]:


#get the synonyms
from nltk.corpus import wordnet
synonyms = []
for syn in wordnet.synsets('Capstone'):
    for lemma in syn.lemmas():
        synonyms.append(lemma.name())
print(synonyms)


# In[26]:


#get the antonym
from nltk.corpus import wordnet
antonyms = []
for syn in wordnet.synsets("big"):
    for l in syn.lemmas():
        if l.antonyms():
            antonyms.append(l.antonyms()[0].name())
print(antonyms)


# to get information from one sentense, there are four steps: tokenize, tag, name entity recognition, relation recognition
# 

# In[27]:


#compare two words
from nltk.corpus import wordnet
w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('boat.n.01')
print(w1.wup_similarity(w2))

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('car.n.01')
print(w1.wup_similarity(w2))

w1 = wordnet.synset('ship.n.01')
w2 = wordnet.synset('cat.n.01')
print(w1.wup_similarity(w2))


# In[28]:


pip install gensim


# In[6]:


from gensim import corpora
documents = ["Human machine interface for lab abc computer applications",
          "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
#遍历documents，将其每个元素的words置为小写，然后通过空格分词，并过滤掉在stoplist中的word。
texts = [[word for word in document.lower().split() if word not in stoplist]
for document in documents]
# remove words that appear only once，collection是python的一个工具库
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] > 1]
               for text in texts]

from pprint import pprint  # pprint可以使输出更易观看。
pprint(texts)
#输出结果：
[['human', 'interface', 'computer'],
 ['survey', 'user', 'computer', 'system', 'response', 'time'],
 ['eps', 'user', 'interface', 'system'],
 ['system', 'human', 'system', 'eps'],
 ['user', 'response', 'time'],
 ['trees'],
 ['graph', 'trees'],
 ['graph', 'minors', 'trees'],
 ['graph', 'minors', 'survey']]

#定义一个词典，里面包含所有语料库中的单词，这里假设上文中输出的texts就是经过处理后的语料库。
dictionary = corpora.Dictionary(texts)
dictionary.save('./desktop/train/deerwester.dict')  # 因为实际运用中该词典非常大，所以将训练的词典保存起来，方便将来使用。
print(dictionary) # 输出：Dictionary(35 unique tokens: ['abc', 'applications', 'computer', 'human', 'interface']...)
# dictionary有35个不重复的词，给每个词赋予一个id
print(dictionary.token2id)#输出：{'abc': 0, 'applications': 1, 'computer': 2, 'human': 3, 'interface': 4, 'lab': 5, 'machine': 6, 'opinion': 7, 'response': 8, 'survey': 9, 'system': 10, 'time': 11, 'user': 12, 'eps': 13, 'management': 14, 'engineering': 15, 'testing': 16, 'error': 17, 'measurement': 18, 'perceived': 19, 'relation': 20, 'binary': 21, 'generation': 22, 'random': 23, 'trees': 24, 'unordered': 25, 'graph': 26, 'intersection': 27, 'paths': 28, 'iv': 29, 'minors': 30, 'ordering': 31, 'quasi': 32, 'well': 33, 'widths': 34}

new_doc = "Human computer interaction"
#用dictionary的doc2bow方法将文本向量化
new_vec = dictionary.doc2bow(new_doc.lower().split())
corpora.MmCorpus.serialize('./desktop/train/deerwester.mm',new_vec)  # 讲训练结果存储到硬盘中，方便将来使用。
print(new_vec)#输出[(2, 1), (3, 1)]

#获取语料
class MyCorpus(object):
    def __iter__(self):
        for line in open('mycorpus.txt'):
            #每一个line代表语料库中的一个文档
            yield dictionary.doc2bow(line.lower().split())
corpus_memory_friendly = MyCorpus()# 没有将corpus加载到内存中
print(corpus_memory_friendly)#输出：<__main__.MyCorpus object at 0x10d5690>

#遍历每个文档
for vector in corpus_memory_friendly:  # load one vector into memory at a time
    print(vector)


# iteritems用来遍历对象中的每个item
from six import iteritems
#初步构建所有单词的词典
dictionary = corpora.Dictionary(line.lower().split() for line in open('mycorpus.txt') )
#去出停用词,stop_ids表示停用词在dictionary中的id
stop_ids = [dictionary.token2id[stopword] for stopword in stoplist if stopword in dictionary.token2id]
#只出现一次的单词id
once_ids = [tokenid for tokenid, docfreq in iteritem(dictionary.dfs) if docfreq ==1]
#根据stop_ids与once_ids清洗dictionary
dictionary.filter_token(stop_ids + once_ids)
# 去除清洗后的空位
dictionary.compactify()
print(dictionary)#输出:Dictionary(12 unique tokens)

#假设训练结果为下面的corpus
corpus = [[(1, 0.5)], []]  # make one document empty, for the heck of it
#存储
corpora.MmCorpus.serialize('./gensim_out/corpus.mm', corpus)
#加载
corpus = corpora.MmCorpus('./gensim_out/corpus.mm')
print(corpus)#输出：MmCorpus(2 documents, 2 features, 1 non-zero entries)
#查看加载后的结果有两种方法：1.转成list2.遍历corpus，这种方法堆内存更加友好。
print(list(corpus))  # calling list() will convert any sequence to a plain Python list
#输出：[[(1, 0.5)], []]

for doc in corpus:
    print(doc)
#输出：[(1, 0.5)][]


# incomplete

# In[9]:


from gensim import corpora
text_corpus = ["Human machine interface for lab abc computer applications",
          "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
             "Graph minors A survey"]

document = "Human machine interface for lab abc computer applications"
stop_list = set("for a of the and to in".split(" "))
#print(stop_list)

texts = [[word for word in document.lower().split() if word not in stop_list]for document in text_corpus]
#print(texts)

#frequency
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] +=1
#print(frequency)

processed_corpus = [[token for token in text if frequency[token]>1]for text in texts]
print(processed_corpus)


# In[14]:


from gensim import corpora
text_corpus = ["What is Capstone",
          "Where can I get information about Capstone",
              "What will we learn from this course",
              "Where is this course's information"]

document = "Capstone is an Engineering course, you can find the course's information from the wiki page"
stop_list = set("for a of the and to in".split(" "))
#print(stop_list)

texts = [[word for word in document.lower().split() if word not in stop_list]for document in text_corpus]
#print(texts)

#frequency
from collections import defaultdict
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] +=1
#print(frequency)

processed_corpus = [[token for token in text if frequency[token]>1]for text in texts]
print(processed_corpus)


# In[ ]:




