# -*- coding: utf-8 -*-
"""
Created on Fri Oct 19 03:25:07 2018

@author: Ayush-PC
"""
import sys
import re
import math

#data = train.read()
city_d = {}

train = open("C:\\Users\\Ayush\\Desktop\\Assignments\\AI\\Assignment 2\\geolocation\\tweets.train.txt","r", encoding="utf-8", errors='ignore')
traindata = train.read()    
traindata = traindata.split('\n')
test = open('C:\\Users\\Ayush\\Desktop\\Assignments\\AI\\Assignment 2\\geolocation\\tweets.test1.txt','r', encoding='utf-8', errors='ignore')
testdata = test.read()
testdata = testdata.split('\n')

trainlist = []
trainlist_tweet = []
testlist = []
testlist_tweet = []

for line in traindata:
    trainlist.append(line.split(' ', 1))
for line in testdata:
    testlist.append(line.split(' ', 1))

trainlist = [x for x in trainlist if x != [''] and x != []]
testlist = [x for x in testlist if x != [''] and x != []]

#####################################################
def get_tweet(tweet):
    return [word_qwe.lower() for word_qwe in re.split(r"[\W_]",tweet) if word_qwe!= '']
#  if tweet != '':
#      for tweet in re.split(r"[\W]", tweet):
#          tweet.lower()
#####################################################
    
for each in trainlist: 
    if len(each)==2:
      trainlist_tweet.append(get_tweet(each[1]))
      
for each in testlist: 
    if len(each)==2:
      testlist_tweet.append(get_tweet(each[1]))
#for each in testlist: 
#    if len(each)==2:
#      testlist_tweet.append(get_tweet(each[1]))
      
stopwords = set(['all', 'just', 'being', 'over', 'both', 'through', 'yourselves', 'its', 'before', 'herself', 'had', 'should', 'to', 'only', 'under', 'ours', 'has', 'do', 'them', 'his', 'very', 'they', 'not', 'during', 'now', 'him', 'nor', 'did', 'this', 'she', 'each', 'further', 'where', 'few', 'because', 'doing', 'some', 'are', 'our', 'ourselves', 'out', 'what', 'for', 'while', 'does', 'above', 'between', 't', 'be', 'we', 'who', 'were', 'here', 'hers', 'by', 'on', 'about', 'of', 'against', 's', 'or', 'own', 'into', 'yourself', 'down', 'your', 'from', 'her', 'their', 'there', 'been', 'whom', 'too', 'themselves', 'was', 'until', 'more', 'himself', 'that', 'but', 'don', 'with', 'than', 'those', 'he', 'me', 'myself', 'these', 'up', 'will', 'below', 'can', 'theirs', 'my','and', 'then', 'is', 'am', 'it', 'an', 'as', 'itself', 'at', 'have', 'in', 'any', 'if', 'again', 'no', 'when', 'same', 'how', 'other', 'which', 'you', 'after', 'most', 'such', 'why', 'a', 'off', 'i', 'yours', 'so', 'the', 'having', 'once', 'us', 'yes', 'its', 'mine', 'her'])

#trainlist_tweet = [j for sub in trainlist_tweet for j in sub] #https://stackoverflow.com/questions/29244286/how-to-flatten-a-2d-list-to-1d-without-using-numpy
#trainlist_tweet = [i for i in trainlist_tweet if i != '']

#remove stopwords
i = 0
while i < len(trainlist_tweet):
    j = 0
    for sab in trainlist_tweet[i]:
        if sab not in stopwords:
            trainlist_tweet[i][j] = sab
            j = j + 1
    del trainlist_tweet[i][j:]
    i =i + 1

while i < len(testlist_tweet):
    j = 0
    for sab in testlist_tweet[i]:
        if sab not in stopwords:
            testlist_tweet[i][j] = sab
            j = j + 1
    del testlist_tweet[i][j:]
    i =i + 1
#for i in trainlist_tweet[:]:
#    if i in stopwor8ds:
#        trainlist_tweet.remove(i)

#print(trainlist_tweet)

#city1: word1, word2, word3......
citydir = {}
i=0
for each in trainlist:
  if len(each) == 2:
    if each[0] not in citydir.keys():
      citydir[each[0]]= trainlist_tweet[i]
    else:
      citydir[each[0]]+=trainlist_tweet[i]
    i=i+1

#word1: {city1: count1, city2: count2.....}
worddir = {}
for allline in trainlist:
    for word in allline:
        worddir[word] = {}

for allline in testlist_tweet:
  for words in allline:
   if words not in worddir.keys():
    worddir[words] = {}
    
for allword in worddir.keys():
    for allcity in citydir.keys():
        worddir[allword][allcity] = worddir[allword][allcity] + 1
        
for allcity in citydir.keys():
    print(citydir.keys())
    for allword in citydir[allcity]:
        worddir[allword][allcity] = worddir[allword][allcity] + 1
        
        
        
#number of tweets from a city/total number of tweets
nooftweetfromcity = {}

for i in range(len(trainlist)):
    a = trainlist[i][0]
    if a not in nooftweetfromcity:
        nooftweetfromcity[a] = 1
    else:
        nooftweetfromcity[a] =nooftweetfromcity[a] + 1
        
length_train_tweet = len(trainlist_tweet)
for a in nooftweetfromcity.keys():
    nooftweetfromcity[a] = -math.log(float(float(nooftweetfromcity[a])/float(len(trainlist_tweet))))
    
#word1: {city1: conditional prob1, city2: conditional prob2....}
prob_c = {}
for allword in worddir.keys():
  prob_c[allword]={}
  for allcity in citydir.keys():
      prob_c[allword][allcity]={}
        
for allword in worddir.keys():
  for allcity in citydir.keys():
    if worddir[allword][allcity]==0:
      prob1 = -math.log(float((0+1)/float((len(worddir)+len(citydir[allcity])))))
    else:
      prob1 = -math.log(float((worddir[allword][allcity]+1)/float((len(worddir)+len(citydir[allcity])))))
    prob_c[allword][allcity] = prob1
    
#P(city/word). Taken -ve log as it is easy to compute
citylist = []
for i in range(len(testlist_tweet)):
    x = sys.maxsize
    for allcity in citydir.keys():
        value1 = 0.0
        for allword in testlist_tweet[i]:
            value1 = value1 + (prob1)
        total = value1 + (nooftweetfromcity[allcity])
        if total < x:
            city = allcity
    citylist.append(city)
    
#output file
out_file = open('C:\\Users\\Ayush\\Desktop\\Assignments\\AI\\Assignment 2\\geolocation\\output.txt','w')
i = 0
c = ''
correctness = 0.0
for i in range (len(testlist_tweet)):
    a = citylist[i]
    b = testlist[i][0]
    c = testlist_tweet[i][1:]
    x = str(a) + '' + str(b) + '' + str(c)
    out_file.write(x)
    if a == b:
        correctness = correctness + 1
    i = i + 1
print((correctness/len(testlist_tweet))*100)

#top 5 words associated with each city
topwords = {}
for allcity in citydir.keys():
    i = 0
    topwords[allcity] = []
    value1