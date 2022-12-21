# -*- coding: utf-8 -*-
import pandas as pd
import re
import collections

discfile = r'C:\Users\17906\Desktop\hair_dryer.tsv\hair_dryer.tsv'
df = pd.read_csv(discfile, sep='\t')

#1.处理异常数据和缺失数据
#1.1处理异常数据：因该案例不属于一般的数理统计范畴，故选择star_rating、review_headline和review_body的一致程度作为判断指标）


#1.2处理缺失数据

df.info()
df = df.fillna('not filled in')
df.info()

#2.处理冗余数据与重复数据
#2.1处理冗余数据：marketplace

df = df.drop(['marketplace'],axis=1)

#2.2处理重复数据

df = df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)

#3.文本替换
#3.1 vine与verified_purchase

df['vine'] = df['vine'].replace(to_replace=['N', 'Y'], value=[0, 1])
df['verified_purchase'] = df['verified_purchase'].replace(to_replace=['N', 'Y'], value=[0, 1])

#####后面一直到#5（含）没排除异常数据，暂时不能跑
#3.2 customer_id

#3.3 review_id

#3.4 product_id

#3.5 product_parent

#3.6 product_title

#3.7 product_category



#4.除去无关变量后的相关性分析

df.drop(['review_headline','review_body','review_date',],axis=1).corr() 

#5.根据相关性分析进一步处理冗余数据:product_parent、product_category、review_id、product_title

df = df.drop(['product_parent','product_category','review_id','product_title'],axis=1)

#6.评论标题和内容处理

df['review_headline'] = df['review_headline'].str.lower()
df['review_body'] = df['review_body'].str.lower()

def tokens(text): 
    return re.findall('[a-z]+', text.lower()) 

with open(r'C:\Users\17906\Desktop\-word--master\-word--master\big.txt', 'r') as f:
    WORDS = tokens(f.read())
WORD_COUNTS = collections.Counter(WORDS)

def known(words):
    return {w for w in words if w in WORD_COUNTS}

def edits0(word): 

    return {word}

def edits1(word):
    alphabet = ''.join([chr(ord('a')+i) for i in range(26)])
    def splits(word):
        return [(word[:i], word[i:]) 
                for i in range(len(word)+1)]
                
    pairs      = splits(word)
    deletes    = [a+b[1:]           for (a, b) in pairs if b]
    transposes = [a+b[1]+b[0]+b[2:] for (a, b) in pairs if len(b) > 1]
    replaces   = [a+c+b[1:]         for (a, b) in pairs for c in alphabet if b]
    inserts    = [a+c+b             for (a, b) in pairs for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    return {e2 for e1 in edits1(word) for e2 in edits1(e1)}
    
    
def correct(word):
    candidates =  (known(edits0(word)) or
                   known(edits1(word)) or
                   known(edits2(word)) or
                   {word})

    return max(candidates, key=WORD_COUNTS.get)

def correct_match(match):
    word = match.group()
    def case_of(text):
        return (str.upper if text.isupper() else
                str.lower if text.islower() else
                str.title if text.istitle() else
                str)
    return case_of(word)(correct(word.lower()))
    
def correct_text_generic(text):
    return re.sub('[a-zA-Z]+', correct_match, text)

def clear(text):
    pattern1 = r'['u'\U0001F300-\U0001F64F'u'\U0001F680-\U0001F6FF'u'\u2600-\u2B55\U00010000-\U0010ffff]+'
    pattern2 =r'[^A-Za-z0-9 ]+'
    text = text.replace("<br />", " ")
    #text = text.replace(' ', "_")
    #text = text.replace("_", " ") 
    text1 = re.sub(pattern1,'',text)   
    text = re.sub(pattern2,'',text1)
    return text

df['review_headline'] = df['review_headline'].apply(clear)
df['review_body'] = df['review_body'].apply(clear)
  














