import string, sys, os, math, array, re, operator, argparse
from collections import defaultdict as dd
def average(s): return sum(s) * 1.0 / len(s)
#
if len(sys.argv) != 4:
    print "Usage: Filename Net_Location Penalty Output"
    sys.exit()
penalty = float(sys.argv[2])

ofile = open( sys.argv[3],'w')
inputfiles = ["1"]
data = {}

penalty_dic = dd(float)
retrain = dd(list)
score = dd(list)
hyp = dd(list)
print "Loading Data..."
ifile = open( sys.argv[1],'r')
lines = ifile.readlines()
for l in lines:
    #hyp = dd(list)
    token = l.split()
    filename = token[0]
    filenames = token[0].split("_")
    trim_filename = filenames[3]+"_"+filenames[4]+"_"+filenames[5]#No in/outline
    starttime = float(token[1])
    endtime = float(token[2])
    predict = []
    multpredict = []
    prob = [[],[],[]] # [[time],[original score],[output score]]
    multprob = []
    third = []
    multthird = []
    layer = 0
    phase = 0
    for i in range(3,len(token)):
        if layer == 0:
            phase = phase + 1
        if layer == 1 and phase == 1 and token[i] != "{" and token[i] != "}":
            predict.append([token[i]])
        if layer == 2 and phase == 1 and token[i] != "}":
            multpredict.append(token[i])
        if layer == 2 and phase == 1 and token[i] == "}":
            if len(multpredict) > 0:
                predict.append(multpredict)
                multpredict = []

        if layer == 1 and phase == 2 and token[i] != "{" and token[i] != "}":
            prob[1].append([float(token[i])])
            prob[2].append([float(token[i])])
        if layer == 2 and phase == 2 and token[i] != "}":
            multprob.append(float(token[i]))
        if layer == 2 and phase == 2 and token[i] == "}":
            if len(multprob) > 0:
                prob[1].append(list(multprob))
                prob[2].append(list(multprob))
                multprob = []

        if layer == 1 and phase == 3 and token[i][0] != "{" and token[i] != "}":
            third.append([token[i]])
        if layer == 1 and phase == 3 and token[i][0] == "{":
            multthird.append(token[i][1:])
        if layer == 2 and phase == 3 and token[i][-1] == "}":
            multthird.append(token[i][:-1])
            if len(multthird) > 0:
                third.append(multthird)
                #Try to match between the list 3 and list 2, add time information
                prob[0].append(float(multthird[1])/100.0 + starttime)
            multthird = []
        if layer == 2 and phase == 3 and token[i] != "}" and token[i][-1] != "}":
            multthird.append(token[i])
        
        if  "{" in token[i]:
            layer = layer + 1
        elif "}" in token[i]:
            layer = layer - 1
    if (data.has_key(trim_filename)):
        data[trim_filename].append([filename, starttime, endtime, predict, prob, third])
    else:
        data[trim_filename] = [[filename, starttime, endtime, predict, prob, third]]
    count = 0.0
    all = 0.0
    score = []
    below = [] # all the score that below threshold, use to decide penalty
    above = []
    #for l in ref[trim_filename]:
    #    if abs(l[0]-starttime) < 1:
    #        truth = l[1]
    #        for p in predict
    for x in prob[1]:
        #print x
        for y in x:
            count = count + 1
            all = all + float(y)
            score.append(float(y))
        #print count
        #print sum
    #score.sort()
#    score = sorted(score)
#    score.reverse()

    #print sorted(score)
#    print score
    avg = all/count

    count = 0.0
    all = 0.0
    score = sorted(score)
    score.reverse()
    for i in range(len(score)/2):
        #print len(score)/4
        count = count + 1.0
        all = all + score[i]
    #print score
    #print all
    #print count
    if count == 0:
        highavg = score[0]
    else:
        highavg = all/count
    count = 0.0
    all = 0.0
    for x in prob[1]:
        #print x
        for y in x:
            if float(y) <= avg:
                count = count + 1
                all = all + float(y)
                below.append(float(y))

    lowavg = all/count
    #std = numpy.std(score)
    threshold = highavg
    sentence = []
    #print sum/count
    for x in range(len(predict)):
        if prob[1][x][0] > threshold:
            sentence.append(predict[x][0])
    retrain[trim_filename].append(sentence)



    
    #count = 0.0
    #all = 0.0
    #score = []
    #below = [] # all the score that below threshold, use to decide penalty
    #above = []
    #for l in ref[trim_filename]:
    #    if abs(l[0]-starttime) < 1:
    #        truth = l[1]
    #        for p in predict
'''    
    for x in range(len(prob[1])):
        #print x
        for y in range(len(prob[1][x])):
            #count = count + 1
            #all = all + float(y)
            score[trim_filename].append(float(prob[1][x][y]))
            hyp[trim_filename].append(predict[x][y])
    #print len(hyp[trim_filename])
    #print len(score[trim_filename])

for k in score.keys():
    high = []
    s = sorted(score[k])
    s.reverse()
    #print s
    #sys.exit()
    for i in range(len(s)/2):
        #print len(score)/4
#        count = count + 1.0
#        all = all + score[i]
        high.append(s[i])
    avg = sum(high) * 1.0 / len(high)
    for i in range(len(score[k])):
        if score[k][i] > avg:
            retrain[k].append(hyp[k][i])
'''
ifile.close()
print "Loading Data Complete..."
all = 0.0
nohit = 0.0
counter = 0.0
thre = 0.1
for k in data.keys():

    train_freq = dd(float)
    words = set()
    total_token = 0
    for sent in retrain[k]:
        tmp = set()
        for idx1, word1 in enumerate(sent):
            if word1 == "@" or word1[0] == "<":
                continue
            train_freq[word1] = train_freq[word1] + 1
#    for q in sorted_MI:
    #for q in sorted_idf:
#        print q, MI[q]
    #    print q, idf[q] 
    #    cc = cc + 1
        #if cc == 100:
        #    break
    #print sorted_MI
    #sys.exit()
    counter = counter + 1.0
    total = len(data.keys())
    if counter/total > thre:
        print str(counter/total * 100) + "%"
        thre = thre + 0.1
    for d1 in data[k]:
        predict = d1[3]
        time = d1[4][0]
        prob = d1[4][1]
        output = d1[4][2]

        for x in range(len(predict)):
            if len(predict) == 1:
                continue
            for y in range(len(predict[x])):
                if predict[x][y][0] == "<" or predict[x][y][0] == "@":
                    continue
#                if predict[x][y] in stoplist:
#                    continue
                if len(predict[x]) == 1:
                    continue
                all = all + 1
                if train_freq[predict[x][y]] == 0: #penalty
                    #penalty_dic[trim_filename] = (avg,min(score))
                    #output[x][y] = prob[x][y] * penalty
                    #output[x][y] = prob[x][y] * penalty_dic[k] #the new penlaty here...
                    #if penalty_dic[k][0] == penalty_dic[k][1]:
                    #    nohit = nohit + 1
                    #    continue

                    #output[x][y] = prob[x][y] * ( 1 - (abs(prob[x][y] - penalty_dic[k][0])/(penalty_dic[k][0]-penalty_dic[k][1])))
                    #output[x][y] = prob[x][y] *  (abs(prob[x][y] - penalty_dic[k][0])/(penalty_dic[k][0]-penalty_dic[k][1]))
                    #output[x][y] = prob[x][y] * 0.25
                    output[x][y] = prob[x][y] * penalty
                    #output[x][y] = prob[x][y] * prob[x][y]
                    #output[x][y] = max(prob[x][y] -0.5, 0.01)
                    #output[x][y] = prob[x][y] - penalty_dic[k]
                    nohit = nohit + 1
                    continue
                #else:
                #    if penalty_dic[k][0] == penalty_dic[k][1]:
                #        continue
                #    output[x][y] = prob[x][y] * ( 1 + (prob[x][y]-penalty_dic[k][0])/(1-penalty_dic[k][0]))
print (all-nohit)/all
print nohit
print all
print "Outputing..."
#output
for k in data.keys():
    for d in data[k]:
        predict = d[3]
        prob = d[4][2] #updated probablility
        third = d[5]
        #print d[0]
        #print d[1]
        #print d[2]
        ofile.write(d[0] + " " + str(round(float(d[1]),2)) + " " + str(round(float(d[2]),2)))
        ofile.write(" { ")
        for p in predict:
            if len(p) == 1:
                ofile.write(p[0] + " ")
            else:
                ofile.write("{ ")
                for mp in p:
                    ofile.write( mp + " ")
                ofile.write("} ")
        ofile.write("} { ")
        for p in prob:
            if len(p) == 1:
                ofile.write(str('%.3f' % p[0]) + " ")
            else:
                ofile.write("{ ")
                for mp in p:
                    ofile.write( str('%.3f' % mp) + " ")
                ofile.write("} ")
        ofile.write("} { ")
        for t in third:
            if len(t) == 1:
                ofile.write(t[0] + " ")
            else:
                ofile.write("{")
                for mt in t:
                    ofile.write(mt)
                    if mt != t[-1]:
                        ofile.write(" ")
                ofile.write("} ")
        ofile.write("}\n")
ofile.close()
print "Output Complete"
