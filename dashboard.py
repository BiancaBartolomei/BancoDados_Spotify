
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.title = "Tutorial"

app.layout = html.Div(children=[
    html.H1(children='Hello Dash'),

    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='histogram',
        figure={
            'data': [
                {
                    'values': [[10, 90], [5, 95], [15, 85], [20, 80]][int(1) - 1],
                    'type' : 'pie'
                }
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    ),

    dcc.Slider(
        min=-5,
        max=10,
        step=0.5,
        value=-3,
    )

])

if __name__ == '__main__':
    app.run_server(debug=True)