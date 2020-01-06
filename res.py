# run chcp 65001 then run python res.py
# spacy installation - "pip install spacy" and to download data and models in english - "python -m spacy download en_core_web_sm" !!! 
#nlp = spacy.load('en_core_web_sm')
import os
java_path = "C:/Program Files/Java/jdk1.8.0_181/bin/java.exe"
os.environ['JAVAHOME'] = java_path
from nltk.tag import StanfordNERTagger
from nltk.tokenize import word_tokenize
import nltk 
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
 
import re

import csv
import pandas as pd
import numpy as np
#import matplotlib.pyplot as plt
#import seaborn as sns

from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
import os

import mysql.connector
import pymysql
import spacy
nlp = spacy.load('en_core_web_sm')



stop_words = set(stopwords.words('english'))

path = str(os.path.dirname(os.path.abspath(__file__)))

st1 = StanfordNERTagger('C:/Users/dmutta/Desktop/resume_to_jd/english.all.3class.distsim.crf.ser.zip',
					   'C:/Users/dmutta/Desktop/resume_to_jd/stanford-ner-2018-10-16/stanford-ner-2018-10-16/stanford-ner.jar',
					   encoding='utf-8')

#MariaDB Connection

mydb = mysql.connector.connect(
	user="mchirukuri",
	passwd="Dochub@2k19",
	host="192.168.1.131",
	database="documenthub"
)
#print("Connection Done")

mycursor = mydb.cursor()
mycursor.execute("SHOW DATABASES")
 
#print("Databases:")
for x in mycursor:
    print(x)
#print("*************")	

mycursor.execute("SHOW TABLES")
#print("Tables:")
for x in mycursor:
    print(x)
#print("*************")	

a=[]
b=[]
c=[]
d=[]
e=[]
f=[]
mycursor.execute("SELECT * FROM mjd")
myresult = mycursor.fetchall()
for x in myresult:
    a.append(x[0])
    b.append(x[1])
    c.append(x[2])
    d.append(x[3])
    e.append(x[4])
    f.append(x[5])
    df = pd.DataFrame({'JobTitle': a,'JobDescription': b,'Team':c,'Location':e,'Experience':f})
    sk=list(df.Team)
    df.set_index("Team", inplace=True)	

#location = "Miracle City IND"

def convert(fname, pages=None):
    if not pages:
        pagenums = set()
    else:
        pagenums = set(pages)
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    infile = open(fname, 'rb')
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close

    return text

def convert1(data,exp, location, pages=None):


    list1 = []
    tokenized = sent_tokenize(data) 
    for i in tokenized: 
      
    # Word tokenizers is used to find the words  
    # and punctuation in a string 
        wordsList1 = nltk.word_tokenize(i) 
  
    # removing stop words from wordList 
        wordsList = [w for w in wordsList1 if not w in stop_words]  
  
    #  Using a Tagger. Which is part-of-speech  
    # tagger or POS-tagger.  
        tagged = nltk.pos_tag(wordsList) 
  
       
        nn = [word for word,pos in tagged if pos == 'NNP']

        for st in nn:
            list1.append(st)
        nn = [j.strip() for j in list1]
		
        data = pd.read_csv("C:/Users/dmutta/Desktop/RTJ/skills.csv",delimiter='\t')
        
        team_list=[]
        for i in range(0,len(nn)):
            team=data.loc[data['Skills'].str.contains(nn[i]), ['Team']]
            team=team.values.tolist()
            team_list.append(team)
        flat_list = [item for sublist in team_list for item in sublist]
        flat = [item for sublist in flat_list for item in sublist]
        di1= {}
        for i in range(0,len(flat)):
            d4=flat.count(flat[i])
            di1.update({flat[i] : d4})
        li = sorted(di1.items(), key=lambda x: x[1], reverse=True)

        dd=dict(li[0:2])
        k=[]
        for key, value in dd.items() :
            k.append(key)  #top most related job titles
			
#checking related job title positions
    #jd=[]
    ej = set()			
    lst = [value for value in sk if value in k]
    ej1=[]
    ej2=[]
    frame = pd.DataFrame([])
    for i in range(0,len(lst)):
        
        ep=df.loc[[lst[i]], ['Experience']]
        d=ep.values.tolist()
        jt=df.loc[[lst[i]], ['JobTitle']]
        dt=jt.values.tolist()
       
#checking experience
        flat_list1 = [item for sublist in d for item in sublist]
        for y in range(0,len(flat_list1)):
            a1=str(flat_list1[y]).split("-")
        
            if (float(exp)>=float(a1[0]) and float(exp)<=float(a1[1])) :
                ej1.append(str(a1[0]+'-'+a1[1]))
                ej2.append(lst[i])
                ej=set(ej1)
                ee=set(ej2)

    lee = list(ee)
    lej = list(ej)
    location = [location]
    if len(ej) != 0:
        fin = df[df.Experience.isin(lej)]
        loc_v = fin[fin.Location.isin(location)]
        team_loc = loc_v[loc_v.index.isin(lee)]
        jd = team_loc.reset_index()
        
        if jd.empty:
            
            return "No related Job Description found"
        else:
            return jd
    else:
        
        return "No related Job Description found"

	
def file_tokenize(data):

    tokens = word_tokenize(data)
    punctuations = ['(',')',';',':','[',']',',','.','&','/']
    stop_words = stopwords.words('english')
    filtered = [w for w in tokens if not w in stop_words and not w in punctuations]
    return filtered
	
def fetch_name(data):
    name = str(file_tokenize(data)[0])
    return name
    
def fetch_email(data):
    email = ""
    match_mail = re.search(r'[\w\.-]+@[\w\.-]+', data)
    if(match_mail != None):
        email = match_mail.group(0)
    return email

def fetch_contact(data):
    mobile = ""
    match_mobile = re.search\
        (r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',data)
    if(match_mobile != None):
        mobile = match_mobile.group(0)
    return mobile

def fetch_degree(lst):

    with open(os.path.dirname(os.path.abspath(__file__)) + '\degree', 'rt') as fp:
        de = ''
        degree = fp.read().lower().split('\n')
        degree_lst = []
        for deg in degree:
            if deg in lst:
                if lst[lst.index(deg)+1] in ['arts','engineering','science','education','economics','technology',
                                             'information','criminal','music','degree']:
                    degree_lst.append(deg +' of '+lst[lst.index(deg)+1])
                    de = ', '.join(degree_lst)
    return de

