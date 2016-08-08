import re,sys
import fileReader
import markablesExtract

# Method to extract training examples
def extractTrain(coref_dict):
    NP_positive = []
    NP_negative = []
    for i in range(len(coref_dict)):
        flag = 0
        counter = 0
        for j in range(len(coref_dict[i+1])):
            for k in range(len(coref_dict[i+1][j+1])):
                NP_coref = coref_dict[i+1][j+1][k]
                if NP_coref[1] != None and flag == 0:
                    NP = NP_coref[0]
                    temp = NP_coref[1]
                    flag = 1
                elif NP_coref[1] == None and flag !=0:
                    counter = counter + 1
                elif NP_coref[1] !=None and flag !=0:
                    if set(NP_coref[1]) & set(temp):
                        flag = 0
                        NP_positive.append((NP,NP_coref[0]))
                    else:
                        NP_negative.append((NP,NP_coref[0]))
    print "NP - Positive"
    print NP_positive   
    
    print "NP - Negative"
    print NP_negative 
    
                
                        
                        
                    
                    



if __name__ == "__main__":
    sys.stdout = open('file.log','w')

    x = fileReader.fileReader('/home/users0/veluthay/2Semester/Coreference/programming-exercise/data/temp.conll')
    y = markablesExtract.getMarkables(x)
    extractTrain(y)
