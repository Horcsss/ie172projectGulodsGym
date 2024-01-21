# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

from app import app
from apps import dbconnect as db


layout = html.Div(
    [
        html.H1("WELCOME TO GULOD'S GYM INFORMATION SYSTEM!", style={'text-align': 'center'}),
        html.Hr(),
        html.Div(
            [
                dbc.Row(
                    [
                        html.H5(
                            'With this application, you can manage and track member information, class details, instructor data, and many more.',
                            style={'text-align': 'center', 'fontSize': '100%'}
                        ),
                    ],
                    align="center",
                ),
                html.Br(),
                html.H2("What do you want to manage?", style={'backgroundColor': '#ffc404', 'text-align': 'center', 'outline': 'true'}),
                html.Hr(),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4("Members", style={'color': 'white'})),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(dbc.Col(html.Div("This page allows you to manage the members of the gym.",
                                                                    style={'color': 'white'}))),
                                            dbc.Row(),
                                            dbc.Row(dbc.Col(html.Div("Edit the members information here.",
                                                                    style={"font-style": "italic", 'color': 'white'}))),
                                            html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "white","opacity": "unset"}),
                                            dbc.Button('Proceed', color="warning", href='/members/members_home'),

                                       ]
                                    ),
                                ],
                                style={"margin-bottom": "30px", 'background-color': '#5A5A5A'}
                            ),
                        ),  
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4("Attendance", style={'color': 'white' })),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(dbc.Col(html.Div("This page allows you to track the attendance.",
                                                                    style={'color': 'white'}))),
                                            dbc.Row(),
                                            dbc.Row(dbc.Col(html.Div("Add and edit entries here.",
                                                                    style={"font-style": "italic", 'color': 'white'}))),
                                            html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "white","opacity": "unset"}),
                                            dbc.Button('Proceed', color="warning", href='/attendance/attendance_home'),

                                        ]
                                    ),
                                ],
                                style={"margin-bottom": "30px", 'background-color': '#5A5A5A'}
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(html.H4("Classes", style={'color': 'white'})),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(dbc.Col(html.Div("This page allows you to manage class information.",
                                                                    style={'color': 'white'}))),
                                            dbc.Row(),
                                            dbc.Row(dbc.Col(html.Div("Edit the class information here.",
                                                                    style={"font-style": "italic", 'color': 'white'}))),
                                            html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "white","opacity": "unset"}),
                                            dbc.Button('Proceed', color="warning", href='/classes/classes_home'),

                                        ]
                                    ),
                                ],
                                style={"margin-bottom": "30px", 'background-color': '#5A5A5A'}
                            ),
                        ),
                    ],
                    style={'text-align': 'center'}
                ),
                dbc.Row([
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Instructors", style={'color': 'white'})),
                                dbc.CardBody(
                                    [
                                        dbc.Row(dbc.Col(html.Div("This page allows you to manage the instructor information.",
                                                                style={'color': 'white'}))),
                                        dbc.Row(),
                                        dbc.Row(dbc.Col(html.Div("Edit the instructor information here.",
                                                                style={"font-style": "italic", 'color': 'white'}))),
                                        html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "white","opacity": "unset"}),
                                        dbc.Button('Proceed', color="warning", href='/instructors/instructors_home'),

                                    ]
                                ),
                            ],
                            style={'background-color': '#5A5A5A'}
                        ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Reports", style={'color': 'white'})),
                                dbc.CardBody(
                                    [
                                        dbc.Row(dbc.Col(html.Div("This page contains the summary of the transactional reports.",
                                                                style={'color': 'white'}))),
                                        dbc.Row(),
                                        dbc.Row(dbc.Col(html.Div("Access the reports here.",
                                                                style={"font-style": "italic", 'color': 'white'}))),
                                        html.Hr(style={'borderWidth': "5vh", "width": "100%", "borderColor": "white","opacity": "unset"}),
                                        dbc.Button('Proceed', color="warning", href='reports/report'),

                                    ]
                                ),
                            ],
                            style={'background-color': '#5A5A5A'}
                        ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            [
                                dbc.CardHeader(html.H4("Contact Information", style={'color': 'white'})),
                                dbc.CardBody(
                                    [
                                        dbc.Row(dbc.Col(html.Div(
                                            [
                                                html.Span("📞", "Phone:", style={"font-weight": "bold", "text-align": "left"}),
                                                " 0956-9659-413"
                                            ],
                                            className="card-text", style={'color': 'white'}))),
                                        dbc.Row(dbc.Col(html.Div(
                                            [
                                                html.Span("🌐", "Facebook:", style={"font-weight": "bold", "text-align": "left"}),
                                                " https://www.facebook.com/GulodsGym"
                                            ],
                                            className="card-text", style={'color': 'white'}))),
                                        dbc.Row(dbc.Col(html.Div(
                                            [
                                                html.Span("📍", "Location:", style={"font-weight": "bold", "text-align": "left"}),
                                                " Tiburcio St. Brgy. Krus na Ligas, Quezon City",
                                            ],
                                            className="card-text", style={'color': 'white'}))),
                                        html.Hr(style={'border-color': 'white'}),
                                    ]
                                ),
                            ],
                            style={'background-color': '#5A5A5A'}
                        ),
                    ),

                ],
                    style={'text-align': 'center'}),
                html.Br(),
                html.Hr(),
                html.Span(
                    "Please contact the owner of the site if you need assistance.",
                    style={'font-style': 'italic', 'fontSize': '70%', 'color': 'black'}
                ),
            ]
        )
    ]
)
