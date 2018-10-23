
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from sqlalchemy import create_engine
from datetime import date as dt



engine = create_engine('postgres://bdxulnbxczgzlx:41d56d0522876a442b7494fa56070a4993b34868812d14d5f93debd7a98fde6b@ec2-'
                       '184-72-234-230.compute-1.amazonaws.com:5432/d9vbm9b8oufhkq')

df = pd.read_sql_query('select * from spotify_db.top_musicas_populares',con=engine)
print(df)

def update_dropdown_artist():
    opt_artist = []
    artistas = []
    for artist in df['artist_name']:

        if artist not in artistas:
            a = {'label':artist, 'value':artist}
            opt_artist.append(a)
            artistas.append(artist)
    return opt_artist

def update_dropdown_genre():
    generos = []
    opt_genre = []
    for genre in df['artist_genre']:

        if genre not in generos and genre is not None:
            a = {'label':genre, 'value':genre}
            opt_genre.append(a)
            generos.append(genre)
    return opt_genre

def update_dropdown_track():
    musicas = []
    opt_track = []
    for track in df['track_name']:

        if track not in musicas and track is not None:
            a = {'label':track, 'value':track}
            opt_track.append(a)
            musicas.append(track)
    return opt_track

external_stylesheets = ['https://raw.githubusercontent.com/BiancaBartolomei/BDII_API_Spotify/css/assets/style.css']

app = dash.Dash(__name__)
server = app.server

app.title = "SPOTIFY POPULARITY DATABASE"

app.layout = html.Div(children=[
    html.H1(children='Spotify Popularity Database',
            style={
                'textAlign': 'center',
                'color' : 'white',
                'font-weight': 'bold'

            }
            , className=''),


    html.Div([
        html.Div([
            html.H4(children='Popularidade das músicas em uma data',
            style={
                'textAlign': 'center',
                'font-weight': 'bold',
                'margin-left' : 50,

            }
            , className=''),
            html.Div([
                dcc.Graph(
                    id='musicas_populares',
                    figure={
                        'data': [
                            {'x': df['track_name'], 'y': df['track_popularity'], 'type': 'bar'},
                        ],
                        'layout': {
                            'yaxis': {'title': 'Popularidade'}
                        }
                    }
                ),
            ], className='mdl-cell mdl-cell--10-col'),

            html.Div([
                html.H4(
                    children='FILTROS',
                        style={
                        'textAlign': 'center',
                        'font-weight': 'bold',

                        }
                    , className=''
                ),
                html.Div([
                    html.H5(children='Data'),
                    dcc.DatePickerSingle(
                        id='date-picker-single',
                        date=dt.today()
                    )
                ], className=''),

                html.Div([
                    html.H5(children='Gênero'),
                    dcc.Dropdown(
                        id='dropdown-genre',
                        options= update_dropdown_genre(),
                        multi=True,
                        value=""
                    ),
                ], className=''),

                html.Div([
                    html.H5(children='Artista'),
                    dcc.Dropdown(
                        id='dropdown-artist',
                        options= update_dropdown_artist(),
                        multi=True,
                        value=""
                    )
                ], className=''),
            ], className='mdl-cell mdl-cell--2-col'),
        ], className='mdl-grid'),
    ], className='card-teste'),

    html.Div([
        html.Div([
            html.H4(children='Popularidade de uma música ao longo do tempo',
            style={
                'textAlign': 'center',
                'font-weight': 'bold',
                'margin-left' : 50,

            }
            , className=''),
            html.Div([
                dcc.Graph(
                    id='popularidade_musica',
                    figure={
                        'data': [
                            {'x': df['data_popularidade'], 'y': df['track_popularity'], 'type': 'lines'},
                        ],
                        'layout': {
                            'xaxis': {'title': 'Data'},
                            'yaxis': {'title': 'Popularidade'}
                        }
                    }
                ),
            ], className='mdl-cell mdl-cell--10-col'),
            html.Div([
                html.H4(children='Músicas',
                        style={
                        'font-weight': 'bold',

                        }
                    , className=''),
                dcc.Dropdown(
                    id='dropdown-music',
                    options=update_dropdown_track(),
                    multi=False,
                    value=""
                )
            ], className='mdl-cell mdl-cell--2-col'),

        ], className='mdl-grid'),
    ], className='card-teste'),
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
        marker=dict(
            color='rgba(39,144,176,1)',
        )
    ))

    return {
        'data': traces,
        'layout': {
                'yaxis': {'title': 'Popularidade'},
        }
    }

@app.callback(
    dash.dependencies.Output('popularidade_musica','figure'),
    [dash.dependencies.Input('dropdown-music','value')])
def update_figure(track_input):
    filtro = pd.DataFrame(columns=['track_name','artist_name','track_popularity','data_popularidade','artist_genre'])
    temp = df


    if track_input:
        temp = temp.loc[df['track_name'] == track_input]

        filtro = temp
    else:
        filtro = pd.DataFrame(columns=['track_name','artist_name','track_popularity','data_popularidade','artist_genre'])



    traces = []

    traces.append(go.Line(
        x=filtro['data_popularidade'],
        y=filtro['track_popularity'],
        marker=dict(
            color='rgba(39,144,176,1)',
        )
    ))

    return {
        'data': traces,
        'layout': {
                'xaxis': {'title': 'Data'},
                'yaxis': {'title': 'Popularidade'}

        }
    }

if __name__ == '__main__':
    app.run_server(debug=True)