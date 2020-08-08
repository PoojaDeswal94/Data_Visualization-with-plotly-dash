#!/usr/bin/env python
# coding: utf-8

# # Data Visualization Project
# 
# ## Analysis on suicide rates across the world from 1985 - 2016
# 
# *Pooja Deswal*
# 
# *Jyothish Kumar CHANDRASENAN GEETHAKUMARI*
# 
# *Levon Avetisyan*
# 
# **Msc DSA Fall 2019-2021**
# 

# In[1]:


# Imports
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# In[3]:


data = pd.read_csv("master.csv")
country = data["country"].unique()
#print(country)
year = data["year"].unique()
#print(year)

country_suicide = {}
year_suicide = {}

for value in country:
    #print(value)
    total_suicide = data.loc[data["country"] == value, "suicides_no"].sum()
    country_suicide[value] = total_suicide
    total_suicide = 0
    
for value in year:
    #print(value)
    total_suicide_year = data.loc[data["year"] == value, "suicides_no"].sum()
    year_suicide[value] = total_suicide_year
    total_suicide_year = 0 

################################# Graph 1 ###################################################
    
suicide_country_df = pd.DataFrame()
suicide_country_df['Country'] = country_suicide.keys()
suicide_country_df['Total Suicide Numbers'] = country_suicide.values()

bar_country_suicide = px.bar(suicide_country_df, y='Total Suicide Numbers', x='Country', text='Total Suicide Numbers')
bar_country_suicide.update_traces(texttemplate='%{text:.2s}', textposition='outside')

bar_country_suicide.update_layout(
    title='Country wise suicides from 1985-2016',
    xaxis_tickfont_size=18,
    yaxis=dict(
        title='Suicide Number',
        titlefont_size=16,
        tickfont_size=14,
    ),
    
   
    bargap=0.25, # gap between bars of adjacent location coordinates.
)    
bar_country_suicide.update_layout(uniformtext_minsize=15, uniformtext_mode='hide')
#fig.update_layout(title_text='Number of Suicides from 1985 to 2016')
#bar_country_suicide.show()


################################# Graph 2 ###################################################

pie_chart= px.pie(data,values='suicides_no', names='generation',title='Suicide Percentage with respect to generation')

################################# Graph 3 ###################################################

year_suicide_df = pd.DataFrame()
year_suicide_df['Year'] = year_suicide.keys()
year_suicide_df['Total Suicide Numbers'] = year_suicide.values()

bar_year_suicide = px.bar(year_suicide_df, y='Total Suicide Numbers', x='Year', text='Total Suicide Numbers')
bar_year_suicide.update_traces(texttemplate='%{text:.2s}', textposition='outside')

bar_year_suicide.update_layout(
    title='Year wise suicides from 1985-2016',
    xaxis_tickfont_size=18,
    yaxis=dict(
        title='Suicide Number',
        titlefont_size=16,
        tickfont_size=14,
    ),
    
   
    bargap=0.25, # gap between bars of adjacent location coordinates.
)    
bar_year_suicide.update_layout(uniformtext_minsize=15, uniformtext_mode='hide')
#fig.update_layout(title_text='Number of Suicides from 1985 to 2016')

################################# Graph 4 ###################################################


year_2002_new = data['year'] == 2002
suicide = data[year_2002_new][['suicides_no','country']]
suicide_dict = {}
for country in suicide['country'].unique():
     sum_suicide =suicide.loc[suicide['country'] == country, 'suicides_no'].sum()
     suicide_dict[country] = sum_suicide
     
#print(suicide_dict)



country_gdp_2002 = data[(data['year'] == 2002) & (data['country'].isin(['France','Australia','Belarus','Colombia','Brazil','Finland','Italy','Japan',
                                                         'Netherlands','Kazakhstan','Singapore','Sweden','Croatia','Latvia','Ireland',
                                                         'Canada','Republic of Korea','Russian Federation', 'Germany', 'United States',
                                                         'Antigua and Barbuda', 'Bahmas', 'Baharin','Kuwait', 'Maldives']))]
country_gdp_2002 = country_gdp_2002[['country',' gdp_for_year ($) ','gdp_per_capita ($)']]
country_gdp_2002 = country_gdp_2002.drop_duplicates()



scatter_gdp_2002 = px.scatter(country_gdp_2002, x="country", y = " gdp_for_year ($) ")

scatter_gdp_2002.update_layout(
    title='GDP status of various countries in the year 2002',
    xaxis_tickfont_size=18,
    yaxis=dict(
        title='GDP of year 2012 ($)',
        titlefont_size=16,
        tickfont_size=14,
    )
    
 )

################################# Graph 5 ###################################################

year_2002 = data['year'] == 2002
gdp_2002 = data[year_2002][['gdp_per_capita ($)','country']]
unique_gdp = gdp_2002.drop_duplicates()
suicide = data[year_2002][['suicides_no','country']]
suicide_dict = {}
suicide_list=[]
for country in suicide['country'].unique():
     sum =suicide.loc[suicide['country'] == country, 'suicides_no'].sum()
     suicide_dict[country] = sum
     suicide_list.append(sum)
unique_gdp.insert(2, "suicide_sum",suicide_list, True)
max_10 = unique_gdp.nlargest(15,'suicide_sum')

layout = go.Layout(title = 'Time Series Plot',
                   hovermode = 'closest')
bubble_gdp_2002 = go.Figure(data=[go.Scatter(
    x=max_10['country'],
    y=max_10['suicide_sum'],
    mode='markers', marker=dict(
        color=[120, 125, 130, 135, 140, 145,150,155,160,165,170,175,180],
        size=max_10['gdp_per_capita ($)']/1000,
        showscale=True
        ))])

bubble_gdp_2002.update_layout(
    title='Suicides based on GDP of the country',
    xaxis_tickfont_size=18,
    yaxis=dict(
        title='Total number of suicides',
        titlefont_size=16,
        tickfont_size=14,
    )
    
 )


bar_country_suicide.show()
bar_year_suicide.show()
scatter_gdp_2002.show()
bubble_gdp_2002.show()
pie_chart.show()

Suicide_rates=dash.Dash()
Suicide_rates.layout = html.Div([html.Div([html.H1("Data visualization project"),html.P("World wide analysis of suicide rates from 1985 - 2016")],
                                        style = {'padding' : '50px' ,'backgroundColor' : '#3EB7EE','font-family': "sans serif", 'color' :'white'}),
                                 dcc.Graph(figure=bar_country_suicide),
                                 dcc.Graph(figure=pie_chart),
                                 dcc.Graph(figure=bar_year_suicide), 
                                 dcc.Graph(figure=scatter_gdp_2002),
                                 dcc.Graph(figure=bubble_gdp_2002)])


Suicide_rates.run_server(debug=True, use_reloader=False)

