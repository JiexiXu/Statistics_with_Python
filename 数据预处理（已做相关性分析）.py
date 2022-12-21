# -*- coding: utf-8 -*-
import pandas as pd
import re
import collections

discfile = r'C:\Users\17906\Desktop\hair_dryer.tsv\hair_dryer.tsv'
df = pd.read_csv(discfile, sep='\t')

'''1.数据筛选'''

'''
无关变量：
marketplace——市场所在地均为us，无用
product_parent和product_category——product_parent指产品所属大类的序号，product_category就是 “生活用品”、“家电”等，无用
review_id——无用
product_id——由于与product_titile一一对应,且并不会应用于叙述性分析中，重复
'''

df.info()
df = df.fillna('not filled in')
df = df.drop(['marketplace','review_id','product_id','product_category','product_parent'],axis=1)
df = df.drop_duplicates(subset=None, keep='first', inplace=False, ignore_index=False)

'''2.文本逻辑值替换'''

df['vine'] = df['vine'].replace(to_replace=['N', 'Y'], value=[0, 1])
df['verified_purchase'] = df['verified_purchase'].replace(to_replace=['N', 'Y'], value=[0, 1])

'''3.相关性分析'''

corr = df.drop(['review_headline','review_body','review_date',],axis=1).corr() 
print(corr)

'''4.评论信息处理'''

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
  














