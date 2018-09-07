

import pandas as pd


def loadDataSet():
        address = '/Users/Evangeline0519/PycharmProjects/Apriori/3002986.csv'
        # address = '/Users/Evangeline0519/PycharmProjects/Receipt_Sale/mem_prod_choose_c.xlsx'
        c = pd.read_excel(address)
        c.columns = ['OID', 'PID']
        m = {}
        nrow = len(c['OID'])
        m[c.iloc[0, 0]] = [str(c.iloc[0, 1])]
        for i in range(nrow):
            if c.iloc[i,0] in m:
             m[c.iloc[i,0]].append(str(c.iloc[i,1]))

            else:
               m[c.iloc[i,0]] = [str(c.iloc[i,1])]

        #  delete keys that only have one value
        temp = []
        for key in m:
            if len(m[key]) == 1:
                temp.append (key)
        for item in temp:
            del m[item]

        ds = list()
        ds.append(m.values())

        ds = ds[0]
        return ds

def createC1(dataSet):
    c1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in c1:
                c1.append([item])
    c1.sort()
    # print "C1:",len(c1)
    return map(frozenset,c1)

def scanD(D,Ck,minSupport):

    ssCnt = {}

    for tid in D:
        for can in Ck:
            if can.issubset(tid):
                ssCnt[can] = ssCnt.get(can, 0) + 1
    numItems = float(len(D))
    retList = []
    supportData = {}
    for key in ssCnt:
        support = ssCnt[key]/numItems
        if support > minSupport:
            # retList.append(key)
            retList.insert(0,key)
            # print key, support
        supportData[key] = support
        #print key,support
    return retList,supportData

def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1,lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if(L1 == L2):
                retList.append(Lk[i] | Lk[j])
    return retList

def apriori(dataSet,minSupport = 0.2):

    c1 = createC1(dataSet)
    D = map(set,dataSet)
    L1,supportData = scanD(D,c1,minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0 ):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        # print "Ck:",len(Lk),Lk
        supportData.update(supK)
        L.append(Lk)
        k = k+1
    return L,supportData

def generateRules(L,supportData,minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1= [frozenset([item]) for item in freqSet]
        # print  H1,H1[0],len(H1[0])
            if(i>1):
                rulesFromConseq(frozenset,H1,supportData,bigRuleList,minConf)
            else:
                calConf(frozenset,H1,supportData,bigRuleList,minConf)
    return bigRuleList


def calConf(freqSet, H, supportData, brl, minConf = 0.7):
    prunedh = []
    for conseq in H:
        conf = supportData[freqSet]/supportData[freqSet - conseq]
        if conf >= minConf:
            print freqSet - conseq,'-->',conseq,'conf:',conf
            brl.append((freqSet-conseq,conseq,conf))
            prunedh.append(conseq)
    return prunedh
def rulesFromConseq(freqSet,H,supportData,brl,minConf=0.7):
    m = len(H[0])
    if(len(freqSet)>m+1):
        Hmpl = aprioriGen(H,m + 1)
        Hmpl = calConf(freqSet,Hmpl,supportData,brl,minConf)
        if(len(Hmpl) > 1):
            rulesFromConseq(freqSet,Hmpl,supportData,brl,minConf)


def main():

    dataSet = loadDataSet()
    # loadDataSet()
    # c1 = createC1(dataSet)
    # D = map(set,dataSet)
    # L1,supportData0=scanD(D,c1,0.5)
    # print L1
    # print dataSet
    print "len_dataset:",len(dataSet)
    minSupport = 200.0/len(dataSet)
    print "minSupport:",minSupport
    # minSupport = 0.2
    L,supportData = apriori(dataSet=dataSet,minSupport=minSupport)
    # rule=generateRules(L, supportData, minConf=0.7)
    # print supportData
    for key in supportData:
        # if len(key)>8:
       # for j in key:
            # if len(key)>1  and  '3002986' in j:
               print "result:",key,supportData[key]


        # if len(L[i]) >1  :
    #         print L[i]
    # print supportData
    # print L
    # print L[3]
    # print aprioriGen(L[1],3)
    # print supportData




if __name__ == '__main__':
    main()



