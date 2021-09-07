def Read_Exceed(Input_File, Output_File):
    '''
    This function will take the output file from "Exceedance_Checker.ipynb" and store it into a list

    Inputs: Output_Max_File from Exceedance__Checker.ipynb. A text file, delimited with "!" exclamation marks containing UTMS, Conc-Count Values, and source group
       Column headers of the Output_Max_File: UTMs, Conc-Count, SrcGroup
       UTMs: UTM coordinates UTME and UTMN combined together into a single string, values joined by an underscore "_"
       Conc-Count: Column of integers counting the number of times each UTM coordinate exceeds the ESL level per year. The Column header here marks the ESL level. Ex: "1xESL", "2XESL"...
       SrcGroup: marks the source group associated with this file. 
    
    Outputs: LIST containing the contents of the Exceed File
    '''
    
    max_file_records = [] #create empty string to store the data from the input file
    with open(Input_File,"r") as file1:
        max_file_records = file1.readlines() #reads the contents into the list, separated by "\n" which denote new lines.
    return max_file_records


def String_to_Elements(contents):
    '''
    This function will take a string object (each element of the "contents" list), and split it out into its useable information 

    Inputs: A string, delimited with "!" exclamation marks containing UTMS, Conc-Count Values, and source group
       Column headers of the Output_Max_File: UTMs, Conc-Count, SrcGroup
       UTMs: UTM coordinates UTME and UTMN combined together into a single string, values joined by an underscore "_"
       Conc-Count: Column of integers counting the number of times each UTM coordinate exceeds the ESL level per year. The Column header here marks the ESL level. Ex: "1xESL", "2XESL"...
       SrcGroup: marks the source group associated with this file. 
       
       Example Input: '409446.0_3315779.0!0!ALL\n'
    
    Outputs: list of individual values for UTME, UTMN, CONC-COUNT, and Source Group.
        Example Output: [409446.0, 3315779.0, 0, ALL]
    '''
    #1) Replace the underscore with an exclamation mark. This returns a string
    #2) Remove the end-of-line "\n" marker. This returns a string
    #3) Split the string, using ! as delimiter, into a list of elements.
    
    values = contents.replace("_","!").strip("\n").split("!")
    return values

def Write_Output_MAXIFILE(vals, Output_File):
    '''
    This function will take a dictionary object, which uses line numbers as the key and line contents as values, and populates an output file from it

    Inputs: vals: a dictionary, keyed off of line numbers.
       
    Outputs: An output file in the format of AERMOD's MAXIFILE
        "   1 ALL      16010720  410135.86000 3316050.20000    4.66    4.66    0.00      20.54187"
    '''
    sourcegroup = vals[0][3]
    fmt1 = "   " #3 spaces
    fmt2 = "    " #4 spaces
    fmt3 = "        0.00     0.00     0.00       1     "# extra unnecessary info
    with open(Output_File,"w") as file2:
        file2.write("* AERMOD (21112 ) \n")
        file2.write("* MODELING OPTIONS USED:\n")
        file2.write("*  CONC  ELEV  ADJ_U*  RURAL  OPTIONS  MODELING  REGDFAULT  USED:\n")
        file2.write("*         EXCEEDANCE FILE FOR 1-HR VALUES >= A THRESHOLD OF 20.00 \n")
        file2.write("*         FOR A TOTAL OF 0 RECEPTORS.\n")
        file2.write("*         FORMAT: (1X,F13.5,1X,F13.5,1X,F13.5,1X,F8.2,1X,F8.2,1X,F8.2,1X,A6,1X,A8)\n")
        file2.write("*      X             Y         COUNT-CONC    ZELEV    ZHILL    ZFLAG    AVE     GRP  \n")
        file2.write("*_____________ _____________ _____________ ________ ________ ________ ______ ________\n")
        for i in range(len(vals)):
            file2.write(fmt1+vals[i][0]+fmt1*2+vals[i][1]+fmt2*2+vals[i][2]+fmt3+fmt1+vals[i][3]+'\n')

    return


#This set of functions will take the output from "Exceedance_Checker.ipynb" and create an exceedance.plt formatted file from it. 
# You'll have to go back and insert the header information.
Input_File = "Permitted_EO_Refined_1xESL.X01"
Output_File = "Permitted_EO_Refined_1xESL.PLT"
contents = Read_Exceed(Input_File,Output_File)
valDict = {}
for i, element in enumerate(contents[1:]):
    valDict[i] = String_to_Elements(element)
Write_Output_MAXIFILE(valDict, Output_File)    
