# Import required libraries
# https://www.coursera.org/learn/applied-data-science-capstone/ungradedLti/EtmJx/hands-on-lab-build-an-interactive-dashboard-with-ploty-dash

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

# 


# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard ',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                                dcc.Dropdown(id='site-dropdown',
                                    options=[
                                    {'label': 'All Sites', 'value': 'ALL'},
                                    {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                    {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                    {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                                    {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                    ],
                                value='ALL',
                                placeholder="Select a Launch Site here ",
                                searchable=True
                                ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

								dcc.RangeSlider(id='payload-slider',
									min=0, max=10000, step=1000,
									marks={0: '0',
										   100: '100'},
									value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# add callback decorator
# Function decorator to specify function input and output
@app.callback([Output(component_id='success-pie-chart', component_property='figure'), Output(component_id='success-payload-scatter-chart', component_property='figure')],
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id="payload-slider", component_property="value")])


def get_pie_chart(entered_site, entered_payload =[min_payload, max_payload]):
    filtered_df = spacex_df
    
    if entered_site == 'ALL':
        fig_all_1 = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='all launch sites')
        filtered_payload_df = spacex_df[(spacex_df["Payload Mass (kg)"] >= entered_payload[0]) & (spacex_df["Payload Mass (kg)"] <= entered_payload[1])]
        print("the spacex_df in all is ", entered_payload )
        fig_all_2 = px.scatter(filtered_payload_df, x = "Payload Mass (kg)", y = "class", color ="Booster Version Category", title =f"Correlation between Patload and Suucess for All Sites in the range {entered_payload}")
        return [fig_all_1, fig_all_2]
    else:
        print("the entered_site is ", entered_site)
        entered_site_df = spacex_df[spacex_df['Launch Site']== entered_site]
        entered_site_df_counted = entered_site_df.groupby('class')[['class']].count().rename(columns = {"class": "counted_class"}).reset_index()	
        fig_site1 = px.pie(entered_site_df_counted, values= 'counted_class', 
        names="class",
        title=f'success rate and failure rate in {entered_site}')
		
        entered_site_df = entered_site_df[(entered_site_df["Payload Mass (kg)"] >=entered_payload[0])  & (entered_site_df["Payload Mass (kg)"] <=entered_payload[1]) ]
        fig_site2 = px.scatter(entered_site_df, x = "Payload Mass (kg)", y = "class", color = "Booster Version Category", 
        title = f"Correlation between Patload and Suucess in Site: {entered_site} in the range : {entered_payload}"
        )
        return [fig_site1, fig_site2]





# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run_server()
