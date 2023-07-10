# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                html.Div(
                                    dcc.Dropdown(id='site-dropdown',
                                                options=[
                                                        {'label': 'All Sites', 'value': 'ALL'},
                                                        {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                        {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                        {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                        {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                                        ],      
                                                        value='ALL',
                                                placeholder="All sites",
                                            searchable=True
                                            ),
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                # html.Div([],id='success-pie-chart'),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={
                                                    0: '0',
                                                    1000: '1000',
                                                    2000: '2000',
                                                    3000: '3000',
                                                    4000: '4000',
                                                    5000: '5000',
                                                    6000: '6000',
                                                    7000: '7000',
                                                    8000: '8000',
                                                    9000: '9000',
                                                    10000: '10000'
                                                    },
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'), 
    Input(component_id='site-dropdown', component_property='value'))
def get_graph(chart):
    text="Total Successful launches by "
    if chart=='ALL':
        df=spacex_df[["Launch Site","class"]]
        p_data = df.groupby("Launch Site").mean()
        p_data.reset_index(inplace=True)
        fig = px.pie(p_data, values='class', names='Launch Site', title=text+"All sites")
        return fig
        # return fig
    else:
        h=spacex_df[spacex_df['Launch Site']==chart]
        df=h[["Launch Site","class"]]
        p_data = df.groupby("Launch Site").value_counts().reset_index(name="count")
        fig = px.pie(p_data, values='count', names='class', title=text+chart)
        return fig
        
        
        

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [
        Input(component_id='site-dropdown', component_property='value'),
        Input(component_id='payload-slider', component_property='value')
    ]
)
def get_graph2(opt,slider):
    text="Correlation between Payload and Success for "
    if opt=='ALL':
        df=spacex_df[(spacex_df['Payload Mass (kg)']>=slider[0]) & (spacex_df['Payload Mass (kg)']<=slider[1])]
        p_data=df[['class','Payload Mass (kg)', 'Booster Version Category',]]
        fig=px.scatter(data_frame=p_data,y='class',x='Payload Mass (kg)',color='Booster Version Category',title=text +'all sites')
        return fig
    else:
        df=spacex_df[(spacex_df['Payload Mass (kg)']>=slider[0]) & (spacex_df['Payload Mass (kg)']<=slider[1]) & (spacex_df['Launch Site']==opt)]
        p_data=df[['class','Payload Mass (kg)', 'Booster Version Category',]]
        fig=px.scatter(data_frame=p_data,y='class',x='Payload Mass (kg)',color='Booster Version Category',title=text +opt)
        return fig
        
    # return 

# Run the app
if __name__ == '__main__':
    app.run_server()