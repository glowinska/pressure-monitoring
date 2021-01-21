import datetime as dt
import dash
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import threading
from time import sleep
import plotly.graph_objects as go
from dash.dependencies import Input, Output, State
from db.db_api import *
import plotly

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
)

from pyorbital.orbital import Orbital
satellite = Orbital('TERRA')

server = app.server

app_color = {"graph_bg": "#082255", "graph_line": "#309ADE"}

params = [
    'L0', 'L1', 'L2', 'R0', 'R1', 'R2'
]

figs = { 
    'L0': go.Figure(), 'L1': go.Figure(), 'L2': go.Figure(), 'R0': go.Figure(), 'R1': go.Figure(), 'R2': go.Figure()
}

app.layout = html.Div(
    [
        # header
        html.Div(
            [
                html.Div(
                    [
                        html.H4("MONITORING WALKING HABITS", className="app__header__title"),
                        html.P(
                            "The application presents a graphical visualization of measurements of a device for monitoring walking habits and patterns and displays live charts of pressure and anomalies in moving.",
                            className="app__header__title--grey",
                        ),
                    ],
                    className="app__header__desc",
                ),
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo.png"),
                            className="app__menu__img",
                        )
                    ],
                    className="app__header__logo",
                ),
            ],
            className="app__header",
        ),
        html.Div(
            [
                #left foot
                html.Div(
                    [
                        html.Div(
                            [html.H6("LEFT FOOT", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="l0",
                            figure=figs['L0'],
                            animate=True,
                        ),
                        dcc.Graph(
                            id="l1",
                            figure=figs['L1'],
                            animate=True,
                        ),
                        dcc.Graph(
                            id="l2",
                            figure=figs['L2'],
                            animate=True,
                        ),
                    ],
                    className="one-third column date__container",
                ),
                # right foot
                html.Div(
                    [
                        html.Div(
                            [html.H6("RIGHT FOOT", className="graph__title")]
                        ),
                        dcc.Graph(
                            id="r0",
                            figure=figs['R0'],
                            animate=True,
                        ),
                        dcc.Graph(
                            id="r1",
                            figure=figs['R1'],
                            animate=True,
                        ),
                            dcc.Graph(
                            id="r2",
                            figure=figs['R2'],
                            animate=True,
                        ),
                    ],
                    className="one-third column date__container",
                ),

                html.Div(
                    [
                        # personal data
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "PERSONAL DATA",
                                            className="graph__title",
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        dcc.Dropdown(
                                            id='person-dropdown',
                                            options=[
                                            {'label': 'Janek Grzegorczyk', 'value': '1'},
                                            {'label': 'Elżbieta Kochalska', 'value': '2'},
                                            {'label': 'Albert Lisowski', 'value': '3'},
                                            {'label': 'Ewelina Nosowska', 'value': '4'},
                                            {'label': 'Piotr Fokalski', 'value': '5'},
                                            {'label': 'Bartosz Moskalski', 'value': '6'}
                                            ],
                                            value='1'
                                        ),
                                    ],
                                    className="dropdown",
                                ),

                                html.Div(
                                    [
                                        html.H2(
                                            "NAME",
                                            className="graph__title",
                                            id="person-name"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H2(
                                            "SURNAME",
                                            className="graph__title",
                                            id="person-surname"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H2(
                                            "YEAR OF BIRTH",
                                            className="graph__title",
                                            id="person-year"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H2(
                                            "DISABLED",
                                            className="graph__title",
                                            id="person-disabled"
                                        )
                                    ]
                                ),
                            ],
                            className="graph__container first",
                        ),
                        # table of measurements 
                        html.Div(
                            [
                                html.Div(
                                    [
                                        html.H6(
                                            "DESCRIPTION OF A GRAPHS", className="graph__title"
                                        )
                                    ]
                                ),
                                # dash_table.DataTable(
                                #     id='table-editing-simple',
                                #     columns=(
                                #     [{'id': 'Model', 'name': 'SENSOR'}] +
                                #     [{'id': p, 'name': p} for p in params]
                                #     ),
                                #     data=[
                                #     dict(Model=i, **{param: 0 for param in params})
                                #     for i in ["VALUE", "ANOMALY", "MEAN", "MIN", "MAX", "QARTILES", "RMS"]
                                #     ],
                                #     style_table={'border': 'thin lightgrey solid'},
                                #                     style_header={'backgroundColor':'lightgrey','fontWeight':'bold'},
                                #                     style_cell={'textAlign':'center','width':'12%'},
                                #                     style_data_conditional=[{
                                #                         'if' : {'filter':  'side eq "bid"' },
                                #                         'color':'blue'
                                #                                 }
                                #                         ]+[
                                #                         {
                                #                         'if' : {'filter': 'side eq "ask"' },
                                #                         'color':'rgb(203,24,40)'
                                #                     }]+[
                                #                         { 'if': {'row_index':'odd'},
                                #                         'backgroundColor':'rgb(242,242,242)'}
                                #                     ]+[
                                #                         {'if':{'column_id':'price'},
                                #                         'fontWeight':'bold',
                                #                         'border': 'thin lightgrey solid'}
                                #                     ]+[{'if':{'column_id':'from_mid'},
                                #                         'fontWeight':'bold'}
                                #                     ],
                                #                     style_as_list_view=True,
                                #     editable=True,
                                # ),

                                html.Div(
                                    [
                                        html.H1(
                                            " ",
                                            className="graph__title",
                                            #id="person-surname"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H1(
                                            "When NO ANOMALIES are detected points of a graph are violet.",
                                            className="graph__title",
                                            #id="person-surname"
                                        )
                                    ]
                                ),
                                html.Div(
                                    [
                                        html.H1(
                                            "When ANOMALY is detected points of a graph are red.",
                                            className="graph__title",
                                            #id="person-surname"
                                        )
                                    ]
                                ),
                            ],
                            className="graph__container second",
                        ),
                    ],
                    className="one-third column histogram__direction",
                ),
            ],
            className="app__content",
        ),
    ],
    className="app__container",
)

style=dict(
    plot_bgcolor=app_color["graph_bg"],
    paper_bgcolor=app_color["graph_bg"],
    font_color="white",
    title_font_size=18,
    title_font_color="white",
    xaxis=dict(
        title="DATE",
        linecolor=app_color["graph_bg"],  # Sets color of X-axis line
        showgrid=False,  # Removes X-axis grid lines
    ),
    yaxis=dict(
        title="VALUE",  
        linecolor=app_color["graph_bg"],  # Sets color of Y-axis line
        showgrid=False,  # Removes Y-axis grid lines    
    ),
)


def get_current_date():
    now = dt.datetime.now()
    total_date = (now.hour * 3600) + (now.minute * 60) + (now.second)
    return total_date

@app.callback(
    Output('person-name', 'children'),
    Output('person-surname', 'children'),
    Output('person-year', 'children'),
    Output('person-disabled', 'children'),
    [dash.dependencies.Input('person-dropdown', 'value')])
def update_output(value):
    df = select_people_by_id(value)
    #print(df)
    return 'NAME: {}'.format(df["name"][0]), 'SURNAME: {}'.format(df["surname"][0]), 'YEAR OF BIRTH: {}'.format(df["birth_year"][0]), 'DISABLED: {}'.format(bool(df["disabled"][0]))


def gen_diag(sensor_name, person_id):
    total_date = get_current_date()
    traces = select_traces(None, person_id)
    df = pd.DataFrame()
    for index, row in traces.iterrows():
        df = df.append(select_sensor_for_trace(None, row['id'], sensor_name))
    return df


@app.callback(
    Output("l0", "figure"),
    Output("l1", "figure"),
    Output("l2", "figure"),
    Output("r0", "figure"),
    Output("r1", "figure"),
    Output("r2", "figure"),
    [dash.dependencies.Input('person-dropdown', 'value')])
def draw_diag_for_person(value):
    for sensor_name in params:
        df = gen_diag(sensor_name, value)
        #print(df)
        data = {
        'time': [],
        'Altitude': [],
        'value1': [],
        'value2': []
    }
        figs[sensor_name] = go.Figure()
        figs[sensor_name].update_layout(title=sensor_name, xaxis_title="Time", yaxis_title="Value")
        figs[sensor_name].update_layout(style)
        #figs[sensor_name].add_trace(go.Scatter(x=df['date'], y=df['value'], mode="markers", name=sensor_name,))
        figs[sensor_name].add_trace(go.Scatter(x=df['date'].loc[df['anomaly'] != 1],y=df['value'],mode="markers",name="non-anomaly",))
        figs[sensor_name].add_trace(go.Scatter(x=df['date'].loc[df['anomaly'] == 1],y=df['value'],mode="markers",name="anomaly",))
    return figs["L0"], figs["L1"], figs["L2"], figs["R0"], figs["R1"], figs["R2"]

# Multiple components can update everytime interval gets fired.
# @app.callback(Output('live-update-graph', 'figure'),
#               Input('interval-component', 'n_intervals'))
# def update_graph_live(n):
#     satellite = Orbital('TERRA')
#     data = {
#         'time': [],
#         'Altitude': [],
#         'value1': [],
#         'value2': []
#     }

#     df = gen_diag('L1', 1)

#     # Collect some data
#     for i in range(df.shape[0]):
#         #df = gen_diag('L1', 1)
#         time = dt.datetime.now() - dt.timedelta(seconds=i*20)
#         time2 = datetime.now().timestamp()
#         #print(df)
#         if (df['anomaly'].iloc[i] == 0):
#              val1 = df.loc[df['anomaly'] == 0, 'value'].iloc[0]
#              data['value1'].append(val1)
#              data['time'].append(time2)
#         else: 
#              val2 = df.loc[df['anomaly'] == 1, 'value'].iloc[0]
#              data['value2'].append(val2)
#              data['time'].append(time2)
#         #val = df.loc[df['date'] == time2, 'value'].iloc[i]
#         #data['value1'].append(val1)
#         #data['value2'].append(val2)
#         #data['Altitude'].append(1+i)
#         #data['time'].append(time2)
#         #print(data)
#         #print("NEEEEEEEEEEEEEEEEEXT")

#     # Create the graph with subplots
#     fig = go.Figure()
#     fig.update_layout(style)
#     fig.add_trace({
#         'x': data['time'],
#         'y': data['value1'],
#         'name': 'Nonanomaly',
#         'mode': 'markers',
#         'type': 'scatter'
#     })
#     fig.add_trace({
#         'x': data['time'],
#         'y': data['value2'],
#         'name': 'Anomaly',
#         'mode': 'markers',
#         'type': 'scatter'
#     })
#     return fig


if __name__ == "__main__":
    #t = threading.Thread(target=get_data, args=[])
    #t.start()
    app.run_server()
    