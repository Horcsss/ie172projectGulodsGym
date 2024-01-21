# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

# callbacks here
from app import app

from apps import dbconnect as db

# store the layout objects into a variable named layout
layout = html.Div(
    [
        html.H1([html.Span("🏋️‍♂️", style={'margin-right': '0.5em'}), "INSTRUCTORS"], 
        style={'background-color': '#ffc404', 'text-align': 'center'}),
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Manage Records')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Div( # Button Div
                            [
                                dbc.Button(
                                    "Add Instructor",
                                    color='warning',
                                    href='/instructors/instructors_profile?mode=add'
                                ),
                                dbc.Button(
                                    "View Instructor Details",
                                    color='primary',
                                    href='/instructors/instructors_home',
                                    style={'margin-left': '10px'}  # Adjust the margin as needed
                                ),
                                 dbc.Button(
                                    "View Instructor Classes",
                                    color='primary',
                                    href='/instructors/instructors_classes',
                                    style={'margin-left': '10px'}  # Adjust the margin as needed
                                ),
                            ],
                            style={'display': 'flex'}  # Set display to flex for horizontal alignment
                        ),
                        html.Hr(),
                        html.Div( 
                            [
                                html.H4('Find Instructor'),
                                html.Div(
                                    dbc.Form(
                                        dbc.Row(
                                            [
                                                dbc.Label("Search Instructor or Class", width= 2),
                                                dbc.Col(
                                                    dbc.Input(
                                                        type='text',
                                                        id='instructorclasses_titlefilter',  # Corrected ID
                                                        placeholder='Instructor Name or Class Name'
                                                    ),
                                                    width=4
                                                )
                                            ],
                                            className = 'mb-3'
                                        )
                                    )
                                ),
                                html.Div(
                                    "Table with instructors will go here.",
                                    id='instructorclasses_instructorclasses'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)
@app.callback(
    [Output('instructorclasses_instructorclasses', 'children')],
    [Input('url', 'pathname'), Input('instructorclasses_titlefilter', 'value')]
)
def instructorclasses_loadinstructorlist(pathname, searchterm):
    if pathname == '/instructors/instructors_classes':
        if not searchterm:  # If searchterm is None or an empty string, show all records
            sql = """
                SELECT
                    i.instructor_id,
                    CONCAT(i.instructor_fname, ' ', i.instructor_lname) AS "Instructor",
                    ARRAY_TO_STRING(ARRAY_AGG(c.class_name), ', ') AS "Handled Classes"
                FROM
                    instructor_info i
                LEFT JOIN
                    class_info c ON i.instructor_id = c.instructor_id
                GROUP BY
                    i.instructor_id, i.instructor_fname, i.instructor_lname;
            """
            values = []
        else:  # If searchterm is provided, filter records based on the search term
            sql = """
                SELECT
                    i.instructor_id,
                    CONCAT(i.instructor_fname, ' ', i.instructor_lname) AS "Instructor",
                    ARRAY_TO_STRING(ARRAY_AGG(c.class_name), ', ') AS "Handled Classes"
                FROM
                    instructor_info i
                LEFT JOIN
                    class_info c ON i.instructor_id = c.instructor_id
                WHERE
                    i.instructor_fname ILIKE %s
                    OR i.instructor_lname ILIKE %s
                    OR c.class_name ILIKE %s
                GROUP BY
                    i.instructor_id, i.instructor_fname, i.instructor_lname;
            """
            searchterm_ilike = f"%{searchterm}%"  # Prepare the search term with % for ILIKE
            values = [searchterm_ilike, searchterm_ilike, searchterm_ilike]

        dfcolumns = ['instructor_id', 'Instructor', 'Handled Classes']
        df = db.querydatafromdatabase(sql, values, dfcolumns)

        if df.shape:
            df = df[['Instructor', 'Handled Classes']]
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No Records to Display"]
    else:
        raise PreventUpdate
