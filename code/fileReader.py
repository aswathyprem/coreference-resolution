
import sys,re


# This method reads the file into a data structure of the form dictionary_of_dictionary where it saves the document number as well as the line number

def fileReader(filename):

   # Read the contents of a file line-by-line and store them into a 'list' called 'file_data'
        print "Reading file: %s" % filename
        try:
                #dictionaries to save the document details and line details
                file_dict = {}
                col_dict={}
                col_list = []
                
                # counters to identify start and end of a document
                doc_count = 0
                line_count = 0
                flag = False

                #Start reading the file
                f = open(filename,'r')
                
                
                for line in f:
                        
                        # Initiatlize parameters at start and end of a document
                        if line.startswith('#begin'):
                            doc_count = doc_count + 1
                            line_count = line_count + 1
                            flag = True
                            continue
                        elif line.startswith('#end'):
                            # every time a document ends, add the line details to a dictionary and reset the dictionary
                            file_dict[doc_count] = col_dict
                            col_dict = {}
                            col_list = []
                            flag = False
                            line_count = 0
                        

                        # if document begin flag is true, increment line count 
                        # and append the columns as a list to the dictionary
                        if flag:
                            columns = line.split( )
                            if not columns:
                                line_count = line_count + 1
                                col_list = [] 
                            else:
                                col_list.append(columns)
                                col_dict[line_count] = col_list
                                                           
                         
                f.close()

        except Exception as e:
                print "\tError %s" % str(e.message)

        return file_dict

    
