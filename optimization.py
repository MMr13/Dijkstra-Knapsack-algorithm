from random import choice
import matplotlib.pyplot as plt
from functools import reduce
import numpy as np
def data():
    f=open('Data_1.csv','r')
    a=f.readlines()
    del(a[0])
    ie,ne=[],[]
    for i in range(len(a)):
        ie.append(int(a[i][:a[i].find(',')]))
        a[i]=a[i][a[i].find(',')+1:]
        ne.append(str(a[i][:a[i].find(',')]))
    EMPLOYEE=[]
    for i in range(len(ie)):
       EMPLOYEE.append((ie[i],ne[i]))
    return(EMPLOYEE,len(a))
def data2():
    f=open('Data_2.csv','r')
    a=f.readlines()
    del(a[0])
    sx,nx,sy,ny=[],[],[],[]
    for i in range(len(a)):
        a[i]=a[i][a[i].find(',')+1:]
        sx.append(int(a[i][:a[i].find(',')]))
        a[i]=a[i][a[i].find(',')+1:]
        sy.append(int(a[i][:a[i].find(',')]))
        a[i]=a[i][a[i].find(',')+1:]
        nx.append(int(a[i][:a[i].find(',')]))
        a[i]=a[i][a[i].find(',')+1:]
        ny.append(int(a[i][:a[i].find(',')]))
    Task=[]
    for i in range(len(sx)):
       Task.append([(sx[i],sy[i]),(nx[i], ny[i])])
    return(Task,len(a))
def label():
    a=data2()[0]
    x,y=[],[]
    for i in range(len(a)):
       x.append(a[i][0][0])
       x.append(a[i][1][0])
       y.append(a[i][0][1])
       y.append(a[i][1][1])
    set(x)
    set(y)
    n=(abs(max(x)-min(x)+1))*(abs(max(y)-min(y)+1))
    mylabel={}
    for i in range(n):
        mylabel[i]=str(i)
    mylabel2={}
    k=0
    for i in range(min(x), max(x) + 1):
        for j in range(min(y), max(y) + 1):
            mylabel2[str(k)]=(i, j)
            k=k+1
    return (mylabel,mylabel2,(min(x),max(x)),(min(y),max(y)))
mylabel,mylabel2=label()[0:2]
def mat():
    a,b=label()[1],len(label()[1])
    mat=np.zeros(shape=(b,b),dtype=int)
    for i in range(b):
        for j in range(b):
            if a[str(i)][0]==a[str(j)][0]:
                if abs(a[str(i)][1]-a[str(j)][1])==1:
                    mat[i][j]=10
            if a[str(i)][1]==a[str(j)][1]:
                if abs(a[str(i)][0]-a[str(j)][0])==1:
                    mat[i][j]=10
    return(mat.tolist())
def grid_show():
    Adj_Matrix=mat()
    b=len(mylabel2)
    z,w=label()[2:4]
    xCoord=[mylabel2[k][0] for k in mylabel2]
    yCoord=[mylabel2[k][1] for k in mylabel2]
    plt.axis([z[0]-1,z[1]+1,w[0]-1,w[1]+1])
    for i in range(b):
        for j in range(b):
            if Adj_Matrix[i][j]:
                plt.plot([xCoord[i],xCoord[j]],[yCoord[i],yCoord[j]],'#eeefff')
def start_target(m):
    d=data2()[0][m]
    a=label()[1]
    for i in range(len(a)):
        if a[str(i)]==d[0]:
            start=str(i)
        if a[str(i)]==d[1]:
            target=str(i)
    return(start,target)
def dijkstra(graph,task):
    start=task[0]
    target=task[1]
    inf=reduce(lambda x,y: x+y,(i[1] for u in graph for i in graph[u]))
    dist=dict.fromkeys(graph,inf)
    prev=dict.fromkeys(graph)
    q=list(graph)
    dist[start] = 0
    while q:
        u=min(q,key=lambda x:dist[x])
        q.remove(u)
        for v,w in graph[u]:
            alt=dist[u]+w
            if alt<dist[v]:
                dist[v]=alt
                prev[v]=u
    trav=[]
    temp=target
    while temp!=start:
        trav.append(prev[temp])
        temp=prev[temp]
    trav.reverse()
    trav.append(target)
    return(trav,dist[target])
def graph():
    a=mat()
    g={}
    for i in range(len(a)):
        l=[]
        for j in range(len(a)):
            if a[i][j]==10:
                l.append((str(j),10))
        g[str(i)]=l
    return(g)
def plot_task(m):
    d=data2()[0][m]
    z,w=label()[2:4]
    mydrawing= dijkstra(graph(), start_target(m))[0]
    plt.plot([mylabel2[n.rstrip()][0] for n in mydrawing],[mylabel2[n.rstrip()][1] for n in mydrawing],choice(['b','g','r','c','m','y','k']),label=str(m+1))
    plt.text(d[1][0]+0.1,d[1][1]+0.1,str(m+1))
    plt.axis([z[0]-1,z[1]+1,w[0]-1,w[1]+1])
    plt.plot([d[0][0],d[1][0]],[d[0][1],d[1][1]],'bo')
def distance_tasks():
    Distance=[]
    for i in range(data2()[1]):
        dist=dijkstra(graph(),start_target(i))[1]
        Distance.append(dist)
    return(Distance)
def time_tasks(v): #v=10 feet/min
    dl=distance_tasks()
    for i in range(len(dl)):
        dl[i]=dl[i]/v
    return(dl)
print(time_tasks(10))
def Knapsack(employee_list,task_time_list):
    totaltime = reduce(lambda x, y: x + y, time_tasks(10))
    if totaltime % data()[1] == 0:
        sum_to_be_formed = totaltime / data()[1]
    else:
        sum_to_be_formed = int(totaltime / data()[1]) + 1
    p=task_time_list
    el=employee_list
    hhh=[]
    fi={}
    def Knap(l):
        r=[]
        list_of_numbers=sorted(l)
        list_of_numbers.reverse()
        def a(n,b):
            if(len(b)==0):
                return False
            while(b[0]>n):
                b.remove(b[0])
                if(len(b)==0):
                    return False
            if(b[0]==n):
                r.append(b[0])
                return True
            if(len(b)==1):
                return False
            for i in b:
                if(a(round(n-i,2),b[b.index(i)+1:])):
                    r.append(i)
                    return True
        if(a(sum_to_be_formed,list_of_numbers)):
            hhh.append(r)
        for i in r:
            del(p[p.index(i)])
    if len(el)==len(p):
        for i in range(len(el)):
            fi[el[i]]=[p[i]]
    else:
        for i in range(len(el)):
            Knap(p)
        for i in hhh:
            i=sorted(i,reverse=True)
        hhh.append(p)
        if len(el) != len(hhh):
            totaltime = reduce(lambda x, y: x + y, hhh[-1:][0])
            if totaltime % (data()[1] - (len(hhh) - 1)) == 0:
                sum_to_be_formed = totaltime / (data()[1] - (len(hhh) - 1))
            else:
                sum_to_be_formed = int(totaltime / (data()[1] - (len(hhh) - 1))) + 1
            print(sum_to_be_formed)
            for i in range(data()[1] - (len(hhh) - 1)):
                Knap(hhh[-1:][0])
            if len(el) != len(hhh):
                sum_to_be_formed=sum_to_be_formed+1
            for i in hhh[-1:][0]:
               i = sorted(i, reverse=True)
            hhh.append(hhh[-1:][0])
        for i in range(len(el)):
            fi[el[i]]=hhh[i]
    return(fi)
def get_task_EMPLOYEE(q,r):
    a=q
    b=r
    bb={}
    for i in range(len(b)):
        bb[i]=b[i]
    aa={}
    for i in a:
        l=[]
        for j in a[i]:
            for key, value in bb.items():
                if j==value:
                    l.append(key+1)
                    del(bb[key])
                    break
        aa[i]=l
    return (aa)
def plot_EMPLOYEE_Task(n):
    a=get_task_EMPLOYEE(Knapsack(data()[0],time_tasks(10)),time_tasks(10))
    l=a[n]
    grid_show()
    for i in l:
        plot_task(i-1)
    plt.title(str(n))
    fig=plt.gcf()
    plt.show()
    plt.draw()
    fig.savefig(str(n[0])+'-'+str(n[1])+'.png',dpi=300)
def final_task_EMPLOYEES():
    a=Knapsack(data()[0],time_tasks(10))
    d=get_task_EMPLOYEE(Knapsack(data()[0],time_tasks(10)),time_tasks(10))
    f=open('final_task_EMPLOYEES.txt','w')
    for i in d:
        print(i,'\t','-> ','Lists of Tasks:',d[i],'\t','total time:',reduce(lambda x,y: x+y,a[i]),'min')
        f.write(str(i)+'\t'+'-> '+'Lists of Tasks:'+str(d[i])+'\t'+'total time:'+str(reduce(lambda x,y: x+y,a[i]))+'min')
        f.write('\n')
    f.close()
def plot_for_all_EMPLOYEE():
    for i in data()[0]:
        plot_EMPLOYEE_Task(i)
final_task_EMPLOYEES()
plot_for_all_EMPLOYEE() # plot just for on EMLOYEE with plot_EMPLOYEE_Task(n) -> for example: plot_EMPLOYEE_Task((9,'IRVINE'))
