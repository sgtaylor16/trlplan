"""
Takes the json file and createsa a flat file of Name, Parent,UID that
d3.stratify reads in.
"""
import json
import pandas as pd

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#Files
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Path to read in input
jsonfile = r"C:\Users\sgtay\Documents\Git\JavaScript\trlplan\bliskplan.json"
# Path to write to for file that is used by javascript to create dendograph
dendographfile = r"C:/Users/sgtay/Documents/Git/JavaScript/trlplan/test2.csv"
# Path to write out for file that is used by javascript to create parallel plot
parallelfile = "continuous.csv"



with open(jsonfile,"r") as fh:
    mystring = fh.read().replace('\n', '')
    inpython = json.loads(mystring)

    
nodes = inpython['Nodes']

with open(dendographfile,"w") as fh:
    fh.write("Name,Parent,UID\n")
    for i,nodeob in enumerate(nodes):
        name = nodeob['Name']
        parent = nodeob["Parent"]
        value = nodeob['UID']
        if parent == 'None':
            fh.write(name + ',' + ','+str(value)+ '\n')
        else:
            fh.write(name + ',' + parent + ','+ str(value)+ '\n')


nodes = inpython["Nodes"]
tests = inpython["Tests"]

#Create the parallel plot df without the problems
testdf = pd.DataFrame(columns = ["Test","Cost","TestDate"])
for test in tests:
    testdf = testdf.append([{"Test":test["Name"],"Cost":test["Cost"],"TestDate":test["TestDate"]}])
    

df = pd.DataFrame(columns = ["Problem","Test","UID"])
for node in nodes:
    try:
         testlist = node["Tests"]
         for test in testlist:
             df = df.append([{"Problem":node["Name"], "Test":test,"UID":str(node["UID"]).replace(".0","")}])
    except KeyError:
        continue


bothdf = pd.merge(df,testdf,left_on = "Test",right_on = "Test",how = "left")
bothdf = bothdf.drop(["Problem"],axis =1)
bothdf = bothdf[['UID','Test','Cost','TestDate']]

bothdf.to_csv(parallelfile,index = False)