import math

#I have neither given nor received unauthorized aid on this program
def testfile(testf, headers, ham, spam, spammailcount, hammailcount, totalmail, allwords):
    with open(testf, 'r') as file:
        array = set()
        testcount = 0
        features = 0
        for line in file:
            line = line.rstrip()
            L = line.split(' ')
            #the line below is used to check if there's a new paragraph 
            if L[0] != "</BODY>":
                for word in L:
                    #Checks if word is a header or an empty space 
                    if word in headers or word == '':
                        continue 
                    elif word.lower() not in array:
                        word = word.lower()
                        array.add(word)
            else:
                spamprob = math.log(spammailcount/totalmail)
                hamprob = math.log(hammailcount/totalmail)
                for word in spam:
                    if word not in array:
                        spamprob += math.log((spammailcount - spam[word] + 1)/(spammailcount + 2))
                    else:
                        spamprob += math.log((spam[word] + 1)/(spammailcount + 2))

                for word in ham:
                    if word not in array:
                        hamprob += math.log((hammailcount - ham[word] + 1)/(hammailcount + 2)) 
                    else:
                        hamprob += math.log((ham[word] + 1)/(hammailcount + 2))
                        
                for word in array:
                    if word in allwords:
                        features += 1
                testcount += 1

                trueorfalse = "false"
                if "ham" in testf and hamprob > spamprob:
                    trueorfalse = "true"
                elif "spam" in testf and spamprob > hamprob:
                    trueorfalse = "true"
                    
                    
                print("TEST " + str(testcount) + " " + str(features) + "/"  + str(len(allwords)) + " "  + str(spamprob) + " " + str(hamprob) + " " +trueorfalse)
                spamprob = 0
                hamprob = 0
                features = 0
                array = set()

def main():

    trainspam = "train-spam.txt"
    trainham = "train-ham.txt"
    testspam = "test-spam.txt"
    testham = "test-ham.txt"

    spam = dict()
    ham = dict()
    spammailcount = 0
    hammailcount = 0
    newemail = True
    headers = ["<SUBJECT>", "<BODY>","</SUBJECT>", "</BODY>"]
    allwords = set()

    
    with open(trainspam, 'r') as file:
        array = set()
        for line in file:
            line = line.rstrip()
            L = line.split(' ')
            if L[0] != "</BODY>":
                for word in L:
                    if word in headers or word == '':
                        continue 
                    elif word.lower() not in array:
                        word = word.lower()
                        array.add(word)
                    if word.lower() not in allwords:
                        allwords.add(word)
            else:
                spammailcount += 1
                for word in array:
                    if word not in spam:
                        spam[word] = 1
                    else:
                        spam[word] = spam[word] + 1
                array = set()
                
    with open(trainham, 'r') as file:
        array = set() 
        for line in file:
            line = line.rstrip()
            L = line.split(' ')
            if L[0] != "</BODY>":
                for word in L:
                    if word in headers or word == '':
                        continue 
                    elif word.lower() not in array:
                        word = word.lower()
                        array.add(word)
                    if word.lower() not in allwords:
                        allwords.add(word)
            else:
                hammailcount += 1
                for word in array:
                    if word not in ham:
                        ham[word] = 1
                    else:
                        ham[word] = ham[word] + 1
                array = set()

    #Used to add the words with 0 probability to spam and ham dictionary
    for word in allwords:
        if word not in spam:
            spam[word] = 0
        if word not in ham:
            ham[word] = 0
            

    totalmail = spammailcount+ hammailcount
    testfile(testspam, headers, ham, spam, spammailcount, hammailcount, totalmail, allwords)
    testfile(testham, headers, ham, spam, spammailcount, hammailcount,totalmail, allwords)

     
                    
                    
main()
