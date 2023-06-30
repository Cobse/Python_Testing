import pandas as pd

#df=pd.read_csv(r"Encoding_issues/ElementTypeArmering.csv",header=0, encoding="utf-8")
df=pd.read_csv(r"Encoding_issues/ElementTypeArmering.csv",header=0)

#print(df)
# control of unique values
#df_Test=df.drop(columns='Type')
df_Test=df
# # Find unique values and count number of occurances
df_Test['Type2']=df_Test.groupby(['Type','Design section','D10xx','D11xx','D12xx','D14xx','D13xx','D20xx','D15xx L1','D15xx L2','D30xx K1','R K1','D30xx K2','R K2','D30xx MID','R MID'],sort=False).ngroup()+1
df_Test['Type2']='BET'+df_Test['Type2'].astype(str)
df_Test['Count']=df_Test.groupby(['Type2'])['Type2'].transform('count')
df_Test2=df_Test.drop_duplicates()

df_arm=df.drop_duplicates()
df_arm.drop(columns='Design section')
print(df_arm)

# df.to_excel("ElementArmeringFullList.xlsx")
# df_Test.to_excel("ElementArmeringFullList_TEST.xlsx")
# df_Test2.to_excel("ElementArmeringFullList_TEST2.xlsx")
# df_arm.to_excel("ElementType_Armering.xlsx")
df_arm.to_excel("WALTER_ElementType_Armering_TESTTEST.xlsx")
