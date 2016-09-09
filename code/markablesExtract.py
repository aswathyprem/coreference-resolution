#!/usr/bin/env python
# -*- coding: utf-8 -*-
import re
import fileReader
from nltk.tree import *

#This method extracts noun phrases and corresponding co-reference markings from the new data structure
def getMarkables(file_dict):
    try:
	# Initialize dictionaries to store data
        doc_dict = {}
        sent_dict = {}   
        #o = open('/home/users0/veluthay/2Semester/Coreference/programming-exercise/code/output/markables.txt','w')    
	# Start reading the data from file_dict
        for i in range(len(file_dict)):
	    # store document id in a variable
            document = i+1
            sent_dict = []
	    # Iterate through each sentence
            for j in range(len(file_dict[i+1])):
		# Store sentence id in a variable
                sentence = j+1
                list_of_list = file_dict[i+1][j+1]
		# Initialize lists to store corresponding values
		# for each sentence
                tokens = []
                pos = []
                parses = []
                coref = []
				
		# Iterate through each line and append 
		# the values to corresponding lists
                for k in range(len(list_of_list)):
                    word_list = list_of_list[k]
                    tokens.append(word_list[3])
                    pos.append(word_list[4])
                    parses.append(word_list[5])
                    coref.append(word_list[-1])
                
                parse_list = []
				
        	# Create a pattern to compare the presence 
		# of stars in the parses
                pattern1 = re.compile('.*\*.*')
				
		# Iterate through parses and replace 
		# the stars with leaf nodes of the tree (tokens).
                for l in range(len(parses)):
                    if pattern1.match(parses[l]):
                        parse_list.append(parses[l].replace('*', ' '+tokens[l]))
                parse_tree = ''.join(parse_list)      
				
		# call extractNP function to extract 
		# noun phrases from the joined parse trees
                NP = extractNP(Tree.fromstring(parse_tree))              
				
		# call matchCoref function to extract
		# the coreferences for the NPs
                NP_coref =  matchCoref(NP, tokens, coref)
				
		# Add the list of coreferences for each 
		# sentence to a dictionary with sentence id as key
                #sent_dict[sentence] = NP_coref
                sent_dict = sent_dict + NP_coref
				
        	# Add the list of coreferences for all the sentences 
	        # in one document to a dictionary with document id as key
            doc_dict[document] = sent_dict
            
        return doc_dict
                                        
    except Exception as e:
        print "\tError %s" % str(e.message)


#Method to extract noun phrases from the parse trees.    
def extractNP(parseTree):
    myPhrases = []
    if (parseTree.label()== 'NP'):
        #print parseTree.leaves()
        myPhrases.append( parseTree.copy(True) )
    for child in parseTree:
        if (type(child) is Tree):
            list_of_phrases = extractNP(child)
            if (len(list_of_phrases) > 0):
                myPhrases.extend(list_of_phrases)
    return myPhrases



#Method to extract the coreference ids for each noun phrase
def matchCoref(NP, tokens, coref):
    NP_coref = []
    for phrases in NP:
        NP_tokens = phrases.leaves()
        coref_final = None
        for m in range(len(tokens)):
            stack = []
            if NP_tokens[0] == tokens[m] and coref[m] != '-':
                temp_coref = coref[m].replace('(',' ').replace('|',' ').replace(')',' ')
                temp_coref = filter(None,temp_coref.strip().split(' '))
                stack.append(list(temp_coref))
                if len(NP_tokens) == 0:
                    break
                else:
                    m = m + len(NP_tokens) - 1
                    if len(tokens) > m and  NP_tokens[-1] == tokens[m] and coref[m] != '-':
                        temp_coref = coref[m].replace('(',' ').replace('|',' ').replace(')',' ')
                        temp_coref = filter(None, temp_coref.strip().split(' '))
                        stack.append(list(temp_coref))
                        coref_final = list(set(stack[0]) & set(stack[1]))
                        break

        NP_string = " ".join(NP_tokens)
        NP_coref.append([NP_string,coref_final])
    return NP_coref
