#!/usr/bin/env python
# coding: utf-8

# ### Importing Libraries

# In[1]:


get_ipython().system('pip install bs4')
get_ipython().system('pip install requests')
get_ipython().system('pip install html5lib')
import bs4
import requests
from bs4 import BeautifulSoup
import pandas as pd
import webbrowser
import  os
import nltk
get_ipython().system('pip install urllib')
import urllib.request
import re


# ### Reading The Data Files

# In[2]:


df=pd.read_excel("D:\Ishty Folder\Projects Python\Assignment\cik_list.xlsx")
data=df


# In[19]:


Master_Dict=pd.read_excel("D:\Ishty Folder\Projects Python\Assignment\Master_Dict.xlsx")
Constrain_D=pd.read_excel("D:\Ishty Folder\Projects Python\Assignment\constraining_dictionary.xlsx")
Unconstrain_D=pd.read_excel("D:\\Ishty Folder\\Projects Python\\Assignment\\uncertainty_dictionary.xlsx")


# In[20]:


files = [file for file in os.listdir("D:\Ishty Folder\Projects Python\Assignment\stopwords")]
file1=open("D:\Ishty Folder\Projects Python\Assignment\\new_file.txt",'w')

for file in files:
    SW = open("D:\Ishty Folder\Projects Python\Assignment\stopwords\\" + file)
    SW_read=SW.read()
    file1.write(SW_read.upper())
    
file1.close()
file2=open("D:\Ishty Folder\Projects Python\Assignment\\new_file.txt" , "r")

stopword=file2.read()


# ### Extracting the url

# In[3]:


def url_define(k):

        url='https://www.sec.gov/Archives/'+data['SECFNAME'][k]
        
        return(url)
url_list=[]
for i in data.index:
    url=url_define(i)
    url_list.append(url)


# ### Extracting and Cleaning of Data From Website

# In[13]:


nltk.download('words')
words = set(nltk.corpus.words.words())
from urllib.request import urlopen, Request
finalp=[]

def clean_text(i):
    final_list=[]
    new_line_list=[]
    list1=[]
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
    reg_url = i
    req = Request(url=reg_url, headers=headers) 
    html = urlopen(req).read()
    decoded_line = html.decode("utf-8")
    cleaning = re.compile('<.*?>')
    cleantext = re.sub(cleaning, '', decoded_line)
    new_line=re.sub(('[^A-Z a-z.]')," ",cleantext)        
    new_line_list.append(new_line)    
    
    final=" ".join(w for w in nltk.wordpunct_tokenize(new_line)               if w.lower() in words )
    final_list.append(final)
        
    complete=re.sub(r'\n\s*\n','\n',final,re.MULTILINE)
    list1.append(complete)
    newlist = (item.strip() if hasattr(item, 'strip') else item for item in list1)
    
    list5=[item for item in newlist if item != '']
    finalp.append(list5)
    return(list5)


# ### Cleaning From Stopwords and Variable 8: Word Count

# In[21]:


def stopword_clean1(cleaned_list1):
    new=[]
    single_occurance_word_list=[]
    
    temp= cleaned_list1.upper().split()
    val=[new.append(j) for j in temp if not j in stopword] 
        
    for k in new:
        if k not in single_occurance_word_list:
            single_occurance_word_list.append(k)
                
    word_count=len(new)
    return(single_occurance_word_list, word_count) 


# ### Defining Functions for Variables

# ### Variable 1, 2 and 3 : Positive Score, Negative Score and Polarity Score

# In[9]:


def Variable_1_2_3(single_occurance_word_list):
   
    Final_Master_Dict=pd.concat([Master_Dict[Master_Dict['Negative']!=0] , Master_Dict[Master_Dict['Positive']!=0]],axis=0)[['Word','Positive','Negative']]
    PS=0
    NS=0
    
    for i in range(0,len(single_occurance_word_list)):
        for j in Final_Master_Dict.index:
            if single_occurance_word_list[i].upper()==Final_Master_Dict['Word'][j]:
                
                if Final_Master_Dict['Positive'][j]!=0:
                    PS=PS+1
                else:
                    NS=NS-1
                    
    Polarity_Score= (PS-NS*(-1))/((PS + NS*(-1))+0.000001)

    return (PS,NS*(-1),Polarity_Score)     


# ### Variable 4, 5, 6 and 7: Average Sentence Length, Percentage of complex words, Fog Index and Complex Word Count

# In[55]:


from pyphen import Pyphen
def variable_4_5_6_7(clean_text_list):
    Avg_sentence_length=[]
    complex_words_percent=[]
    FogIndex=[]
    decoded=[]
    Complex_Words_Count_list=[]
    for i in data.index:
        for cleaned_list1 in clean_text_list[i]:
            url='https://www.sec.gov/Archives/'+data['SECFNAME'][i]
            Complex_Words_Count=0
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}
            reg_url = url
            req = Request(url=reg_url, headers=headers) 
            html = urlopen(req).read()
            decoded_line = html.decode("utf-8")
            new_line=re.sub(('[^A-Z a-z.]')," ",decoded_line)
            decoded.append(new_line)
            CWC=0
                    
            for l in decoded:
                val=l.split()
        
                for o in val:
                    p = Pyphen(lang='en_US')
                    
            
                    for lo in range(0,len((p.positions(o)))):
                        
                    
                        if len(p.positions(o)) > 2:
                    
                            CWC=CWC+1
        print(i)
            
           
                            
        ASL=len(val)/len(cleaned_list1)
        CWP=(CWC)/(len(val))   
        FI = 0.4 * (ASL + CWP)
        Avg_sentence_length.append(ASL)
        complex_words_percent.append(CWP)
        FogIndex.append(FI)
        Complex_Words_Count_list.append(CWC)
        
        
    
    return(Avg_sentence_length,complex_words_percent, FogIndex, Complex_Words_Count_list)
    


# ### Variable 9 and 10: Uncertainty and Constraining

# In[ ]:


def variable_9_10(single_occurance_word_list):
    
    Constraining=0
    Uncertainty=0

    for i in range(0,len(single_occurance_word_list)):
        for j in Constrain_D.index:
            if single_occurance_word_list[i].upper()==Constrain_D['Word'][j]:
                Constraining=Constraining+1
                
        for k in Unconstrain_D.index:
            if single_occurance_word_list[i].upper()==Unconstrain_D['Word'][k]:
                Uncertainty=Uncertainty+1
                
    return(Uncertainty,Constraining )


# ### Variable 11,12,13 and 14: Positive word proportion, Negative word proportion, Uncertainty word proportion and Constraining word proportion

# In[ ]:


def variable_11_12_13_4(PS,NS,Uncertainty,Constraining,word_count):

    PWP=PS/word_count
    NWP=NS/word_count
    UWP=Uncertainty/word_count
    CWP=Constraining/word_count
    
    return (PWP,NWP,UWP,CWP)


# ### Varible 15: Constraining words for whole report

# In[69]:


def variable_15(cleaned_list1):
    CWP=0
    
    for i in cleaned_list1.split():
        for s in Constrain_D.index:
            if i.upper()==Constrain_D['Word'][s]:
                CWP=CWP+1  
                
    return(CWP)

