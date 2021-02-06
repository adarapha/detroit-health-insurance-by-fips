import pandas as pd
import plotly.express as px  # (version 4.7.0)
import plotly.graph_objects as go
from helper import merge

import dash  # (version 1.12.0) pip install dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from urllib.request import urlopen
import json
with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response: counties = json.load(response)

app = dash.Dash(__name__)
df = merge()

app.layout = html.Div([
    dcc.Graph(id='my_map', figure={})
])

fig = px.choropleth(
    data_frame=df,
    geojson=counties,
    locations='STCOUNTYFP',
    color='Estimated_Percent_Insured',
    scope="usa",
    color_continuous_scale="Viridis",
    labels={'Estimated_Percent_Insured': 'Estimated_Percent_Insured'},
    template='plotly_dark'
)

fig.show()

if __name__ == '__main__':
    app.run_server(debug=True)