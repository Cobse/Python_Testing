import pandas as pd

df_ULS2 = pd.read_excel('C:/Users/ermd/OneDrive - COWI/Ferjefri E39/Bjørnefjorden/Resultater GAM/forces_results_BJF_FEED_stage_1_pier.xlsx', sheet_name = 'ULS 2 Envelopes')
df_ULS3 = pd.read_excel('C:/Users/ermd/OneDrive - COWI/Ferjefri E39/Bjørnefjorden/Resultater GAM/forces_results_BJF_FEED_stage_1_pier.xlsx', sheet_name = 'ULS 3 Envelopes')

#FKJN sine stier, kommenteres bort 
df_ULS2 = pd.read_excel(r'Bjørnafjorden\forces_results_BJF_FEED_stage_1_pier.xlsx', sheet_name = 'ULS 2 Envelopes')
df_ULS3 = pd.read_excel(r'Bjørnafjorden\forces_results_BJF_FEED_stage_1_pier.xlsx', sheet_name = 'ULS 3 Envelopes')
 
results_dict = {}
 
def test(df_input):
    #print(df_input)
    df_dict = {}
    
    for pier in ['pier_1','pier_2','pier_3','pier_4']:
        rad_nummer = df_input.loc[(df_input['Unnamed: 0'] == pier)].index.values.astype(int)[0]        
        df = df_input.loc[rad_nummer : rad_nummer + 7, : ]
        df = df.reset_index(drop = 'True')
 
        levels = [df.loc[0,'case']]
        for z in range(1, len(df.index), 2 ):
            levels.append(df.loc[z,'case'])
        
        temp_dict = {}
        for i in levels:        
            rad_nummer2 = df.loc[(df['case'] == i)].index.values.astype(int)[0]        
            df3 = pd.DataFrame()
            for x in range(12):        
                df2 = df.iloc[rad_nummer2:(rad_nummer2+1),(2+6*x):(5+6*x)]
                df2.columns = ['Fx', 'Mz', 'My']
                df2.index = [df.columns[2+6*x]]
                df3 = pd.concat([df3, df2], ignore_index = False)
            df3 = df3.multiply(1000)
            temp_dict[round(float(i), 3)] = df3
        df_dict[pier] = temp_dict
        return df_dict
 
 
#results_dict['ULS3'] = sorResults(df_ULS3)

# Lagrer foreløpige dictionary-verdier til den tomme som er definert tidligere
# Dette kan nok gjøres på en mer dynamisk og elegant måte
results_dict = {"ULS2":df_ULS2,"ULS3":df_ULS3}

# looper igjennom results_dict for deretter å legge til ny dataframe, test(v),ved hver loop
for k,v in results_dict.items():
    print(k, v)
    results_dict[k] = test(v)


''' 
print('df_%s' %'test')
for envelope in ['ULS2', 'ULS3']: 
    print('df_%s' %envelope)
    results_dict[envelope] = test([df_%s  %envelope])
'''