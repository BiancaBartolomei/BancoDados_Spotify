
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import datetime as dt



engine = create_engine('postgres://bdxulnbxczgzlx:41d56d0522876a442b7494fa56070a4993b34868812d14d5f93debd7a98fde6b@ec2-'
                       '184-72-234-230.compute-1.amazonaws.com:5432/d9vbm9b8oufhkq')

df = pd.read_sql_query('select * from spotify_db.top_musicas_populares',con=engine)
print(df)
opt_artist = []
opt_genre = []

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.title = "Spotify Popularidades Database"

app.layout = html.Div(children=[
    html.H1(children='Spotify Popularidades Database'),

    html.Div(children='''
        Top 10
    '''),
    html.Div([
        dcc.Graph(
            id='musicas_populares',
            figure={
                'data': [
                    {'x': df['track_name'], 'y': df['track_popularity'], 'type': 'bar'},
                ],
                'layout': {
                    'title': 'Dash Data Visualization'
                }
            }
        ),
        html.Div([
            html.H3(children='Filtro por data'),
            dcc.DatePickerSingle(
                id='date-picker-single',
                date=dt.now()
            )
        ], className='six columns'),

        html.Div([
            html.H3(children='Filtro por genero'),
            dcc.Dropdown(
                id='dropdown-genre',
                options= opt_genre,
                multi=True,
                value=""
            ),
        ], className='six columns'),

        html.Div([
            html.H3(children='Filtro por artista'),
            dcc.Dropdown(
                id='dropdown-artist',
                options= opt_artist,
                multi=True,
                value=""
            )
        ], className='six columns'),
    ], className='row')

])


@app.callback(
    dash.dependencies.Output('musicas_populares','figure'),
    [dash.dependencies.Input('date-picker-single', 'date'),
     dash.dependencies.Input('dropdown-genre','value'),
     dash.dependencies.Input('dropdown-artist','value')])
def update_figure(date, genre_input, artist_input):
    print(genre_input)
    print(artist_input)

    filtro = pd.DataFrame(columns=['track_name','artist_name','track_popularity','data_popularidade','artist_genre'])
    temp = df

    if artist_input or genre_input or date:
        if artist_input:
            temp = temp.loc[df['artist_name'].isin(artist_input)]
        if genre_input:
            temp = temp.loc[df['artist_genre'].isin(genre_input)]
        if date:
            temp = temp.loc[df['data_popularidade'] == date]

        filtro = temp
    else:
        filtro = df



    traces = []

    traces.append(go.Bar(
        x=filtro['track_name'],
        y=filtro['track_popularity'],
    ))

    return {
        'data': traces,
        'layout': {
                'title': 'Dash Data Visualization'
        }
    }


if __name__ == '__main__':
    artistas = []
    generos = []
    for artist in df['artist_name']:

        if artist not in artistas:
            a = {'label':artist, 'value':artist}
            opt_artist.append(a)
            artistas.append(artist)

    for genre in df['artist_genre']:

        if genre not in generos and genre is not None:
            a = {'label':genre, 'value':genre}
            opt_genre.append(a)
            generos.append(genre)

    app.run_server(debug=True)