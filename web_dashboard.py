from analysis import *

import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

df = update_db()

external_stylesheets = [dbc.themes.BOOTSTRAP]
app = dash.Dash (__name__, external_stylesheets=external_stylesheets)
server = app.server


app.layout = dbc.Container(
    [
        html.Div ([
            dcc.Dropdown (
                id='day-dropdown',
                options=[{'label': d, 'value': d} for d in df['extract_day'].unique()],
                multi=True,
                placeholder='All dates combined'
            ),
            html.Div(id='dd-output-container')
        ]),
        dbc.Row(
            [
                dbc.Col(children=[
                    html.H2('Wordcloud of all words present in articles',
                            style={'font-size': '16px', 'text-align': 'center'}),
                    html.Img(id='wordcloud')

                ]),
                dbc.Col(
                    dcc.Graph(id='sources_graph'),
                    style={"margin-left": "100px", 'width': '100%'},
                ),
            ],
            style={'margin-top': '50px', 'margin-bottom': '50px'},
        ),
        # dbc.Row(
        #     [
        #         dbc.Col(
        #             dcc.Graph(figure=freq_sources_graph(df)),
        #             width=12,
        #             style={"height": "100%", "background-color": "blue"},
        #         )
        #     ],
        #     className="h-35",
        # ),
    ]
)


@app.callback(
    dash.dependencies.Output('sources_graph', 'figure'),
    [dash.dependencies.Input('day-dropdown', 'value')])
def update_graph(day):
    if day is None:
        dff = df
    else:
        dff = df.loc[df.extract_day.isin(day)]
    return fig_freq(list(dff['sources']))


@app.callback(
    dash.dependencies.Output('wordcloud', 'src'),
    [dash.dependencies.Input('day-dropdown', 'value')])
def wordcloud_graph(day):
    if day is None:
        dff = df
    else:
        dff = df.loc[df.extract_day.isin(day)]

    fig = fig_wordcloud(get_full_text(dff['titles']), 500)

    return "data:image/png;base64," + fig


def per_hour_graph(df):
    pass


if __name__ == '__main__':
    app.run_server(debug=False)