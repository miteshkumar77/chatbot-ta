#!/usr/bin/env python
# coding: utf-8

# In[20]:


import matplotlib.pyplot as plt  
import pandas as pd   
import seaborn as sns
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')

file_path = "./Capstone EDN information survey  (Responses).csv"
data = pd.read_csv(file_path)

sns.distplot(a=data["How convenient would it be to access the chatbot through Webex chat?"], bins = 10,kde= True, norm_hist=False)


# In[28]:


sns.countplot(data = data,x="How convenient would it be to access the chatbot through Webex chat?",color = None)


# In[30]:


sns.countplot(data = data,x="How convenient would it be to access it on a standalone webpage THAT REQUIRES BEING ON THE RPI VPN?",color = None)


# In[31]:


plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
sizes = [0,78]
labels = ['instructor','student']
plt.pie(sizes,labels=labels,autopct='%1.1f%%',shadow=100,startangle=180)


# In[61]:


ai = 0
at = 0
ad = 0
edn =0
pc = 0#project contact
sc = 0 #student contact
ca = 0#class agenda
h = 0#subversion help
af = 0#avaliable
pg = 0
ws = 0
oth = 0
for answers in data["STUDENTS: what have you had trouble finding, or would appreciate faster access to, on the EDN wiki so far? INSTRUCTORS: what are your most common questions from students about? (Select all that apply.)"]:
    b = answers.split(',')
    for elements in b:
        if "Assignment instructions (Statement of Work" in elements:
            ai += 1
        elif "Class agendas&out-of-class activities" in elements:
            ca += 1
        elif "Assignment templates & rubrics" in elements:
            at += 1
        elif "Assignment due dates/deadlines" in elements:
            ad += 1 
        elif "EDN usage/FAQs (what goes where on EDN forum/repository" in elements:
            edn += 1 
        elif "Subversion help" in elements:
            h += 1 
        elif "Project/Chief Engineer & other facility contact infomation" in elements:
            pc += 1 
        elif "Student/team member contact information" in elements:
            sc += 1 
        elif "Available fabrication facilities and guidelines" in elements:
            af += 1 
        elif "Purchasing guidelines" in elements:
            pg += 1 
        elif "Working with sponsors" in elements:
            ws += 1 
        elif "Everything" in elements:
            ai +=1 
            ca +=1
            at+=1
            ad+=1
            edn+=1
            h+=1
            pc+=1
            sc+=1
            af+=1
            pg+=1
            ws+=1
       
print(ai)
print(at)
print(ad)
print(edn)
print(pc)
print(sc)
print(ca)
print(h)
print(af)
print(pg)
print(ws)
print(oth)


# In[56]:


elements = "Assignment templates & rubrics"
if "Assignment templates & rubrics" == elements:
    print("1")


# In[64]:


file_path1 = "./survey.csv"
data1 = pd.read_csv(file_path1)
sns.countplot(data = data1,x="STUDENTS: what have you had trouble finding, or would appreciate faster access to, on the EDN wiki so far? INSTRUCTORS: what are your most common questions from students about? (Select all that apply.)",color = None)


# In[ ]:




