# importing modules
import pandas as pd
import numpy as np

if __name__ == '__main__':
    
    df = pd.read_excel("./data/CentracareSocialIsolationData.xlsx")

    berkman_syme = df["DISP_NAME"].unique()
    subjects = df["ID"].unique()

    df["Groups_YN_Val"] = ''
    df["Groups_YN_Ext"] = ''
    df["Marriage_Val"] = ''
    df["Marriage_Ext"] = ''
    df['Religious_Val'] = ''
    df['Religious_Ext'] = ''
    df['GetTogether_Val'] = ''
    df['GetTogether_Ext'] = ''
    df['Phone_Val'] = ''
    df['Phone_Ext'] = ''
    df["NumGroupMeetings_Val"] = ''
    df["NumGroupMeetings_Ext"] = ''

    row_vals = ["Groups_YN_Val", "Marriage_Val", 'Religious_Val', 'GetTogether_Val', 'Phone_Val', "NumGroupMeetings_Val"]
    row_exts = ["Groups_YN_Ext", "Marriage_Ext", 'Religious_Ext', 'GetTogether_Ext', 'Phone_Ext', "NumGroupMeetings_Ext"]

    for subj in subjects:
        subj_rows = df.loc[(df['ID'] == subj)]
        print(subj)
        
        for index, item in enumerate(berkman_syme):
            row = subj_rows.loc[(subj_rows['DISP_NAME'] == item)]
            
            if row.size == 0:
                pass
            else:
                value = row['MEAS_VALUE'].unique()[0]
                ext_value = row['MEAS_VALUE_EXTERNAL'].unique()[0]

                df.loc[(df['ID'] == subj), row_vals[index]] = value
                df.loc[(df['ID'] == subj), row_exts[index]] = ext_value 

    out = df.drop(["FLO_MEAS_ID", "Last Date", "DISP_NAME", "MEAS_VALUE", "MEAS_VALUE_EXTERNAL"], axis=1).drop_duplicates()

    out.to_csv("CentraCareSocialIsolation_CLEANED.csv")