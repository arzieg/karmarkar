# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 19:45:01 2017

@author: arne
"""

# Karmarkar - Karp Algotirhmus
# Zwei Phasen - erste Phase bestimme die maximale Differenz zw. zwei Partitionen
# (a) Calculate Difference 
# - {18, 17, 12, 11, 8, 2}
# (18 − 17) → 1 {12, 11, 8, 2, 1} 
# (12 − 11) → 1 {8, 2, 1, 1} 
# (8 − 2) → 6 {6, 1, 1} 
# (6 − 1) → 5 {5, 1} 
# (5 − 1) → 4 {4} 
#
# zweite Phase
# (b) Generate Partition Action S 
# Reverse Action    S1          S2
# -                 {4}         {}
#   4 → (5 − 1)     {5}         {1}
#   5 → (6 − 1)     {6}         {1, 1}
#   6 → (8 − 2)     {8}         {2, 1, 1}
#   1 → (12 − 11)   {11, 8}     {12, 2, 1}
#   1 → (18 − 17)   {17, 11, 8} {18, 12, 2}

# The upper bound is calculated as max {sum(S 1 ), sum(S 2 )} = max{36, 32} = 36.


# Karmarkar-Karp Algorithmus
import bisect as b

def kk_list(l, k):
    # calculate difference
    a=list(l)                        
    a.sort()                            # sortiere die Liste nach der Größe
    cost = 100000                       # Kosten (d.h. Differenz nach dem ersten durchlauf
    v = []

    while (len(a) > 1 ):
        print ("a: old {}".format(a))
        t1 = a.pop()
        t2 = a.pop()
        v.append(t1)
        v.append(t2)                     
        #z = a.pop() - a.pop()           # Subtrahiere Element 0 von 1
        z = t1 - t2
        v.append(z)
        b.insort(a,z)                   # sortiere z in die Liste ein
        #m.append(z)                     # Differenzwert speichern
        cost=z
        print ("a: new {}".format(a))
        print ("cost = {}".format(cost))
        print ("=============================")
    print ("v={}".format(v))
    print ("Upper bound:{}".format(cost))
    
    # reverse order und verteilen auf zwei partitionen
    
    # Initialisierung
    s1=[v[len(v)-1]]     # ein wenig schräg, also das letzte Element als Liste speichern
    s2=[]    
    
    while (len(v) > 1):
        print ("v={}".format(v))
        t1 = v.pop()  #4 
        t2 = v.pop()  #1
        t3 = v.pop()  #5
        if (t1 in s1):
            i = s1.index(t1)   # bestimme Index vom Wert in Liste
            s1[i]=t3
            s2.append(t2)
        elif(t1 in s2):
            i = s2.index(t1)   # bestimme Index vom Wert in Liste
            s2[i]=t3
            s1.append(t2)
        else:
            print ("Fehler:")            
            print ("t1= {} t3={} < t2={}".format(t1,t3,t2))
            print ("v={}".format(v))
            break
        print ("=================================")
        print ("s1 = {}".format(s1))
        print ("s2 = {}".format(s2))
    p=[s1,s2]
    return (p, cost)
    
    

def print_best_partition(l, k):
    #simple function to partition a list and print info
    print ('    Partitioning {0} into {1} partitions'.format(l, k))
    p,cost = kk_list(l, k)
    print ('    Karmarkar-Karp Partitioning is {0}\n    and Cost {1}\n'.format(p, cost))

#tests
# l = [1, 6, 2, 3, 4, 1, 7, 6, 4]  # s1 = [4, 7, 6] ~ s2 = [1, 2, 1, 3, 4, 6], cost=0
# l = [18,17,12,11,8,2]            # s1 = [8, 11, 17] ~ s2 = [12, 18, 2], cost=4
# l = [1, 10, 10, 1]               # s1 = [1, 10] ~ s2 = [10, 1], cost=0
# l = [95, 15, 75, 25, 85, 5]      # s1 = [75, 85] ~ s2 = [5, 95, 15, 25], cost=20
l=[8,7,6,5,4]                    # s1 = [4, 5, 7] ~ s2 = [6, 8], cost=2
# l=[25,17,10,8,7,4]

import random
#l = [random.randint(0,20) for x in range(100)]
print_best_partition(l, 2)
 