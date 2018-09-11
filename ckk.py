# -*- coding: utf-8 -*-
"""
Created on Sun Oct 22 19:45:01 2017

@author: arne
"""

# Karmarkar - Karp Algorithmus
# 
# dies ist ein Proof of Concept
#
# Es gibt zwei Funnktionen. 
#  1. Der eigentliche Karmarkar - Karp Algorithmus, bestehen aus zwei Phasen
#       Die erste Phase bestimme die maximale Differenz zw. zwei Partitionen
#           (a) Calculate Difference 
#           - {18, 17, 12, 11, 8, 2}
#           (18 − 17) → 1 {12, 11, 8, 2, 1} 
#           (12 − 11) → 1 {8, 2, 1, 1} 
#           (8 − 2) → 6 {6, 1, 1} 
#           (6 − 1) → 5 {5, 1} 
#           (5 − 1) → 4 {4} 
#
#       Die zweite Phase
#           (b) Generate Partition Action S 
#            Reverse Action    S1          S2
#            -                 {4}         {}
#              4 → (5 − 1)     {5}         {1}
#              5 → (6 − 1)     {6}         {1, 1}
#              6 → (8 − 2)     {8}         {2, 1, 1}
#              1 → (12 − 11)   {11, 8}     {12, 2, 1}
#              1 → (18 − 17)   {17, 11, 8} {18, 12, 2}
#
#        The upper bound is calculated as max {sum(S 1 ), sum(S 2 )} = max{36, 32} = 36.
#
# 2. Der Complete Karmarkar Karp (CKK) Algorithmus. 
#   Die Differentmethode findet nicht zwingend eine gute Lösung. Durch Addition
#   kann es sein, eine bessere Lösung zu finden. Der CKK berechnet den Baum 
#   auf Basis der Addition von den zwei größten Werten. 
#       Beispiel [4,5,6,7,8]
#       Karmarkar - Karp:  [4,5,7] und [6,8] mit Kosten von 2
#       CKK:               [4,5,6] und [7,8] mit Kosten von 0 

# Karmarkar-Karp Algorithmus
import bisect as b                 # Einsortieren in eine Liste

import os                          # os (für logging)
import json                        # json Struktur (für logging)
import logging.config              # Logging

# Logger Setup
def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'
):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)



def kk_list(l, k):
    # calculate difference
    a=list(l)                        
    a.sort()                            # sortiere die Liste nach der Größe
    cost = 100000                       # Kosten (d.h. Differenz nach dem ersten durchlauf
    v = []
    log.info ("Enter KK Algorithm")
    log.info ("="*120)
    while (len(a) > 1 ):
        log.debug ("a: old {}".format(a))
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
        log.debug ("a: new {}".format(a))
        log.debug ("cost = {}".format(cost))
        log.debug ("-"*120)
    log.info ("Created vector v={}".format(v))
    log.info ("Cost: {}".format(cost))
    
    # reverse order und verteilen auf zwei partitionen
    
    # Initialisierung
    s1=[v[len(v)-1]]     # ein wenig schräg, also das letzte Element als Liste speichern
    s2=[]    
    
    while (len(v) > 1):
        log.debug ("v={}".format(v))
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
            log.error ("Fehler:")            
            log.error ("t1= {} t3={} < t2={}".format(t1,t3,t2))
            log.error ("v={}".format(v))
            break
        log.info ("-"*120)
        log.info ("Created partition s1 = {}".format(s1))
        log.info ("Created partition s2 = {}".format(s2))
    p=[s1,s2]
    return (p, cost)

def ckk_list(l, k, min_cost):
    # calculate difference
    a=list(l)                        
    a.sort()                            # sortiere die Liste nach der Größe
    cost = 100000                       # Kosten (d.h. Differenz nach dem ersten durchlauf
    v = []
    log.info ("Enter CKK Algorithm")
    log.info ("="*120)
    while (len(a) > 1 ):
        log.debug ("a: old {}".format(a))
        t1 = a.pop()
        t2 = a.pop()
        v.append(t1)
        v.append(t2)                     
        z = t1 + t2
        v.append(z)
        b.insort(a,z)                       # sortiere z in die Liste ein
        #m.append(z)                        # Differenzwert speichern
        cost=max(a) - sum(a[0:(len(a)-1)])  # Differenz zw. Maximalwert und Rest
        log.debug ("a: new {}".format(a))
        log.debug ("cost = {}".format(cost))
        if (cost == 0):
            log.info ("Found Optimal Solution!")
            a.pop()   # den letzen Wert wieder vom Stack nehmen
            break
        elif (cost < min_cost and cost > 0):
            log.info ("Found a better Solution!")
            a.pop()
            break
        log.debug ("-"*120)
    log.info ("Created vector v={}".format(v))
    log.info ("Cost: {}".format(cost))
    
    # Initialisierung
    s1=[v[len(v)-1]]     # ein wenig schräg, also das letzte Element als Liste speichern
    s2=[]    
    
    while (len(v) > 1):
        log.debug ("v={}".format(v))
        t1 = v.pop()  #11 
        t2 = v.pop()  #6
        t3 = v.pop()  #5
        if (t1 in s1):
            i = s1.index(t1)   # bestimme Index vom Wert in Liste
            s1[i]=t2
            s1.append(t3)
        elif(t1 in s2):
            i = s2.index(t1)   # bestimme Index vom Wert in Liste
            s2[i]=t2
            s2.append(t3)
        else:
            log.error ("Fehler:")            
            log.error ("t1= {} t3={} < t2={}".format(t1,t3,t2))
            log.error ("v={}".format(v))
            break
        log.debug ("=================================")
        if (sum(s1)+sum(a)+cost == sum(s2)):
            s1 = s1+a
        else:
            s2 = s2+a
        log.info ("Created partition s1 = {}".format(s1))
        log.info ("Created partition s2 = {}".format(s2))        
    p=[s1,s2]
    return (p, cost)
   
    

def print_best_partition(l, k):
    #simple function to partition a list and print info
    print ("*"*120)
    print ('    Partitioning {0} into {1} partitions'.format(l, k))
    kkp,kkcost = kk_list(l, k)
    ckkp,ckkcost = ckk_list(l,k, kkcost)
    if ckkcost < kkcost:
        p=ckkp
        cost=ckkcost
    else:
        p=kkp
        cost=kkcost
    print ('    Karmarkar-Karp Partitioning is {0}\n    and Cost {1}\n'.format(p, cost))


# ************************************************************************
# main()
# ************************************************************************
setup_logging()
log = logging.getLogger(__name__)

#tests
# l = [1, 6, 2, 3, 4, 1, 7, 6, 4]  # s1 = [4, 7, 6] ~ s2 = [1, 2, 1, 3, 4, 6], cost=0
# l = [18,17,12,11,8,2]            # s1 = [8, 11, 17] ~ s2 = [12, 18, 2], cost=4
# l = [1, 10, 10, 1]               # s1 = [1, 10] ~ s2 = [10, 1], cost=0
# l = [95, 15, 75, 25, 85, 5]      # s1 = [75, 85] ~ s2 = [5, 95, 15, 25], cost=20
#l=[8,7,6,5,4]                    # s1 = [4, 5, 7] ~ s2 = [6, 8], cost=2
l=[22,21,20,10,10,10,10,10,10,3]
# l=[25,17,10,8,7,4]
# l=[205,157,133,111,100,91,88,59,47,23]
# l = [10,5,3,2]
# l=[6,5,4,4,3]
#import random
#l = [random.randint(0,20) for x in range(100)]
print_best_partition(l, 2)
 