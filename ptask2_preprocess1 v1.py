# -*- coding: utf-8 -*-
"""
Created on Thu Nov 10 19:12:47 2022

@author: lenovo
"""

# -*- coding: utf-8 -*-
import pandas as pd
import re
import collections

from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import axes

" 设置一个开关P，控制是否打印输入，默认关闭打印 "
P =0
if P ==1:
    print('print message enabled')
else:
    print('print message disabled')


discfile = r'hair_dryer.tsv'
df = pd.read_csv(discfile, sep='\t',encoding = 'utf-8',dtype={'text':str})

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
if P ==1:
    print(corr)

'''4.评论信息处理'''

df['review_headline'] = df['review_headline'].str.lower()
df['review_body'] = df['review_body'].str.lower()
def tokens(text): 
    return re.findall('[a-z]+', text.lower()) 
with open(r'big.txt', 'r') as f:
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


#%%
"这里开始情感分析"
"""在停用词表中过滤否定词和程度副词"""
#生成stopword表，需要去除一些否定词和程度词汇
stopwords = set()
fr = open(r'python词典\stopwords.txt','r',encoding='utf-8')
for word in fr:
    stopwords.add(word.strip())#Python strip() 方法用于移除字符串头尾指定的字符（默认为空格或换行符）或字符序列。
    # #读取否定词文件
    not_word_file = open(r'python词典\合集.txt','r+',encoding='utf-8')
    not_word_list = not_word_file.readlines()
    not_word_list = [w.strip() for w in not_word_list]
    #生成新的停用词表
    with open(r'python词典\stopwords_new.txt','w',encoding='utf-8') as f:
        for word in stopwords:
            if word not in not_word_list:
                f.write(word+'\n')
stopwords_new=set()
fn=open(r'python词典\stopwords_new.txt','r',encoding='utf-8')
for word in fn:
    stopwords_new.add(word.strip())
df['review_body'] = df['review_body'].str.lower().str.split()
df['review_body'].apply(lambda x: [item for item in x if item not in stopwords_new])


"1、将同类词典合并并转化为字典格式（情感词典使用的是senticnet情感词典，但简化了一些，原版有14w个数据，不过这个词典应该可以直接安装在python中直接使用）"

#生成否定词字典，赋值-1
not_word_df = pd.read_csv(r'python词典\否定词.txt', sep=";", names=['vocabulary'])
not_word_df['value'] = -1
not_dict = dict(zip(not_word_df['vocabulary'],not_word_df['value']))

#生成程度副词字典（针对六种程度副词，分别赋权）
degree_word_df = pd.read_csv(r'python词典\程度副词.txt', sep=";", names=['vocabulary'])
degree_word_df['value']=2
degree_word_df['value'].iloc[66:92]=1.5;
degree_word_df['value'].iloc[92:115]=1;
degree_word_df['value'].iloc[115:131]=0.5;
degree_word_df['value'].iloc[131:143]=0.1;
new_degree_word_df=degree_word_df.drop(degree_word_df.index[[0,1,66,92,115,131,143]])
degree_dict=dict(zip(new_degree_word_df['vocabulary'],new_degree_word_df['value']))

#读取senticnet文件，导入数据
sen_df = pd.read_excel(r'python词典\senticnet_list.xlsx',header=0,usecols='A:B')
#由于这个情感词典里面针对每个情感词的分类过于细化，这里把每个词的其他释义删除，只保留原始得分
sen_df = sen_df[sen_df['CONCEPT'].str.contains('_')==False]
#这里由于不确定senticnet字典中是否会与另外两个字典重复，因此我们再筛一下，把重复的词语删掉
sen_df['CONCEPT'].apply(lambda x: [item for item in x if item not in new_degree_word_df and item not in not_word_df])
sen_dict = dict(zip(sen_df['CONCEPT'], sen_df['POLARITY INTENSITY']))


"2、针对已经拆分的评论中的各个词语分类，将其归类至三个新建的字典中，以备后续计算分值使用"
def classify_words(word_list):
  sen_word = dict()
  not_word = dict()
  degree_word = dict()
  for i in range(len(word_list)):
        word = word_list[i]
        if word in sen_dict.keys() and word not in not_dict.keys() and word not in degree_dict.keys():
            # 找出分词结果中在情感词字典中的词
            sen_word[i] = sen_dict[word]
        elif word in not_dict.keys() and word not in degree_dict.keys():
            # 分词结果中在否定词字典中的词
            not_word[i] = -1
        elif word in degree_dict.keys():
            # 分词结果中在程度副词字典中的词
            degree_word[i] = degree_dict[word]
  # 将分类结果返回
  
  if P ==1:
    print(sen_word,not_word,degree_word)
  return sen_word, not_word, degree_word

"3、由于一句话中可能会出现多个情感词，因此需要谨慎分辨修饰每个情感词的程度副词与否定词的位置。"
"以找出的情感词为主体，首先定义新的函数通过遍历找出第一个情感词前面的程度副词与否定词，并计算赋予该情感词分数的权重"
"针对后面的情感词，在初始化权重的基础上，运用与上述类似的方法对每个情感词的分值计算并相加"
#（1）判断第一个情感词之前是否存在程度副词和否定词，并计算权重
def get_init_weight(sen_word, not_word, degree_word):
    # 权重初始化为1
    W = 1
    # 将情感字典的key转为list
    sen_word_index_list = list(sen_word.keys())
    if len(sen_word_index_list) == 0:
        return W
    # 获取第一个情感词的下标，遍历从0到此位置之间的所有词，找出程度副词和否定词
    for i in range(0, sen_word_index_list[0]):
        if i in not_word.keys():
            W *= -1
        elif i in degree_word.keys():
            #更新权重，如果有程度副词，分值乘以程度副词的程度分值
            W *= float(degree_word[i])
    return W
#（2）计算评论分值
def score_sentiment(sen_word, not_word, degree_word, seg_result):
    W = get_init_weight(sen_word, not_word, degree_word)
    if P ==1:
        print(W)
    score = 0
    # 情感词下标初始化
    sentiment_index = -1
    # 情感词的位置下标集合
    sentiment_index_list = list(sen_word.keys())
    #print(sentiment_index_list)
    # 遍历分词结果(遍历分词结果是为了定位两个情感词之间的程度副词和否定词)
    for i in range(0, len(seg_result)):
        # 如果是情感词（根据下标是否在情感词分类结果中判断）
        if i in sen_word.keys():
            # 权重*情感词得分
            score += W * float(sen_word[i])
            if P ==1:
                print(score)
            # 情感词下标加1，获取下一个情感词的位置
            sentiment_index += 1
            if P ==1:
                print("sentiment_index:",sentiment_index)
            if sentiment_index < len(sentiment_index_list) - 1:  #总的情感词的个数
                # 判断当前的情感词与下一个情感词之间是否有程度副词或否定词
                W=1  #防止第二轮的权重出现累乘的情况
                for j in range(sentiment_index_list[sentiment_index], sentiment_index_list[sentiment_index + 1]):
                    # 更新权重，如果有否定词，取反
                    if j in not_word.keys():
                        W *= -1
                    elif j in degree_word.keys():
                        # 更新权重，如果有程度副词，分值乘以程度副词的程度分值
                        W *= float(degree_word[j])
                    if P ==1:
                        print(W)
                    """这里又出现了一个问题，就是后一个没有否定词和程度副词的权重会将前一个覆盖掉，所以初始化权重W=1不能放在for循环中"""
        # 定位到下一个情感词
        if sentiment_index < len(sentiment_index_list) - 1:
            i = sentiment_index_list[sentiment_index + 1]
    return score

"4、将df中所有的已处理的评论转为单独的word_list，计算其得分并输出"
# 同时生成评论得分(review_score)、评论字数统计(word_count)、评论帮助性得分(help_rating)
df['review_score']=0
df['word_count']=0
df['help_rating']=0
for s in range(len(df['review_body'])):
    review = list(df['review_body'].iloc[s])
    sen_word, not_word, degree_word = classify_words(review)
    score = score_sentiment(sen_word, not_word, degree_word, review)

    df.loc[s, 'review_score'] = score
    df.loc[s, 'word_count'] = len(review)
    if df['total_votes'].iloc[s] !=0:
        df.loc[s, 'help_rating'] = df['helpful_votes'].iloc[s]/df['total_votes'].iloc[s]

list_focus = ['star_rating','review_score','help_rating','word_count']
df1 = df.loc[:, list_focus]
df2 = df1[df1['help_rating']>0]

wt = pd.ExcelWriter('output_hair_dryer.xlsx')
df.to_excel(wt, sheet_name = 'df', index =False)
df1.to_excel(wt, sheet_name = 'df1', index =False)
df2.to_excel(wt, sheet_name = 'df2', index =False)
wt.save()
print('finish!')
pass