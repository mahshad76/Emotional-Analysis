from csv import reader
import numpy
from scipy.spatial import distance
import random
import math
from numpy import linalg as la
import csv

def max_distance(data):
    max=0
    for i in range(0,len(data)):
        for j in range(i+1,len(data)):
            dst = distance.euclidean(data[i],data[j])
            if(dst>max):
                max=dst
    return max

def min_max_range(data,dimension):
    min_max = numpy.zeros((dimension, 2))
    for i in range(0,dimension):
        min_max[i, 0] = numpy.max(numpy.array(data)[:,i])
        min_max[i, 1] = numpy.min(numpy.array(data)[:,i])
    return min_max

def mutation(parents,num_feature,dimension):
    rate=1/(math.sqrt(num_feature))
    delta=math.exp(-1*rate*numpy.random.normal(0,1))
    count=len(parents)
    muted=[]
    i=0
    while(i<count):
        list=[]
        parents[i][dimension-1]=parents[i][dimension-1]*delta
        for j in range(0,dimension-1):
            list.append(parents[i][j]+(parents[i][dimension-1]*numpy.random.normal(0,1)))
        list.append(parents[i][dimension - 1])
        turn=0
        if(i==0):
            muted.append(list)
            i+=1
        else:
            for j in range(0,len(muted)):
                if (list[0:len(list) - 1] == muted[j][0:len(list) - 1]):
                    print(j)
                    turn=1
                    break
            if(turn==0):
                muted.append(list)
                i+=1
    return muted

def calculateG(cluster,train,num_feature,array):
    cluster_center=[]
    index=0
    for i in range(0,cluster):
        list=[]
        for j in range(0,num_feature):
            list.append(array[index])
            index+=1
        cluster_center.append(list)
    num_data = len(train)
    g = [ [0]*cluster for i in range(num_data)]
    for j in range(0,cluster):
        for i in range(0,num_data):
            sum=0
            for y in range(0,num_feature):
                sum+=(train[i][y]-cluster_center[j][y])**2
            #print(sum)
            g[i][j]=sum*math.log(math.sqrt(sum))
    return g

def y_of_network(g,w):
    return numpy.dot(g,w)

def calculateW(g,y,cluster):
    lam = 0.01
    w = la.inv(g.transpose().dot(g) + lam * numpy.identity(cluster)).dot(g.transpose()).dot(y)
    return w

def fitness(y,y_net):
    error=0
    for i in range(0,2000):
       if(y_net[i][0]<0):
           error+=1
    for i in range(2000,4000):
        if (y_net[i][1] < 0):
            error += 1
    precision=1-(error/4000)
    return precision

def q_tournament(parents,fitnesses,population,parents_count,iteration):
    count=0
    remainder=[]
    max_fit=0
    max_fit_index=0
    b=0
    while count<population:
        i1=random.randint(0,parents_count - 1)
        i2 = random.randint(0, parents_count - 1)
        if(b==2000):
            for jj in range(0,parents_count):
                print("b=10")
                print(jj)
                if parents[jj] not in remainder:
                    remainder.append(parents[jj])
                    count += 1
                    b=0
                    print("worst")
                    print(count)
                    if (fitnesses[jj] > max_fit):
                        max_fit = fitnesses[jj]
                        max_fit_index = jj
                    break
        elif(fitnesses[i1]>=fitnesses[i2]):
            print("next one")
            if(parents[i1] not in remainder):
                remainder.append(parents[i1])
                b=0
                if(fitnesses[i1]>max_fit):
                    max_fit=fitnesses[i1]
                    max_fit_index=i1
                print("best:")
                print(count)
                count+=1
            else:
                b+=1
                print("plus b")
                print(b)
    if(iteration==1084):
        print("max fit")
        print(max_fit)
        with open(r"C:\Users\Mohammadreza Rahmani\Desktop\best_parent.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(parents[max_fit_index])
    print("max fitness")
    print(max_fit)
    print("parent max fitness:")
    print(parents[max_fit_index])
    print("/////////////////////")
    return remainder

def ES(cluster,num_feature,min_max,max_distance,train,y):
    population=500#increase population=3500
    dimension=(num_feature*cluster)+1
    samples = []
    for i in range(0, population):
        chromosome = []
        for j in range(0, cluster):
            for m in range(0, num_feature):
                chromosome.append(random.random() * (min_max[m][0] - min_max[m][1]) + min_max[m][1])
                    # chromosome.append(random.random() * (max_range - min_range) + min_range)
        chromosome.append(random.random() * max_distance)
        samples.append(chromosome)
    parents_count=7*population
    for i in range(0,1085):#1085
        parents=[]
        for j in range(0,parents_count):
            index=random.randint(0, population-1)
            parents.append(samples[index])
        parents=mutation(parents,num_feature,dimension)
        fitnesses=[]
        for j in range(0,parents_count):#pqrents_count
            g=numpy.array(calculateG(cluster,train,num_feature,parents[j]))
            w=numpy.array(calculateW(g,y,cluster))
            y_net=y_of_network(g,w)
            fitnesses.append(fitness(y,y_net))
            print(j)
        print(fitnesses)
        samples=q_tournament(parents,fitnesses,population,parents_count,i)
        print("samples")
        print(samples[0:4])
        print(len(samples))
        print("hi")
        print("iteration")
        print(i)
    return

def main():
    num_class=2
    cluster=4*num_class
    with open(r'C:\Users\Mohammadreza Rahmani\Desktop\embedding_train.csv', 'r') as read_obj:
        csv_reader = reader(read_obj)
        list_of_rows = list(csv_reader)
    train_data = numpy.array(list_of_rows)
    train=[]
    for item in train_data:
        b = numpy.asarray(item, dtype=numpy.float64, order='C')
        train.append(list(b))
    train=train[0:2000]+train[2000:4000]#increase population

    y = [ [-1]*2 for i in range(len(train))]
    for i in range(0,2000):
        y[i][0]=1
    for i in range(2000,len(train)):
        y[i][1]=1
    num_feature=len(train[0])
    print(num_feature)
    maximum_distance=max_distance(train)
    min_max=min_max_range(train,num_feature)
    ES(cluster,num_feature,min_max,maximum_distance,train,y)

main()
