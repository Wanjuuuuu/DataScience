import sys
import math


def ReadData(File,Visited):
    tuple=[]
    for line in File:
        line=line.replace('\n','')
        splited=line.split('\t')
        splited.remove(splited[0])
        splited=[float(i) for i in splited]
        tuple.append(splited)
        Visited.append(0)
    return tuple

def RegionQuery(Data,indexP):
    global Eps
    neighborSet=[]
    standard=Data[indexP]
    index=0
    for point in Data:
        result=math.sqrt(math.pow((standard[0]-point[0]),2)+math.pow((standard[1]-point[1]),2))
        if result<Eps: # point within P's eps-neighborhood
            neighborSet.append(index)
        index+=1
    return neighborSet

def CheckCluster(Cluster,indexP): # check whether object is already in any cluster
    for list in Cluster:
        for element in list:
            if element==indexP:
                return True
    return False

def ExpandCluster(Data,Cluster,Neighborhood,index,Num):
    global Visited,MinPts
    Cluster[Num].append(index)
    for point in Neighborhood:
        if Visited[point]==0: # if this point has not been visited yet
            Visited[point]=1
            NforPoint=RegionQuery(Data,point)
            if len(NforPoint)>=MinPts:
                Neighborhood+=NforPoint
        if CheckCluster(Cluster,point)==False: # if this point is not yet member of any cluster
            Cluster[Num].append(point)
    Cluster[Num].sort()

def DBSCAN(Data,Cluster):
    global Visited,MinPts
    Noise=[]
    index=0
    clusterNum=0
    for mark in Data:
        if Visited[index]==0: # if this mark has not been visited yet
            Visited[index]=1
            Neighborhood=RegionQuery(Data,index)
            if len(Neighborhood)<MinPts:
                Noise.append(index)
            else:
                Cluster.append([])
                ExpandCluster(Data,Cluster,Neighborhood,index,clusterNum)
                clusterNum+=1
        index+=1
    Cluster.sort(key=len)
    Cluster.reverse() # in order of the cluster which has more objects

def WriteOutput(Cluster,clusterNum,inputFilename):
    for number in range(clusterNum):
        output="input%s_cluster_%d.txt" %(str(inputFilename[5]), number)
        outputFile=open(output,'w')
        for object in Cluster[number]:
            outputFile.write(str(object)+'\n')
        outputFile.close()




if(len(sys.argv)!=5):
    print("clustering.py <inputFile> <n> <Eps> <MinPts>")
    sys.exit(1)

inputFile=sys.argv[1]
n=int(sys.argv[2])
Eps=int(sys.argv[3])
MinPts=int(sys.argv[4])

Cluster=[] # Key: # of Cluster, Value: the objects corresponding to this Cluster
Visited=[] # which object has been visited

input=open(inputFile,'r')
Data=ReadData(input,Visited) # read Data
input.close()

DBSCAN(Data,Cluster) # Density-Based

WriteOutput(Cluster,n,inputFile) # write outputfile according to set-format
