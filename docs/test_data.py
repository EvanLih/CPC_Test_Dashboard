import pandas as pd
from sodapy import Socrata
import plotly.express as px
import plotly
client = Socrata("data.seattle.gov", None)

results = client.get("99yi-dthu", limit = 47000)

results_df = pd.DataFrame.from_records(results)



results_2021 = results_df.astype({'received_date': 'datetime64[ns]', 'occurred_date':'datetime64[ns]','investigation_begin_date':'datetime64[ns]','investigation_end_date':'datetime64[ns]'})
results_2021['year'] = results_2021['received_date'].dt.year

results_2021 = results_2021[~results_2021.investigation_end_date.isnull()] 
# test = results_2021['investigation_begin_date'] > '2021-01-01' 
# test = results_2021['investigation_end_date'] - results_2021['investigation_begin_date']  
# test.median()


results_2021['investigation_end_date'].head()
results_2021['investigation_begin_date'].head()

Dispositions = pd.DataFrame(results_df['disposition'].value_counts().reset_index())
Dispositions = Dispositions.rename(index = {0:"disposition", 1:"count"} )


Incidents_yearly = pd.DataFrame(results_2021.groupby(['incident_type', 'year']).size().reset_index(name = "counts")).sort_values('year', inplace = False)




fig = px.histogram(Dispositions, x = "index", y = "disposition").show()
fig1 = px.histogram(Incidents_yearly, x = "incident_type", y = "counts", facet_col = "year")

fig1.write_html('histogram.html')


results_2021.groupby(results_df['received_date'].dt.year)