import pandas as pd
from sodapy import Socrata
import plotly.express as px
import plotly
import squarify
client = Socrata("data.seattle.gov", None)

results = client.get("99yi-dthu", limit = 47000)

results_df = pd.DataFrame.from_records(results)

#Verifying unique file ID/OPA case # Information. 
results_df.file_number.value_counts()


results_df = results_df.astype({'received_date': 'datetime64[ns]', 'occurred_date':'datetime64[ns]','investigation_begin_date':'datetime64[ns]','investigation_end_date':'datetime64[ns]'})
results_df['year'] = results_df['received_date'].dt.year

# results_2021 = results_2021[~results_2021.investigation_end_date.isnull()] 
# test = results_2021['investigation_begin_date'] > '2021-01-01' 
# test = results_2021['investigation_end_date'] - results_2021['investigation_begin_date']  
# test.median()


results_df['investigation_end_date'].head()
results_df['investigation_begin_date'].head()
results_df= results_df.drop_duplicates(subset = 'file_number', keep = 'first')

results_df = results_df.drop_duplicates(subset = 'file_number', keep = 'first')
results_df['disposition'].replace({'-':'OPA Active Cases'}, inplace = True)

Dispositions_yearly = pd.DataFrame(results_df.groupby(['disposition', 'year']).size().reset_index(name = "counts")).sort_values('year', inplace = False)

Incidents_yearly = pd.DataFrame(results_df.groupby(['incident_type', 'year']).size().reset_index(name = "counts")).sort_values('year', inplace = False)


##creating new subsets from 2019-2021, for flowchart data. 
Incident_type_2019_2022 = Incidents_yearly.loc[Incidents_yearly['year'] >=2019]

Incident_type_2019_2022 

#Subsetting to only include from 2014 onward 
Dispositions_yearly = Dispositions_yearly.loc[Dispositions_yearly['year'] >=2014]

Incidents_yearly = Incidents_yearly.loc[Incidents_yearly['year']>=2014]

#Dispositions can only contain No Allegations Sustained, Partially Sustained, All Allegations Sustained, and Rapid Adjudication Closed. ALl the other findings arte sent back to the CoC or

Dispositions_yearly = Dispositions_yearly[Dispositions_yearly['disposition'].isin(['OPA All Allegations Sustained', 'OPA No Allegations Sustained', 'OPA Partially Sustained', 'OPA Rapid Adjudication Closed', 'OPA Active Cases'])]


fig = px.histogram(Dispositions_yearly, x = "disposition", y = "counts", facet_col = "year").update_xaxes(tickangle=30)

treemap = px.treemap(Dispositions_yearly, path = ["year","disposition"], values = 'counts')
totaltreemap = px.treemap(Incident_type_2019_2022 , path = [ "disposition"], values = 'counts')

totaltreemap.show()

fig1 = px.histogram(Incidents_yearly, x = "incident_type", y = "counts", facet_col = "year").update_xaxes(tickangle=30)

plotly.offline.plot(fig1, filename = 'F:/Github/CPC_Test_Dashboard/docs/histogram.html')
plotly.offline.plot(fig, filename = 'F:/Github/CPC_Test_Dashboard/docs/histogram2.html')
plotly.offline.plot(treemap, filename = 'F:/Github/CPC_Test_Dashboard/docs/treemap.html')
plotly.offline.plot(totaltreemap, filename = 'F:/Github/CPC_Test_Dashboard/docs/totaltreemap.html')




# results_2021.groupby(results_df['received_date'].dt.year)

