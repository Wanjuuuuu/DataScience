### 2017.04.20 ###
### WANJU  KIM ###

import sys
import math



#==== 0. The Collection of Functions and Class



# Tree Data Structure for Decision Tree

class Tree(object):
    def __init__(self):
        self.name={}
        self.node=[]
        self.childList=[]
        self.prev=None
    def next(self,child):
        return self.node[child]
    def prev(self):
        return self.prev
    def add(self,child):
        node1=Tree()
        self.childList.append(child)
        self.node.append(node1)
        node1.prev=self
        return node1

# Attribute & Data Scan

def ScanData(File,Attribute):
    tupleSet=[]
    line=File.readline()
    line = line.replace('\n', '')
    splited = line.split('\t')
    for attr in splited:
        Attribute.append(attr)
    for line in File:
        line=line.replace('\n','')
        splited=line.split('\t')
        tupleSet.append(splited)
    return tupleSet

# Make all tuple's Class Labels or Attribute Outcomes into a list

def MakeBranchList(Data,AttributeNo):
    checkList=[]
    for tuple in Data:
        checkList.append(tuple[AttributeNo])
    return checkList

# Find out Class Labels or Branch types and also the number of each of them

def FindBranch(Data,AttributeNo):
    countDic = {}
    branchList = MakeBranchList(Data,AttributeNo)
    for branch in branchList:  # Count the number of each Class Label
        if branch not in countDic.keys():
            countDic[branch] = 1
        else:
            countDic[branch] += 1
    return countDic # Return all the branches or class label

# Count all the tuples according to class label

def CountClassLabel(Data):
    global ClassLabel
    labelCounter={}
    ClassList=MakeBranchList(Data,-1)
    for Class in ClassLabel:
        labelCounter[Class]=0
        for item in ClassList:
            if item == Class:
                labelCounter[Class]+=1
    return labelCounter

# Make dic with all the needed values to compute the Gain Info

def GetValuesForGain(Data,classLabel,branchDic,AttributeNo):
    for branch in list(branchDic.keys()):
        countList={}
        for label in classLabel:
            countList[label] = 0
        branchDic[branch]=countList
        for tuple in Data:
            if tuple[AttributeNo]==branch:
                branchDic[branch][tuple[-1]]+=1 # put the Dictionary which has Class Label with its number

# Get total num of tuple which has specific branch

def GetTotalNumber(Dic):
    total=0
    for value in Dic.values():
        total+=value
    return total

# Calculate Info(D)

def GetExpectedInfo(Dic):
    total=GetTotalNumber(Dic)
    expectedInfo = 0  # Expected Information (entropy)
    for value in Dic.values():
        result = value / total
        if result!=0:
            expectedInfo -= result * math.log(result, 2)
        else: ###### if result is 0 then error occurred
            expectedInfo-=0
    return expectedInfo

# Splitting Method 1. Calculate all Attribute's Gain Ratio and Choose best one

def GainRatio(Data,AttributeList,BranchList):
    global OriginalAttr
    RatioList=[]
    classDic=CountClassLabel(Data)
    total=len(Data) # total num of Data
    for Attribute in AttributeList: # for each Attribute in AttributeList
        AttributeNo=OriginalAttr.index(Attribute)
        branchDic=FindBranch(Data,AttributeNo)
        GetValuesForGain(Data,list(classDic.keys()),branchDic,AttributeNo)
        expectedInfo=GetExpectedInfo(classDic)
        residualInfo=0
        splitInfo=0
        for branch in branchDic:
            totalBranch=GetTotalNumber(branchDic[branch])
            residualInfo+=(totalBranch/total)*GetExpectedInfo(branchDic[branch])
            splitInfo-=(totalBranch/total)*math.log(totalBranch/total,2)
        RatioList.append((expectedInfo-residualInfo)/splitInfo)
    # Find out which Attribute has the max value
    BestAttribute=AttributeList[RatioList.index(max(RatioList))]
    for branch in list(FindBranch(Data,OriginalAttr.index(BestAttribute)).keys()):
        BranchList.append(branch)
    return BestAttribute


# Splitting Method 2. Calculate all Attribute's Gain info and Choose best one
#
# def InformationGain(Data,AttributeList,BranchList):
#     global OriginalAttr
#     gainList=[]
#     classDic=CountClassLabel(Data)
#     # print("ClassDic : ")
#     # print(classDic)
#     total=len(Data) # total num of Data
#     for Attribute in AttributeList: # for each Attribute in AttributeList
#         AttributeNo=OriginalAttr.index(Attribute)
#         branchDic=FindBranch(Data,AttributeNo)
#         GetValuesForGain(Data,list(classDic.keys()),branchDic,AttributeNo)
#         # print("branchDic")
#         # print(branchDic)
#         expectedInfo=GetExpectedInfo(classDic)
#         residualInfo=0
#         for branch in branchDic:
#             totalBranch=GetTotalNumber(branchDic[branch])
#             residualInfo+=(totalBranch/total)*GetExpectedInfo(branchDic[branch])
#         gainList.append(expectedInfo-residualInfo)
#     print(max(gainList))
#     # Find out which Attribute has the max value
#     # print(gainList)
#     BestAttribute=AttributeList[gainList.index(max(gainList))]
#     for branch in list(FindBranch(Data,OriginalAttr.index(BestAttribute)).keys()):
#         BranchList.append(branch)
#     return BestAttribute

# Find out which Attribute has the most max value in 2 Selection Methods

def SelectAttribute(Data,AttributeList,BranchList):
    MaxGainRatioAttribute=GainRatio(Data,AttributeList,BranchList) # Using Gain Ratio
    # MaxGainInfoAttribute = InformationGain(Data, AttributeList, BranchList) # Using Gain Information
    return MaxGainRatioAttribute

# Check if all tuples are all of the same Class

def CheckSameClass(Data):
    classList=MakeBranchList(Data,-1)
    if classList.count(classList[0])==len(classList):
        return classList[0]
    else:
        return False

# Find out which is a major Class given tuples

def ReturnMajorityClass(Data):
    classDic = FindBranch(Data, -1)
    keys = list(classDic.keys())
    values = list(classDic.values())
    return keys[values.index(max(values))]  # Return the Class Label which has max number

def CopyAttributeList(AttributeList,SplitAttribute):
    CopiedList=[]
    for Attribute in AttributeList:
        CopiedList.append(Attribute)
    CopiedList.remove(SplitAttribute)
    return CopiedList

# Build Decision Tree

def BuildDecisionTree(Data,DT,AttributeList,Criterion,Branch):
    global OriginalAttr, realBranchList # keep all the Attribute
    BranchList=[]
    # Only when it is about root node
    if Criterion==None:
        Class=CheckSameClass(Data)
        if Class!=False:
            DT.name[Criterion]=Class
            return
        if any(AttributeList)==False:
            DT.name[Criterion] = ReturnMajorityClass(Data)
            return
        SplitAttribute=SelectAttribute(Data,AttributeList,BranchList)
        AttributeList.remove(SplitAttribute)
    else:
        Class=CheckSameClass(Data) # the same Class Label which all tuples have
        if Class!=False: # If tuples in D are all of the Same Class
            DT.name[Branch]=Class
            DT=DT.prev
            return
        if any(AttributeList)==False: # If AttributeList is empty
            DT.name[Branch] = ReturnMajorityClass(Data)
            DT=DT.prev
            return
        SplitAttribute=SelectAttribute(Data,AttributeList,BranchList)
        AttributeList=CopyAttributeList(AttributeList,SplitAttribute)
    # Common Code Area
    Criterion=SplitAttribute
    DT.name[Branch]=Criterion
    for realBranch in realBranchList[OriginalAttr.index(Criterion)]: # to find out whether all the branches can be made
        if realBranch not in BranchList:
            BranchList.append(realBranch)
    for Branch in BranchList:
        dataPartition=[]
        DT=DT.add(Branch)
        # Partition the tuples
        for tuple in Data:
            if tuple[OriginalAttr.index(SplitAttribute)]==Branch:
                dataPartition.append(tuple)
        if any(dataPartition)==False: # If Partitioned Data is empty
            DT.name[Branch]=ReturnMajorityClass(Data)
        else:
            BuildDecisionTree(dataPartition,DT,AttributeList,Criterion,Branch)
        DT =DT.prev

# Test non labeled data using Decision Tree Classification Rule

def TestClassificationRules(Data,DT,Outcome):
    global Attribute
    for Branch in DT.childList:
        dataPartition = []
        CriterionIndex=Attribute.index(DT.name[Outcome])
        ChildIndex = DT.childList.index(Branch)
        DT = DT.next(ChildIndex)
        for tuple in Data:
            if tuple[CriterionIndex]==Branch:
                Criterion=DT.name[Branch]
                if Criterion not in Attribute: # if Classifier has just class label
                    tuple.append(Criterion)
                    continue
                else:
                    dataPartition.append(tuple)
        TestClassificationRules(dataPartition,DT,Branch)
        DT=DT.prev



#==== 1. Get Arguments by sys class



if len(sys.argv)!=4:
    print("Usage: dt.py <TrainingFile> <TestFile> <OutputFile>")
    sys.exit()

TrainingFilename=sys.argv[1]
TestFilename=sys.argv[2]
OutputFilename=sys.argv[3]



#==== 2. Make Decision Tree with Training Data



TrainingFile = open(TrainingFilename,"r")

DecisionTree = Tree()
OriginalAttr=[]  ### Global Variable
Attribute=[]
realBranchList=[] # all Branches in Attributes

TrainingSet=ScanData(TrainingFile,Attribute)

ClassLabel=list(FindBranch(TrainingSet,-1).keys()) # Class labels will be needed to calculate splitting method

for attr in Attribute: # full attribute is needed to build decision tree
    OriginalAttr.append(attr)

for AttributeIndex in range(len(OriginalAttr)-1):
    realBranchList.append(list(FindBranch(TrainingSet,AttributeIndex).keys()))

Attribute.pop() # The last attribute is Class Attribute

BuildDecisionTree(TrainingSet,DecisionTree,Attribute,None,None) # Build the Decision Tree with Training Set

TrainingFile.close()



#==== 3. Apply Testing Data to Decision Tree



TestFile = open(TestFilename,"r")

Attribute.clear()

TestSet=ScanData(TestFile,Attribute)

Attribute.append(OriginalAttr[-1]) # Add Class Attribute ### Global Variable

TestClassificationRules(TestSet,DecisionTree,None) # Apply Test Set to DT for finding out the Class Label

TestFile.close()



#==== 4. Make Output File



OutputFile = open(OutputFilename,"w")

length=len(Attribute)-1

count=0

for attribute in Attribute:
    OutputFile.write(attribute)
    if count<length:
        OutputFile.write("\t")
    count += 1
OutputFile.write("\n")

for tuple in TestSet:
    count=0
    for attribute in tuple:
        OutputFile.write(attribute)
        if count<length:
            OutputFile.write("\t")
        count += 1
    OutputFile.write("\n")

OutputFile.close()
