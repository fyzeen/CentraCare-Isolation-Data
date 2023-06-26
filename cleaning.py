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

    df = df.drop(["FLO_MEAS_ID", "Last Date", "DISP_NAME", "MEAS_VALUE", "MEAS_VALUE_EXTERNAL"], axis=1).drop_duplicates()

    # Now we define a new row: Number of interactions (Item 2 in the SNI)
    df['NumInteractions'] = df.apply(lambda row: row['GetTogether_Val'] + row['Phone_Val'] if row['GetTogether_Val'] != 98 and row['Phone_Val'] != 98 else (row['GetTogether_Val'] + row['Phone_Val'] - 196) if row['GetTogether_Val'] == 98 and row['Phone_Val'] == 98 else row['GetTogether_Val'] + row['Phone_Val'] - 98, axis=1)
    df["NumInteractions"] = df["NumInteractions"] - 2 # Subtract two because GetTogether_Val==1 and Phone_Vla==1 representes 0 interactions via that medium

    # Define value to score mappings for each value
    Groups_YN_ValToScore = {1:1, 2:0, 98:0}
    Marriage_ValToScore = {3:1, 4:0, 5:0, 6:0, 7:0, 8:1, 98:0}
    Religious_ValToScore = {1:0, 2:0, 3:1, 98:0}
    GetTogether_ValToScore = {1:0, 2:0, 3:0, 4:1, 5:1, 98:0}
    Phone_ValToScore = {1:0, 2:0, 3:0, 4:1, 5:1, 98:0}
    NumGroupMeetings_ValToScore = {1:0, 2:0, 3:1, 98:0, None:0}
    NumInteractions_ValToScore = {0:0,  7:1,  1:0,  4:1,  5:1,  3:1,  8:1,  6:1,  2:0, None:0, -2:0, -1:0}

    # Compute scores based on values
    df["Groups_YN_Score"] = df["Groups_YN_Val"].map(Groups_YN_ValToScore)
    df["Marriage_Score"] = df["Marriage_Val"].map(Marriage_ValToScore)
    df['Religious_Score'] = df['Religious_Val'].map(Religious_ValToScore)
    df['GetTogether_Score'] = df['GetTogether_Val'].map(GetTogether_ValToScore)
    df['Phone_Score'] = df['Phone_Val'].map(Phone_ValToScore)
    df["NumGroupMeetings_Score"] = df["NumGroupMeetings_Val"].map(NumGroupMeetings_ValToScore)
    df["NumInteractions_Score"] = df["NumInteractions"].map(NumInteractions_ValToScore)

    # Compute Risk Score (4+ = Socially Integrated; 3 = Moderately Integrated; 2 = Moderately Isolated; 1 or 0 = Socially Isolated)
    df["SocialIntegrationScore"] = df["Groups_YN_Score"] + df["Marriage_Score"] + df['Religious_Score'] + df["NumInteractions_Score"]

    # Use a cutoff of TWO (2) as the score under which a patient is classified as "isolated"
    df["Isolation_YN"] = (df["SocialIntegrationScore"] < 2).astype(int)

    # Keeping only patients >= 18 years and < 100 (because we have only (maximum of) 10 individuals per age > 100)
    df = df[df['Age'] >= 18]
    df = df[df['Age'] < 100]
    
    # Add income information from ACS (median household income by zipcode)
    ACS_path = "/Users/fyzeen/FyzeenLocal/GitHub/CentraCare-Isolation-Data/data/ACS_Data/ACSST5Y2021.S1903-Data.csv"
    ACS = pd.read_csv(ACS_path)
    ACS['NAME(zip)'] = ACS['NAME(zip)'].str[6:].astype('float64')
    df["MedianZipIncome"] = df["Zipcode"].map(ACS.set_index("NAME(zip)")["S1903_C03_001E(median_indome)"])
    df["MedianZipIncome"] = df["MedianZipIncome"].replace('-', np.nan)
    df["MedianZipIncome"] = df["MedianZipIncome"].astype('float64')

    # Write csv
    df.to_csv("CentraCareIsolation_CLEANED.csv")