from xml.dom import INVALID_MODIFICATION_ERR
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#plotly
import chart_studio as py
import cufflinks as cf
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
#dcc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input,Output #mainly for the i/o function=
import dash
import dash_bootstrap_components as dbc

from plotly.offline import download_plotlyjs,init_notebook_mode,plot,iplot
init_notebook_mode(connected=True)

cf.go_offline() #mainly for the plotly


 
#csv edit importation
gender = pd.read_csv('/Users/admin/Desktop/Python_Work/SGstats/sport-participation-level/gender_edit.csv')
race = pd.read_csv('/Users/admin/Desktop/Python_Work/SGstats/sport-participation-level/race_edit.csv')
gmod = pd.read_csv('/Users/admin/Desktop/Python_Work/SGstats/sport-participation-level/participation_level_edit.csv')
age = pd.read_csv('/Users/admin/Desktop/Python_Work/SGstats/sport-participation-level/age_group.csv')

#external graphs and whatever that is needed
def participation():
    fig = go.Figure()
    fig.add_trace(go.Bar(
        y = gmod["didnotparticipatepastyear"],
        x = gmod.annual,
        name = "Did Not Participate %",
        marker = dict(
            color = 'rgba(0,300,0,0.6)',
            line= dict (
                color ='rgba(0,0,0,0.5)' , width = 0.1)
        )
    ))
    fig.add_trace(go.Bar(
        y = gmod["sedentary"],
        x = gmod.annual,
        name = "Sedentary %",
        marker = dict(
            color = 'rgba(0,0,300,0.6)',
            line = dict (
                color ='rgba(0,0,0,0.5)' , width = 0.1)
        )
    ))
    fig.add_trace(go.Bar(
        y = gmod["irregular"],
        x = gmod.annual,
        name = "Irregular %",
        marker = dict(
            color = 'rgba(0,150,0,0.5)',
            line = dict (
                color ='rgba(0,0,0,0.5)' , width = 0.1)
        )
    ))
    fig.add_trace(go.Bar(
        y = gmod["regular"],
        x = gmod.annual,
        name = "Regular %",
        marker = dict(
            color = 'rgba(0,0,150,0.6)',
            line = dict (
                color ='rgba(0,0,0,0.5)' , width = 0.1)
        )
    ))
    fig.update_layout(
        yaxis = dict(
            title_text = "General Participation %"
        ),
        xaxis = dict(
            tickmode = 'linear',
            tick0 = 2015,
            dtick = 1
        
        ),
        autosize = False,
        barmode = 'stack',
        title = dict(text = "Sports Participation Per Year"),
        title_x = 0.5,
    )

    return fig

#initializing the main applciation
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.LITERA])
#WHENEVER YOU WANT TO SPECIFY THEME PLEASE CAPITALISE IT
server = app.server
#dbc container as a whole if you are using purely dbc
app.layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H1("Sports Participation In Singapore",
            #class name suggestions for whenever you want to edit your css of the title 
            className = 'text-center text-primary'
            ), width = 12)
    #if you wish to add class name into the utility do this (use a cheatsheet)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='general',figure = participation())
        ],width = 12)
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Dropdown(
                id = 'year',
                options = [
                    {'label': i, 'value': i} for i in range(2015,2022)
                    ],
                value = 2015),
        ], width = 12)
    ]),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id= 'race')
        ])
    ]),
    html.Br(),
    dbc.Row([
        dbc.Col([
            dcc.Graph(id = 'gender')
    ], width = {'size':6},
    #width = reference towards the gridding
    #values below are referencing towards different screen sizes. xs - xl sizes
        xs = 12, sm = 12, md = 12, lg = 5, xl = 5
    ),
        dbc.Col([
            dcc.Graph(id = 'age')
            #ensure that the offset does not exceed the number of cols else it will colapse
            #order decides which column comes first
        ], width = {'size':5,'offset': 1,'order':1},
    #values reference to diff screen size (xs - xl)
            xs = 12, sm = 12, md = 12, lg = 5, xl = 5
        )
    ]) 
], fluid = True)

#DBC Container also contains this thing called Fluid (stretches everything out)


#callbacks
@app.callback(
    [Output(component_id = 'race',component_property = 'figure'),
    Output(component_id = 'gender',component_property = 'figure'),
    Output(component_id = 'age',component_property = 'figure')
    ],
    [Input(component_id = 'year',component_property = 'value')]

)

def update_graph(year_selected):
#race function
    rcc = race.copy()
    fig = make_subplots(rows = 1, cols = 4,
    specs = [[{"type":"pie"},{"type":"pie"},{"type":"pie"},{"type":"pie"}]],
    #naming each subplot title for the naming purpose
    subplot_titles = ["Plot 1", "Plot 2", "Plot 3", "Plot 4"])
    labelling = ["Exercise", " Did Not Exercise"]
#converting the entire pandas list into numerical ( getting rid of data name and dtype)
    rc = rcc.loc[rcc['annual'] == year_selected].values.flatten().tolist()
    fig.add_trace(go.Pie(values = rc[2:4],labels = labelling,
    name = "Chinese"),
    row = 1 , col = 1)

    fig.add_trace(go.Pie(values = rc[4:6],labels = labelling,
    name = "Malay"),
    row = 1 , col = 2)

    fig.add_trace(go.Pie(values = rc[6:8],labels = labelling,
    name = "Indian"),
    row = 1 , col = 3)

    fig.add_trace(go.Pie(values = rc[8:10],labels = labelling,
    name = "Others"),
    row = 1 , col = 4)
    #layout name updating
    fig.update_layout(
        title = "Race Participation",
        title_x = 0.5
    )
#naming them
    names = {'Plot 1':'Chinese', 'Plot 2':'Malay', 'Plot 3':'Indian', 'Plot 4':'Others'}
    fig.for_each_annotation(lambda a: a.update(text = names[a.text]))

#gender function
    gender_edit= gender.copy()
    fig2 = make_subplots(rows = 1, cols = 2,
    specs = [[{"type":"pie"}, {"type":"pie"}]],
    subplot_titles = ["P1", "P2"],) 
# we will reuse the labels from labelling
    gc = gender_edit.loc[gender_edit["annual"] == year_selected].values.flatten().tolist()
    fig2.add_trace(go.Pie(values = gc[2:4],labels = labelling,name = "Male"),
    row = 1, col = 1)

    fig2.add_trace(go.Pie(values = gc[4:6],labels = labelling,name = "Female"),
    row = 1, col = 2)

    fig2.update_layout(
        title = "Gender",
        title_x = 0.5
    )
#gender naming
    gender_name = {'P1': 'Male', 'P2': 'Female'}
    fig2.for_each_annotation(lambda a: a.update(text = gender_name[a.text])) 
    
#we will now do a multi line/bar chart for the age group
    fig3 = go.Figure()
    acc = age.copy()
    ac = acc.loc[acc["annual"] == year_selected].values.flatten().tolist()
#using the pandas method of converting the namelist 
    z = acc.columns.values.flatten().tolist()
    labels = z[1:]
    fig3.add_trace(go.Bar(x=labels, y = ac[1:],
    hovertext= labels, name = 'Bar Representation'))
    fig3.add_trace(go.Scatter(x=labels, y = ac[1:], name = 'Line Representation'))

    fig3.update_layout(
        title = "Age Representation",
        title_x = 0.5
    )
#take note that in future when returning graph objects must be placed in array, do not seperate it out
    return [go.Figure(data = fig),go.Figure(data = fig2),go.Figure(data = fig3)]


if __name__ == '__main__':
    app.run_server(debug = True)
