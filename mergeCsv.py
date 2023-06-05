import os
import pandas as pd 
from pandas_ods_reader import read_ods


def mergeCsvCurrDir(filename="mergedDataCurrDir.csv"):
    res=[]
    for file in os.listdir():
        if file.endswith(".csv"):
            res.append(pd.read_csv(file))
        elif file.endswith(".xlsx") or file.endswith(".xls"):
            res.append(pd.read_excel(file))
        elif file.endswith(".ods"):
            res.append(read_ods(file))
    
    resFile=pd.concat(res,axis=0,ignore_index=True)

    resFile.to_csv(filename)

def mergeCsvMultDir(filename="mergedDataMultDirs.csv"):
    res=[]

    for dir in os.listdir():
        if len (dir.split("."))==1:
            for file in os.listdir(dir):
                path="{}/{}".format(dir,file)
                if file.endswith(".csv",):
                    res.append(pd.read_csv(path))
                elif file.endswith(".xlsx"):
                    res.append(pd.read_excel(path))
                elif file.endswith(".xls"):
                    res.append(pd.read_excel(path))
                elif file.endswith(".ods"):
                    res.append(read_ods(path))

    resFile=pd.concat(res,axis=0,ignore_index=True)
    resFile.drop_duplicates(keep="last")

    resFile.to_csv(filename)




def mergeAll(filename="mergedData.csv"):
    res=[]

    for dir in os.listdir():
        if dir.endswith(".csv"):
            res.append(pd.read_csv(dir))
        elif dir.endswith(".xlxx") or dir.endswith(".xls"):
            res.append(pd.read_excel(dir))
        elif dir.endswith(".ods"):
            res.append(read_ods(dir))
        elif len (dir.split("."))==1:
            for file in os.listdir(dir):
                path="{}/{}".format(dir,file)
                if file.endswith(".csv"):
                    res.append(pd.read_csv(file,on_bad_lines="skip"))
                elif file.endswith(".xlxx") or dir.endswith(".xls"):
                    res.append(pd.read_excel(file))
                elif file.endswith(".ods"):
                    res.append(read_ods(file))
        
        resFile=pd.concat(res,axis=0,ignore_index=True)
        resFile.drop_duplicates(keep="last")

        resFile.to_csv(filename)

        


def mergeAllOnKey(key,filename):
    res=[]

    for dir in os.listdir():
        if dir.endswith(".csv"):
            res.append(pd.read_csv(dir))
        elif dir.endswith(".xlxx") or dir.endswith(".xls"):
            res.append(pd.read_excel(dir))
        elif dir.endswith(".ods"):
            res.append(read_ods(dir))
        elif len (dir.split("."))==1:
            for file in os.listdir(dir):
                path="{}/{}".format(dir,file)
                if file.endswith(".csv"):
                    res.append(pd.read_csv(file,on_bad_lines="skip"))
                elif file.endswith(".xlxx") or dir.endswith(".xls"):
                    res.append(pd.read_excel(file))
                elif file.endswith(".ods"):
                    res.append(read_ods(file))
        
        resFile=pd.merge(res)

        resFile.to_csv(filename)


mergeCsvMultDir()