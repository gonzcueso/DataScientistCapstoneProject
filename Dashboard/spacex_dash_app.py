# Import required libraries
import pandas as pd
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import dash

# Read the SpaceX data into a pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[
    html.H1('SpaceX Launch Records Dashboard',
            style={'textAlign': 'center', 'color': '#503D36',
                   'font-size': 40}),
    
    # TASK 1: Add a dropdown list to enable Launch Site selection
    dcc.Dropdown(id='site-dropdown',
                 options=[
                     {'label': 'All Sites', 'value': 'ALL'},
                     {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                     {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'},
                     {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                     {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'}
                 ],
                 value='ALL',
                 placeholder="Select a Launch Site here",
                 searchable=True
                 ),
    html.Br(),

    # TASK 2: Add a pie chart to show the total successful launches count for all sites
    # If a specific launch site was selected, show the Success vs. Failed counts for the site
    dcc.Graph(id='success-pie-chart'),
    html.Br(),

    html.P("Payload range (Kg):"),
    
    # TASK 3: Add a slider to select payload range
    dcc.RangeSlider(id='payload-slider',
                    min=0, max=10000, step=1000,
                    marks={0: '0',
                           1000: '1000',
                           2000: '2000',
                           3000: '3000',
                           4000: '4000',
                           5000: '5000',
                           6000: '6000',
                           7000: '7000',
                           8000: '8000',
                           9000: '9000',
                           10000: '10000'},
                    value=[min_payload, max_payload]),
    
    # TASK 4: Add a scatter chart to show the correlation between payload and launch success
    dcc.Graph(id='success-payload-scatter-chart'),
])

# TASK 2: Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(
    Output(component_id='success-pie-chart', component_property='figure'),
    Input(component_id='site-dropdown', component_property='value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Filter data for all sites and calculate the percentage of successful launches
        df_all_sites = spacex_df.groupby('Launch Site')['class'].mean().reset_index()
        fig = px.pie(df_all_sites, names='Launch Site', values='class',
                     title='Total Launch Success Rate by Site')
    else:
        # Filter data for the selected site and calculate the counts of successful and failed launches
        df_site = spacex_df[spacex_df['Launch Site'] == selected_site]
        site_success_counts = df_site['class'].value_counts().reset_index()
        site_success_counts.columns = ['Outcome', 'Count']
        fig = px.pie(site_success_counts, names='Outcome', values='Count',
                     title=f'Success vs. Failure for {selected_site}')
    
    return fig

# TASK 4: Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(
    Output(component_id='success-payload-scatter-chart', component_property='figure'),
    [Input(component_id='site-dropdown', component_property='value'),
     Input(component_id='payload-slider', component_property='value')]
)
def update_scatter_chart(selected_site, payload_range):
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) &
                            (spacex_df['Payload Mass (kg)'] <= max_payload)]

    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]
    
    fig = px.scatter(filtered_df, x='Payload Mass (kg)', y='class',
                     color='Booster Version Category',
                     title=f'Payload vs. Success for {selected_site if selected_site != "ALL" else "All Sites"}')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
