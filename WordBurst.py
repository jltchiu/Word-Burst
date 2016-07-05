import string, sys, os, math, array, re, operator, argparse
from collections import defaultdict as dd
#
if len(sys.argv) != 7:
    print "Usage: Filename Net_Location Type Window_Size Stop% Penalty Output"
    sys.exit()
intime = float(sys.argv[3])
stoplist_size = float(sys.argv[4]) / 100.0
penalty = float(sys.argv[5])

#Tagalog_net_inputdir = sys.argv[1]
#Tagalog_net_inputdir = "C:\\Users\\jchiu1\\Desktop\\Site\\nets\\"
#Tagalog_net_inputdir = "nets1\\"
#ofile = open( "RescoringNet",'w')
ofile = open( sys.argv[6],'w')
#inputfiles = os.listdir(Tagalog_net_inputdir)
inputfiles = ["1"]
data = {}

type = sys.argv[2]
Cantonese_utt = "/home/jchiu1/BABEL/utterance/Cantonese-Limited-train.utt"
Pashto_utt = "/home/jchiu1/BABEL/utterance/Pashto-Limited-train.utt"
Tagalog_utt = "/home/jchiu1/BABEL/utterance/Tagalog-Limited-train.utt"
Turkish_utt = "/home/jchiu1/BABEL/utterance/Turkish-Limited-train.utt"

Cantonese_spk = "/home/jchiu1/BABEL/utterance/Cantonese.spklist"
Pashto_spk = "/home/jchiu1/BABEL/utterance/Pashto.spklist"
Tagalog_spk = "/home/jchiu1/BABEL/utterance/Tagalog.spklist"
Turkish_spk = "/home/jchiu1/BABEL/utterance/Turkish.spklist"


Cantonese_freq_flie = "/home/jchiu1/BABEL/freq/Cantonese-Limited_Train_Freq.txt"
Pashto_freq_flie = "/home/jchiu1/BABEL/freq/Pashto-Limited_Train_Freq.txt"
Tagalog_freq_flie = "/home/jchiu1/BABEL/freq/Tagalog-Limited_Train_Freq.txt"
Turkish_freq_flie = "/home/jchiu1/BABEL/freq/Turkish-Limited_Train_Freq.txt"

if type == "Cantonese":
    freq = open( Cantonese_freq_flie,'r')
#    spk = open( Cantonese_spk,'r')
#    utt = open( Cantonese_utt,'r')
elif type == "Pashto":
    freq = open( Pashto_freq_flie,'r')
#    spk = open( Pashto_spk,'r')
#    utt = open( Pashto_utt,'r')
elif type == "Tagalog":
    freq = open( Tagalog_freq_flie,'r')
#    spk = open( Tagalog_spk,'r')
#    utt = open( Tagalog_utt,'r')
elif type == "Turkish": 
    freq = open( Turkish_freq_flie,'r')
#    spk = open( Turkish_spk,'r')
#    utt = open( Turkish_utt,'r')
else:
    print "Wrong Language!"
    sys.exit()

    
#lines = spk.readlines()
#file_name = set()
#for l in lines:
#   file_name.add(l.replace("outLine","").replace("inLine","").strip())
#spk.close()

#train = dd(list)
#lines = utt.readlines()
#for l in lines:
#    token = l.replace('}','{').split("{")
#    do = 0
#    for t in token:
#        if "SPK" in t and "Line" in t:
#            tok = t.split()
#            speaker = tok[1].replace("outLine","").replace("inLine","")
#            if speaker in file_name:
#                do = 1
#        if "TEXT" in t:
#            #tok = t.split()
#            text = t.replace("TEXT","").strip()
#        if "FROM" in t:
#            start = float(t.replace("FROM","").strip())
#        if "TO" in t:
#            end = float(t.replace("TO","").strip())
#    if do == 1:
        #train[speaker] = train[speaker] + text + " "
#        train[speaker].append((start,end,text))
#utt.close()

#print train
#sys.exit()
#freq = open( sys.argv[2],'r')
lines = freq.readlines()
templist = []
stoplist = set()
penallist = set()
for l in lines:
    token = l.split()
    templist.append(token[0])
word_type = len(templist)
freqlist = dd(float)

x = float(word_type)
for l in templist:
    freqlist[l] = x
    x = x - 1.0
# original is / 50. now is * 2%
for i in range(int(len(templist) * stoplist_size)):
    stoplist.add(templist[i])
for i in range(int(10 * len(templist) * stoplist_size)):
    penallist.add(templist[i])

freq.close()
#print stoplist
'''
MI = dd(float)
train_freq = dd(float)
coocur = dd(float)
words = set()
total_token = 0.0
for k in train.keys():
    for i in train[k]:
        texti = i[2]
        fromi = i[0]
        toi = i[1]
        tokeni = texti.split()
        for ti in tokeni:
            train_freq[ti] = train_freq[ti] + 1
        total_token = total_token + len(tokeni)
        for j in train[k]:
            fromj = j[0]
            toj = j[1]
            textj = j[2]
            tokenj = textj.split()  
            if fromi == fromj:
                continue
            if fromj - toi > intime or fromj < fromi:
                continue
            for ti in tokeni:
                for tj in tokenj:
                    if ti in stoplist or tj in stoplist or ti[0] == "<" or tj[0] == "<":
                        continue
                    key = frozenset([ti,tj])
                    coocur[key] = coocur[key] + 1
                    words.add(key)
for k in words:
    lk = list(k)
    #there are two kinds of MI calculation, multiply, addition, now its addition, bottom one will be addition
    if len(lk) == 1:
        #MI[k] = math.log((coocur[k]* total_token)/(train_freq[lk[0]]*train_freq[lk[0]]),2)
        #MI[k] = math.log((2 * coocur[k])/(train_freq[lk[0]]+train_freq[lk[0]]),2)
        MI[k] = (2 * coocur[k])/(train_freq[lk[0]]+train_freq[lk[0]])
    elif len(lk) == 2:
        #MI[k] = math.log((coocur[k]* total_token)/(train_freq[lk[0]]*train_freq[lk[1]]),2)
        #MI[k] = math.log((2 * coocur[k])/(train_freq[lk[0]]+train_freq[lk[1]]),2)
        MI[k] = (2 * coocur[k])/(train_freq[lk[0]]+train_freq[lk[1]])
    else:
        print "something is wrong"
        sys.exit()
    #if MI[k] < 0:
    #print str(k) + ":" + str(MI[k])


'''


#print MI
#print cluster_index

#sys.exit()




#format {trim_filename:[realfilename, start time, end time, [[predict1][predict2]]],format}

    #ifile = open( Tagalog_net_inputdir + i,'r')
ifile = open( sys.argv[1],'r')
lines = ifile.readlines()
for l in lines:
    #print l
    token = l.split()
    filename = token[0]
    filenames = token[0].split("_")
#    trim_filename = filenames[3]+"_"+filenames[4]+"_"+filenames[5]#No in/outline
    trim_filename = filenames[3]+"_"+filenames[4]+"_"+filenames[5]+"_"+filenames[6]
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
        #print token[i]
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
            #print str(phase)
        #print str(predict)
        #print str(prob)
        #print str(third)
    if (data.has_key(trim_filename)):
        data[trim_filename].append([filename, starttime, endtime, predict, prob, third])
    else:
        data[trim_filename] = [[filename, starttime, endtime, predict, prob, third]]
ifile.close()


#Rescoring
#OOV= 0.0

flag = 0
counter = 0.0
thre = 0.1
for k in data.keys():
    counter = counter + 1.0
    total = len(data.keys())
    if counter/total > thre:
        print str(counter/total * 100) + "%"
        thre = thre + 0.1
    for d1 in data[k]:
        #print l
        #d1time = float(d1[1])
        predict = d1[3]
        time = d1[4][0]
        prob = d1[4][1]
        output = d1[4][2]
        #bonus = {}
        #I should do local bonus here
        for x in range(len(predict)):
            if len(predict) == 1:
                continue
            #if len(predict) >5:
            #    OOV = OOV + 1
            for y in range(len(predict[x])):
                if predict[x][y][0] == "<" or predict[x][y][0] == "@":
                    continue
                #if predict[x][y][0] == "@":
                #    continue
                if predict[x][y] in stoplist:
                    continue
                if len(predict[x]) == 1:
                    continue
#                if len(predict[x]) > 4: #simple OOV
 #                   #OOV = OOV + 1
 #                   output[x][y] = 0.01
 #                   continue #basically, destroy all node with 5 or more hyp

                self_time = time[x] #no y there cause all hypothesis share a x (bracelet) so same time with different y
                update_score = 0.0 #new score for predict[x][y], sum up andsave at output[x][y]
                burst = 0.0
                MIs = 0.0
#DEGUB
                if "30554_20120301_192050" in k and self_time == 264.81:
                    print "hello??"
                    flag = 1
                else:
                    flag = 0
                for d2 in data[k]:
                    #kill stoplist
                    #if predict[x][y] in stoplist:
                    #    break

                    predict2 = d2[3]
                    time2 = d2[4][0]
                    prob2 = d2[4][1]
                    #if prob2 < 0.2:
                    #    continue
                    
                    for x2 in range(len(predict2)):
                        for y2 in range(len(predict2[x2])):
                            #if len(predict2[x2]) != 1 and prob2[x2][y2] <0.5:
                            if prob2[x2][y2] <0.6:
                                break
                            self_time2 = time2[x2]
                            dis = abs(self_time - self_time2)
                            if self_time == self_time2 and x == x2 and y == y2:
                                continue
#                            if dis > intime or dis < 1:
                            if dis > intime:
                                continue
                            if self_time2 - self_time > 30:
                                break
                            #if abs(self_time2 - self_time) < 1:
                            #    continue
                            #print "in"
                            ratio = (1 - dis/intime)
#                            ratio = (1 - math.pow(dis/intime,2))
                            



                            #trapzoid
                            #if ratio > 2.0/3.0:
                            #    ratio = 1
                            #else:
                            #    ratio = ratio * 1.5
                            #print ratio
                            #print predict2
                            #print predict2[x]
                            #print x2
                            #print y2
#try mutual information here








#                            key = frozenset([predict2[x2][y2],predict[x][y]])
#                            if MI[key] != 0:
#                                update_score = update_score + ratio * prob2[x2][y2]
#                                burst = burst + ratio
                            #update_score = update_score + MI[key] * prob2[x2][y2]
                            #burst = burst + MI[key]
#                update_score = prob[x][y] + update_score * burst
                #update_score = prob[x][y] + update_score













#original
                            if predict2[x2][y2] == predict[x][y]:
#                            if predict2[x2][y2] == predict[x][y] and prob2[x2][y2] > (1.0-ratio):
                                #update_score = update_score + ratio * prob2[x2][y2]
                                update_score = update_score + ratio * prob2[x2][y2]



                                #update_score = update_score + ratio / prob2[x2][y2]
                                #print update_score
                                burst = burst + ratio
                                #print burst
                if flag == 1:
                    print burst
                update_score = prob[x][y] + update_score * math.exp(burst)
#                update_score = prob[x][y] + math.pow(update_score,1+burst)
#                            else:
#                                key = frozenset([predict2[x2][y2],predict[x][y]])
#                                update_score = update_score + MI[key] * prob2[x2][y2]
#                                MIs = MIs + MI[key]



#                key = frozenset([predict[x][y]])
#                if MI[key] == 0:
#                    burst = 0


#                update_score = prob[x][y] + update_score * burst





#                if predict[x][y] not in stoplist:
#                    update_score = prob[x][y] * ( 1 + burst )
#                else:
#                    update_score = prob[x][y]
#                update_score = prob[x][y] * ( 1 + burst )
#                update_score = prob[x][y] *  burst 










#                if MIs != 0:
#                    update_score = prob[x][y] + update_score * burst
#                else:
#                    update_score = prob[x][y]
                    #burst = 0









                #update_score = prob[x][y] + update_score
                #if predict[x][y] in idf.keys():
                    #update_score = update_score * idf[predict[x][y]]
                #update_score = prob[x][y] + update_score * burst * idf[predict[x][y]]
                #else:
                #    print "not in idf"
                    #update_score = update_score * math.log(docs)
                #    update_score = prob[x][y] + update_score * burst * math.log(docs)
                
                if burst == 0:
                    #update_score = update_score * 0.2
#                    if MIs == 0:
#                        update_score = update_score * penalty
#                    else:
#                        update_score = update_score
#                    update_score = update_score * (1 - freqlist[predict[x][y]]/word_type)
#                    if predict[x][y] not in penallist:
#                        update_score = update_score * penalty
                    if prob[x][y] < 0.5:
#                    if y != 0:
                        update_score = update_score * penalty
#                    update_score = update_score * penalty



                    #update_score = update_score / len(predict[x])
                    #update_score = 1 / len(predict[x])
                #update_score = max((prob[x][y] + update_score) * burst,prob[x][y])

                #if MIs == 0:
                #    update_score = update_score * penalty


                #update_score = update_score * MIs

                if update_score != prob[x][y]:
                    output[x][y] = update_score


#normalize the rescore, need to normalize the output score, so it's [4][2], I didn't change the name here.
    for d1 in data[k]:
        #print l
        predict = d1[3]
        prob = d1[4][2]
        for x in range(len(predict)):
            #if len(predict[x]) == 1:
            #    continue
            sum =0.0
            for y in range(len(predict[x])):
                sum = sum + prob[x][y]
#            for y in range(len(predict[x])):
#                prob[x][y] = prob[x][y] / sum

       #after take care of the file behind us, rescore the current one, if there is only one hypothesis, no need to rescore


#print OOV
#output
for k in data.keys():
    for d in data[k]:
        predict = d[3]
        prob = d[4][2] #updated probablility
        third = d[5]
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
