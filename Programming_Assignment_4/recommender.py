### 2017.06.06 Wanju Kim ###
### user-based collaborative filtering ###

import sys
import math


def ReadInput(fileName,function): # function!=1, training data / function==1, test data
    File=open(fileName,'r')
    itemDic={}
    itemList=[]
    userID=0
    for line in File:
        line=line.replace('\n','')
        splited=line.split('\t')
        splited.pop()  # time stamp
        splited = [int(i) for i in splited]
        if function==1: # testing data
            splited.pop() # rating
            itemList.append(splited)
            continue
        if splited[0]!=userID: # training data
            userID=splited[0]
            itemDic[userID]=[]
        splited.remove(userID)
        itemDic[userID].append(splited)
    File.close()
    if function==1:
        return itemList
    else:
        return itemDic


### get the items that exists for both users
### predUserList=the user predict

def GetSameItemset(predUserList,otherUserList):
    itemDic={}
    for predUserItem in predUserList:
        for otherUserItem in otherUserList:
            if predUserItem[0] == otherUserItem[0]:
                bothItemList=[]
                bothItemList.append(predUserItem[1]) # pred
                bothItemList.append(otherUserItem[1]) # other
                itemDic[predUserItem[0]]=bothItemList
    return itemDic


### calculate the average of item in sameItemList that belongs to both users
### userItemList can be user1's, user2's

def AverageUserRating(sameItemList,type):
    sum=0
    for itemID in sameItemList:
        sum+=sameItemList[itemID][type] # pred or other
    return sum/len(sameItemList)


### Calculate the all similarity between pred and another users

def GetSimilarity(sameItemList,avgList):
    predAvg=AverageUserRating(sameItemList,0) # pred
    otherAvg=AverageUserRating(sameItemList,1) # other
    avgList.append([predAvg,otherAvg])
    numerator=0
    denominator1=0
    denominator2=0
    for itemID in sameItemList:
        predItemDif = sameItemList[itemID][0] - predAvg
        otherItemDif = sameItemList[itemID][1] - otherAvg
        numerator+=predItemDif*otherItemDif
        denominator1+=math.pow(predItemDif,2)
        denominator2+=math.pow(otherItemDif,2)
    if (denominator1==0) or (denominator2==0): # zero division
        return 0
    return numerator/(math.sqrt(denominator1)*math.sqrt(denominator2))


### Get similarity dic between pred and another users

def GetsimDic(allAvgList,predUser):
    global trainingData
    simDic={}
    avgList=[]
    for otherUserID in trainingData:
        if predUser!=otherUserID:
            sameItemList=GetSameItemset(trainingData[predUser],trainingData[otherUserID])
            if len(sameItemList)==0: # when there is no same item
                continue
            similarity=GetSimilarity(sameItemList,avgList)
            if similarity>0.5: ###????? or neighbor 30?
                simDic[otherUserID]=similarity
            elif similarity>1:
                simDic[otherUserID]=1.0
            else:
                avgList.pop
    allAvgList.append(avgList)
    return simDic


###

def Filtering(allSimDic,allAvgList,testingData):
    userID=0
    for predUser in testingData:
        if predUser[0]!=userID: # first user met
            userID=predUser[0]
            allSimDic[userID]=GetsimDic(allAvgList,userID)
        else: # already simList found user
            continue


### Get rating

def GetRating(userID,ItemID):
    global trainingData
    for tuple in trainingData[userID]:
        if tuple[0]==ItemID:
            return tuple[1]
    return 0 # no pred Item


### Get prediction

def GetPrediction(simDic,avgList,predItemID):
    global trainingData
    numerator=0
    denominator=0
    count=0
    for simUserID in simDic:
        rating=GetRating(simUserID,predItemID)
        if rating==0:
            continue
        numerator+=simDic[simUserID]*(rating-avgList[count][1]) # rating 넣기
        denominator+=simDic[simUserID]
        count+=1
    if denominator<=0: # zero division
        return 1
    prediction=avgList[0][0]+numerator/denominator

    if prediction<1:
        return 1
    elif prediction>5:
        return 5
    else:
        return int(prediction)


def WriteOutput(testingData,fileName):
    output="u%s.base_prediction.txt"%fileName[1]
    File=open(output,'w')
    for tuple in testingData:
        content=''
        count=0
        for info in tuple:
            content+=str(info)
            if count==2:
                break
            content+='\t'
            count+=1
        content+='\n'
        File.write(content)
    File.close()


if(len(sys.argv)!=3):
    print("recommender.py <training data> <test data>")
    sys.exit(1)

trainingFile=sys.argv[1]
testingFile=sys.argv[2]

trainingData=ReadInput(trainingFile,0) # read training data

testingData=ReadInput(testingFile,1) # read testing data

AllSimDic = {}
AllAvgList=[]

Filtering(AllSimDic,AllAvgList,testingData)

userID=0
count=-1

for testTuple in testingData:
    if testTuple[0]!=userID:
        userID=testTuple[0]
        count += 1
    predRating=GetPrediction(AllSimDic[userID],AllAvgList[count],testTuple[1])
    testTuple.append(predRating)

WriteOutput(testingData,testingFile)
