# https://docs.python.org/3.4/tutorial/datastructures.html
# checked the above website to see how to append values in a dictionary without over-writing the previous values
import random

inp =[random.randint(1,6), random.randint(1,6), random.randint(1,6)]
print ('randomly generated input dice is :', inp)
dice = [1,2,3,4,5,6]
exp = {}

if inp[0] == inp[1] == inp[2]:
    exp['no roll, all same face value'] = 25
else:
    exp['no roll, max expected value achieved'] = inp[0]+inp[1]+inp[2]
    
total = 0
for i in dice:
    if i == inp[1] and i == inp[2]:
        total = total + 25
    else:
        total = total + i + inp[1] + inp[2]
exp['roll 1st dice'] = total/6.0

total = 0
for i in dice:
    if i == inp[0] and i == inp[2]:
        total = total + 25
    else:
        total = total + i + inp[0] + inp[2]
exp['roll 2nd dice'] = total/6.0

total = 0
for i in dice:
    if i == inp[0] and i == inp[1]:
        total = total + 25
    else:
        total = total + i + inp[0] + inp[1]
exp['roll 3rd dice'] = total/6.0

total = 0
for i in dice:
    for j in dice:
        if i  == inp[2] and j == inp[2]:
            total = total + 25
        else:
            total = total + i + j + inp[2]
exp['roll 1st and 2nd dice'] = total/36

total = 0
for i in dice:
    for j in dice:
        if i  == inp[1] and j == inp[1]:
            total = total + 25
        else:
            total = total + i + j + inp[1]
exp['roll 1st and 3rd dice'] = total/36

total = 0
for i in dice:
    for j in dice:
        if i  == inp[0] and j == inp[0]:
            total = total + 25
        else:
            total = total + i + j + inp[0]
exp['roll 2nd and 3rd dice'] = total/36

total = 0
for i in dice:
    for j in dice:
        for k in dice:
            if i == j and i == k:
                total = total + 25
            else:
                total = total + i + j + k
exp['roll all three dice'] = total/216

#print(exp)
print(max(exp, key=exp.get)) #https://artemrudenko.wordpress.com/2013/04/12/python-finding-a-key-of-dictionary-element-with-the-highestmin-value/