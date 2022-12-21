import pandas as pd
import numpy as np
import math

def nml(series):  # 正向指标归一化
    l = []
    for i in series:
        l.append((i - series.min()) / (series.max() - series.min()))
    return pd.Series(l, name=series.name)

def nml_max(series): #负向指标归一化
    l = []
    for i in series:
        l.append((series.max() - i) / (series.max() - series.min()))
    return pd.Series(l, name=series.name)

#归一化函数，对正负向指标分别调用nml()和nml_max(),其中useless_votes为负向指标，其余五个指标均为正向指标
def nmlzt(df):
    dfn = pd.DataFrame()
    for i in df.columns:
        if (i=='useless_votes'):
            dfn = pd.concat([dfn, nml_max(df[i])], axis=1)  #负向
        else:
            dfn = pd.concat([dfn, nml(df[i])], axis=1)     #正向
    # dfn为归一化的数据
    return dfn

def pij(df):  #求信息熵公式中的p，这里直接用取值除以取值总和，而不是数量的比例
    D = df.copy()
    for i in range(D.shape[1]):  # 列
        sum = D.iloc[:, i].sum()
        for j in range(D.shape[0]):  # 行
            D.iloc[j, i] = D.iloc[j, i] / sum
            # 算pij
    return D


def entropy(series):	#计算信息熵
    _len = len(series)

    def ln(x):
        if x > 0:
            return math.log(x)
        else:
            return 0

    s = 0
    for i in series:
        s += i * ln(i)
    return -(1 / ln(_len)) * s


def _result(dfij):	#求e、d、w并返回
    dfn = dfij.copy()
    w = pd.DataFrame(index=dfn.columns, dtype='float64')
    l = []
    for i in dfn.columns:
        l.append(entropy(dfn[i]))
    w['熵'] = l
    w['差异性系数'] = 1 - np.array(l)
    sum = w['差异性系数'].sum()
    l = []
    for i in w['差异性系数']:
        l.append(i / sum)
    w['权重'] = l
    return w


#读取你需要计算的文件
df = pd.read_csv(r'C:\Users\limuyao\Desktop\带评分的数据.csv',encoding='gbk')
#选取需要计算的属性列
df=df[['star_rating','useless_votes','review_score']]
dfn = nmlzt(df) #归一化
dfij = pij(dfn) #求p
w = _result(dfij)	#求权重
print(w)#输出权重

#输出标准化结果到excel
dfn = dfn.set_index(df.index, drop=True)
resultPath = 'C:/Users/limuyao/Desktop/标准化及评分.xlsx'
dfn.to_excel(resultPath,sheet_name = "标准化",index = False,na_rep = 0,inf_rep = 0)

#print(dfn)
#计算得分
