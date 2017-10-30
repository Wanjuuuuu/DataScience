import sys
import itertools


#==== 0. All of Functions



def CountTransaction(inputFile): # count the # of transaction
    File = open(inputFile, "r")
    TransactionNum=sum(1 for OneLine in File)
    File.close()
    return TransactionNum

def ScanTransaction():
    list=[]
    Line=File.readline()
    Line=Line.replace('\n','')
    Splited=Line.split('\t')
    for Item in Splited:
        Item=int(Item)
        list.append(Item)
    list.sort()
    return list

def AddTransaction():
    Transaction=[]
    for iteration in range(TransactionNum):
        Transaction.append(ScanTransaction())
    Transaction.sort()
    return Transaction

# Generating L1

def Generate_L1(Support_Count):
    # guess the range of itemID by min and max of ID
    min=trans[0][0]
    max=trans[TransactionNum-1][len(trans[TransactionNum-1])-1]
    C1=[]
    for i in range(min,max+1):
        C1.append([i])
    L1=CheckSupport(C1,Support_Count,0)
    return L1

# Generating Frequent Itemset

def CheckSupport(Ck,Support_Count,k):
    itemset=[]
    support=[]
    for i in Ck:# all sets in Lk # the members of L1 maybe it may not exist
        item_count=0
        for j in trans:# 500
            if len(set(j).intersection(set(i)))==k+1: # if a candidate exists at Transaction
                item_count+=1
        if item_count>=min_sup:# frequent item?
            itemset.append(i)
            support.append(item_count)
    Support_Count.append(support)
    return itemset # sets containing min_sup

def CheckDuplicate(C,set):
    if C.count(set)==0: # don't have duplicates
        return True
    else:
        return False

def SelfJoin(L,k):
    C=[]
    itemset=[]
    for i in L[k] :
        for j in L[k] :
            if (i[0:k]==j[0:k]) & (i[k]!=j[k]):
                itemset=i[0:k+1]
                itemset.append(j[k])
                itemset.sort()
                if CheckDuplicate(C,itemset):
                    C.append(itemset)
    return C

def GenerateSubset(Candidate,k): # getting subset using in Pruning, Generating association rule #
    subset_list=[]
    for iteration in range(1,k+1):
        for subset in itertools.combinations(set(Candidate),iteration):
            subset=list(subset)
            subset.sort()
            subset_list.append(subset)
    return subset_list

def Prune(L,C,k):
    if k==1: # Candidate 2 doesn't need to be pruned
        return C
    for Candidate in C:
        whole_subset=GenerateSubset(Candidate,k)
        for subset in whole_subset:
            if CheckDuplicate(L[len(subset)-1], subset):
                C.remove(Candidate)
                break # get out of loop
    return C


#==== 1. Get Arguments by sys class



if len(sys.argv) != 4:
    print("Usage: apriori.exe <min_sup> <input> <output>")
    sys.exit()


inputFile = sys.argv[2]
outputFile = sys.argv[3]
TransactionNum=CountTransaction(inputFile) # num of total trans
min_sup = int(sys.argv[1])*TransactionNum/100


#==== 2. Store Transaction Data with Sorting



File=open(inputFile,"r")

trans=AddTransaction()

File.close() # close input file


#==== 3. Generate Frequent Itemset



L=[] # list of frequent itemsets ( #: k )
Support_Count=[] # support counts of L[k]

L.append(Generate_L1(Support_Count)) # generate L1

k=0 # the list index of previous completed L

while len(L[k])!=0: # if there is no more L
    C=SelfJoin(L,k) # self joining
    Ck=Prune(L,C,k+1) # Prune
    Lk=CheckSupport(Ck,Support_Count,k+1) # >=min_sup
    L.append(Lk)
    k+=1


#==== 4. Generate Association Rule



File=open(outputFile,'w')

k=1

while len(L[k])!=0: # if there is no more L
    num=0
    for frequent_set in L[k]:
        whole_subset=GenerateSubset(frequent_set,k)
        for subset in whole_subset:
            opposite_subset=list(set(frequent_set)-set(subset)) # B in A->B
            opposite_subset.sort()
            ruleSupport=Support_Count[len(subset)-1][L[len(subset)-1].index(subset)] # support count of subset
            Support=Support_Count[k][num]/TransactionNum*100
            Confidence=(Support_Count[k][num]/ruleSupport)*100
            if (Confidence % 1 == 0.125) | (Confidence % 1 == 0.625): # exception for 0.125 and 0.625 (the limitation of method 'round' #
                Confidence+=0.001
            File.write("{"+str(subset).replace(' ','').replace('[','').replace(']','')+"}")
            File.write('\t')
            File.write("{"+str(opposite_subset).replace(' ','').replace('[','').replace(']','')+"}")
            File.write('\t')
            File.write(str("%.2f"%round(Support,2))) # support
            File.write('\t')
            File.write(str("%.2f"%round(Confidence,2))) # confidence
            File.write('\n')
        num+=1
    k+=1

File.close()
