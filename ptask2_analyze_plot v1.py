# -*- coding: utf-8 -*-
"""
Created on Thu Nov 18 19:12:47 2022

@author: xujx
"""

# -*- coding: utf-8 -*-
import pandas as pd
import re
import collections

from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib import axes

'''
1 分别从三个xlsx文件中读出已经处理的3个产品的数据集

'''
'''1.1读出已经处理的hair dryer的数据'''
discfile = r'output_hair_dryer.xlsx'
hair_df = pd.read_excel(discfile, sheet_name = 'df')
hair_df1 = pd.read_excel(discfile, sheet_name = 'df1')
hair_df2 = pd.read_excel(discfile, sheet_name = 'df2')

'''1.2读出已经处理的microwave的数据'''
discfile = r'output_microwave.xlsx'
microwave_df = pd.read_excel(discfile, sheet_name = 'df')
microwave_df1 = pd.read_excel(discfile, sheet_name = 'df1')
microwave_df2 = pd.read_excel(discfile, sheet_name = 'df2')

'''1.3读出已经处理的pacifier的数据'''
discfile = r'output_pacifier.xlsx'
pacifier_df = pd.read_excel(discfile, sheet_name = 'df')
pacifier_df1 = pd.read_excel(discfile, sheet_name = 'df1')
pacifier_df2 = pd.read_excel(discfile, sheet_name = 'df2')

'''
2. 数据统统计信息概览 - 显示数据框中数字统计描述摘要信息（使用describe方法）
'''
"2.1 Hair_Dryer "
hair_desc  = hair_df.describe()  # 完整数据摘要统计描述
hair_desc1 = hair_df1.describe() # 部分数据摘要统计描述，仅含list_focus列表中的几项
hair_desc2 = hair_df2.describe() # 部分数据摘要统计描述，排除total_votes为0的数据
# 打印显示(主要关注第1个，整体数据信息概览)，仅打印显示
print(hair_desc)
print(hair_desc1) # 可忽略
print(hair_desc2) # 可忽略

"2.2 microwave "
microwave_desc  = microwave_df.describe()  # 完整数据摘要统计描述
microwave_desc1 = microwave_df1.describe() # 部分数据摘要统计描述，仅含list_focus列表中的几项
microwave_desc2 = microwave_df2.describe() # 部分数据摘要统计描述，排除total_votes为0的数据
# 打印显示(主要关注第1个，整体数据信息概览)，仅打印显示
print(microwave_desc)
print(microwave_desc1) # 可忽略
print(microwave_desc2) # 可忽略

"2.3 pacifier "
pacifier_desc  = pacifier_df.describe()  # 完整数据摘要统计描述
pacifier_desc1 = pacifier_df1.describe() # 部分数据摘要统计描述，仅含list_focus列表中的几项
pacifier_desc2 = pacifier_df2.describe() # 部分数据摘要统计描述，排除total_votes为0的数据
# 打印显示(主要关注第1个，整体数据信息概览)，仅打印显示
print(pacifier_desc)
print(pacifier_desc1) # 可忽略
print(microwave_desc2) # 可忽略

'''
3.2 描述性分析 
- 计算关键指标统计信息，并可视化
- 统计star rating的总数、平均值和方差。还计算了helpful votes的平均值和评论中的单词数量和平均值
'''
"3.2.1 产生Hair_Dryer统计信息列表"
total = hair_df['star_rating'].count()
star_rating_avg = hair_df['star_rating'].mean()
star_rating_var = hair_df['star_rating'].var()

helpful_votes_avg = hair_df['helpful_votes'].mean()

word_count_sum = hair_df['word_count'].sum()
word_count_avg = hair_df['word_count'].mean()
#列表表示Hair_Dryer的统计数据
Hair_Dryer = [total, star_rating_avg, helpful_votes_avg, star_rating_var, word_count_sum, word_count_avg]

"3.2.2 产生microwave统计信息列表"
total = microwave_df['star_rating'].count()
star_rating_avg = microwave_df['star_rating'].mean()
star_rating_var = microwave_df['star_rating'].var()

helpful_votes_avg = microwave_df['helpful_votes'].mean()

word_count_sum = microwave_df['word_count'].sum()
word_count_avg = microwave_df['word_count'].mean()
#列表表示microwave的统计数据
microwave = [total, star_rating_avg, helpful_votes_avg, star_rating_var, word_count_sum, word_count_avg]

"3.2.3 产生pacifier统计信息列表"
total = pacifier_df['star_rating'].count()
star_rating_avg = pacifier_df['star_rating'].mean()
star_rating_var = pacifier_df['star_rating'].var()

helpful_votes_avg = pacifier_df['helpful_votes'].mean()

word_count_sum = pacifier_df['word_count'].sum()
word_count_avg = pacifier_df['word_count'].mean()
#列表表示pacifier的统计数据
pacifier = [total, star_rating_avg, helpful_votes_avg, star_rating_var, word_count_sum, word_count_avg]

"3.2.4 把统计信息汇总生成一个数据框"
Row_Name = ['total','star_rating_avg', 'helpful_votes_avg', 'star_rating_var','word_count_sum' ,'word_count_avg']
data_statics = pd.DataFrame(
    {
        "Row_Name": Row_Name,
        "pacifier": pacifier,
        "microwave": microwave,
        "Hair_Dryer": Hair_Dryer,
        #如果有其它产品，可以添加到这里,
    },
    #index = Row_Name
)
# 转置显示
ddf = data_statics.T
print(data_statics) #仅打印显示，不需要plot画图
print(ddf) #仅打印显示，不需要plot画图

"3.2.5 转换为三个产品各统计数据占比 -- 用于可视化作图" 
data_statics["sum"] =  data_statics["pacifier"] + data_statics["microwave"] + data_statics["Hair_Dryer"]
data_statics["normal_percent_p"] =  data_statics["pacifier"] / data_statics["sum"] 
data_statics["normal_percent_m"] =  data_statics["microwave"] / data_statics["sum"] 
data_statics["normal_percent_h"] =  data_statics["Hair_Dryer"] / data_statics["sum"]
#data_statics["normal"] =  data_statics["sum"] / data_statics["sum"]

df3 = data_statics.drop(["pacifier", "microwave", "Hair_Dryer", "sum"],axis=1)
ddf3 = df3.T
print(df3)
print(ddf3)



'''
4. 可视化作图
'''
" 4.1箱型图 - 显示各指标 "
#fig=plt.figure()
#plt.rcParams["font.sans-serif"] = ["SimHei"]      #设置显示中文
#ax1=fig.add_subplot(121)
#plt.boxplot(ddf3["total"],vert=True) 
#plt.title('',size=20)
#plt.show()


" 4.2堆叠图 "
# importing package
import matplotlib.pyplot as plt
 
# create data
x  = df3["Row_Name"]
y1 = df3["normal_percent_p"]
y2 = df3["normal_percent_m"]
y3 = df3["normal_percent_h"]

 # plot bars in stack manner
plt.bar(x, y1, color='r')
plt.bar(x, y2, bottom=y1, color='b')
plt.bar(x, y3, bottom=y2, color='g')

plt.rcParams["font.sans-serif"] = ["SimHei"]      #设置显示中文
plt.xlabel("评价指标")
plt.ylabel("Score")
plt.legend(["pacifier", "microwave", "Hair_Dry"])
plt.title("3个产品评价指标对比")
plt.show()

" 4.3星级评分分布图 - 以star_rating为例"
import matplotlib.pyplot as plt
import seaborn as sns

# 把3个产品的数据框合并，并增加1列以区分
hair_df["product"] = "hair_df"
pacifier_df["product"] = "pacifier"
microwave_df["product"] = "microwave"

frames = [hair_df, pacifier_df, microwave_df]
result_df = pd.concat(frames, ignore_index = True) #合并数据框，忽略原始index

# 画图
sns.displot(data=result_df,x="star_rating",kind='kde', hue="product")
plt.show()


" 4.4 评分相关性分析视图"
# 函数定义
def draw_corr(corr, title):
    #定义热图的横纵坐标
    xLabel = ['sr','rs','hr','rc']
    yLabel = ['sr','rs','hr','rc']
 
    #准备数据阶段，利用random生成二维数据（5*5）

    #作图阶段
    fig = plt.figure()
    plt.rcParams["font.sans-serif"] = ["SimHei"]      #设置显示中文
    #定义画布为1*1个划分，并在第1个位置上进行作图
    ax = fig.add_subplot(111)
    #定义横纵坐标的刻度
    ax.set_yticks(range(len(yLabel)))
    #ax.set_yticklabels(yLabel, fontproperties=font)
    ax.set_yticklabels(yLabel)
    ax.set_xticks(range(len(xLabel)))
    ax.set_xticklabels(xLabel)
    #作图并选择热图的颜色填充风格，这里选择blue
    im = ax.imshow(corr, cmap=plt.cm.hot)
    #im = ax.imshow(corr)
    #增加右侧的颜色刻度条
    plt.colorbar(im)
    #增加标题
    plt.title(title)
    #show
    plt.show()


# 函数调用
corr = hair_df2.corr()
title ="Hair Dryer"
draw_corr(corr, title)

corr = microwave_df2.corr()
title ="Microwave Oven"
draw_corr(corr, title)

corr = pacifier_df2.corr()
title ="Pacifier"
draw_corr(corr, title)
