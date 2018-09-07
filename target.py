# encoding:utf-8
import numpy as np
import pandas as pd

# import math

def loadSet(sale_mem, mem_prod):

        s = pd.read_excel(sale_mem)  # s for sale
        s.columns = ['OG', 'MID', 'PID', 'quantity']
        del s['OG']

        # merge p and pass the values into map
        p = pd.read_csv(mem_prod)  # p for product
        p.columns = ['OG','MID', 'PID', 'quantity']
        del p['OG']

        p_nrow = len(p['PID'])
        m = {}
        m[p.iloc[0, 0]] = [[str(p.iloc[0, 1]),str(p.iloc[0,2])]]

        list = np.array(s['MID']).tolist() # convert dataFrame to list, so we can use p.iloc[i,0] in list
        for i in range(p_nrow):
             if p.iloc[i,0] in list:
                if p.iloc[i,0] in m:
                    m[p.iloc[i,0]].append([str(p.iloc[i,1]),str(p.iloc[i,2])])

                else:
                    m[p.iloc[i,0]] = [[str(p.iloc[i,1]),str(p.iloc[i,2])]]

        # 还有一种方法：标记s在p中的mem 然后从s中把这些mem提取出来
        return s, m

def loadTarget(t):
    # need adjustion
    t ="2ECB826DFF730E48E05337030201EA76': [['8502745', 0.3333], ['1000400', 0.6667]]"
    list = [['8502745', 0.3333], ['1000400', 0.6667]]
    return list

def calSupp(m):
    sum = []
    for key in m:
        lsum = 0
        list = m[key]
        for sublist in list:
            if len(sublist) > 1:
             lsum += float(sublist[1])
            else:
                sublist.append(1) # if dont have quantity listed, then assume one
        sum.append(lsum)
        # if lsum != 0:
        for sublist in list:
            sublist[1] = float(sublist[1])/lsum
            # sublist[1] = round(float(sublist[1])/lsum, 4)
    return m

def cosChoose(m, target):
    x = []
    simi = {}

    for sublist in target:
        x.append(sublist[1])

    for key in m:
        y = []
        list = m[key]
        for sublist in list:
            y.append(sublist[1])
        # calculate cosine similarity, transfer list to vector
        dot_product = 0.0
        normA = 0.0
        normB = 0.0
        for a, b in zip(x, y):
            dot_product += a * b
            normA += a ** 2
            normB += b ** 2
        if normA != 0.0 and normB != 0.0:
            cossimi = dot_product / ((normA * normB) ** 0.5)
            # ** means square
            # why return 1.00?
            if cossimi > 0.9:
                simi[key] = cossimi

    return simi

# # radix sort
# def sort(dict):
#     # 有多少个item
#     n = len(dict)
#     digitQ =[]
#     # 保留多少位小数
#     r = 3
#     for i in range(10):
#         digitQ.append([])
#
#     list= []
#     for key in dict:
#         list.append([key, 1000*round(dict[key],3)])
#
#     # for 小数最后一位pos到第一位
#     pos = r-1
#     while pos >= 0 :
#       # for list里每一个item: list[j]
#       for j in range(n):
#           # x = list[j]里的item在pos位的数字
#           temp = list[j] # temp in the form [key, value]
#           dx = str(temp[1])
#           x = int(dx[pos])
#           digitQ[x].append(temp)
#       index = 0
#       for i in range(10):
#           while digitQ[i]:
#                 list[index] = digitQ[i].pop(0)
#                 index += 1
#       pos = pos - 1
#
#     # print list
#     return list


# def radix_sort(lists, radix=10):
#     lists = dict.values()
#     k = int(math.ceil(math.log(max(lists), radix)))
#     bucket = [[] for i in range(radix)]
#     for i in range(1, k+1):
#         for j in lists:
#             bucket[j/(radix**(i-1)) % (radix**i)].append(j)
#         del lists[:]
#         for z in bucket:
#             lists += z
#             del z[:]
#     return lists


def select_sort(dict):
    # 选择排序
    lists= dict.values()
    count = len(lists)
    for i in range(0, count):
        min = i
        for j in range(i + 1, count):
            if lists[min] > lists[j]:
                min = j
        lists[min], lists[i] = lists[i], lists[min]

    a = dict.keys()[dict.values().index(lists.pop())]

    return a

def main():
    s, dataSet = loadSet('sale_mem.xlsx','mem_prod.csv')

    # trial 1: 2ECB826DFF730E48E05337030201EA76

    target = loadTarget('target.xlsx')

    suppData = calSupp(dataSet)
    # top similiar members

    simi_mems = cosChoose(suppData, target)
    print simi_mems
    # sorted top similiar members, return the first mem
    # 说dict是nontype does not have attribute values
    the_mem = select_sort(simi_mems)
    print the_mem
    # need to get the index of mem then return the product related to mem in s
    a = list(s['MID']).index(the_mem)
    target_prod = s.iloc[a,1]
    print target_prod, "can be promoted to target member 2ECB826DFF730E48E05337030201EA76"

if __name__ == '__main__':
    main()

    '''
    result simple analysis
    8502745 打包袋 （要进行数据处理） 
    1000400 莫匹罗星软膏：治疗皮肤疾病
    2010023 三七粉：治疗创伤
    '''


