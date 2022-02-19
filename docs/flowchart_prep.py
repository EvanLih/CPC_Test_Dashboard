import pandas as pd
import plotly.express as px
from sodapy import Socrata
import webbrowser
client = Socrata("data.seattle.gov", None)

#OPA Internal Case Status
df = pd.DataFrame.from_records(client.get("pafy-bfmu", limit = 47000))

#OPA Disposition Outcomes
df2 = pd.DataFrame.from_records(client.get("99yi-dthu", limit = 47000))

#Closed Cases 2021-2022
df3 = pd.DataFrame.from_records(client.get("f8kp-sfr3", limit = 47000))
#Closed Cases 2022
df4 = pd.DataFrame.from_records(client.get("m33m-84uk", limit = 47000))


case_url_1 = pd.DataFrame([i for i in df3['case']])
case_url_2 = pd.DataFrame([i for i in df4['case']])

case_urls = pd.concat([case_url_1, case_url_2])


df.head()
df2.head()

def OPA_Case_Tracker():
    Case = input("Please Input OPA Case Number: ")
    try:
        print("This current case's status is classified as '{}'. The Disposition outcome is classified as '{}'".format(df.loc[df['opa_case_number'] == Case, 'status_description'].iloc[0], df2.loc[df2['file_number'] == Case, 'disposition'].iloc[0]))
    except:
        print("This is an invalid OPA case number. Please Input a valid OPA Case #. ")
    # if df.loc[df['opa_case_number'] == Case, 'status_description'].iloc[0] == 'OPA Close Case':
    try:
        webbrowser.open(case_urls.loc[case_urls['description'] == Case, 'url'].iloc[0])
    except:
        print("This case is not closed yet. ")


case_url.loc[case_url['description'] == "2019OPA-0506", 'url'].iloc[0]


df.loc[df['opa_case_number'] == Case, 'status_description'].iloc[0]

OPA_Case_Tracker()

df2.loc[df2['file_number'] == "2017OPA-0405", 'disposition'].iloc[0]

df.loc[df['opa_case_number'] == '2017OPA-0405', 'status_description'].iloc[0]

"This current case's status is classified as {}".format(df.loc[df['opa_case_number'] == "2017OPA-0405", 'status_description'].iloc[0])


df['status_description'].value_counts()

test = "2019OPA-0506"

test[0:4]