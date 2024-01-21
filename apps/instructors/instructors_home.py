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

dropdown_button_style = {
    'background-color': '#ffffff',
    'color': '#dark',
    'font-size': 'medium',
    'padding': '0.2rem 0.5rem',  # Adjust padding
    'border-radius': '0.25rem',  # Add border-radius for rounded corners
}

sort_add = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("No filter", href="/instructors/instructors_home"),
        dbc.DropdownMenuItem("Instructor A-Z", href="/instructors/instructors_home_atoz"),
        dbc.DropdownMenuItem("Instructor Z-A", href="/instructors/instructors_home_ztoa"),
    ],
    nav=True,
    in_navbar=True,
    label="Sort by",
    style=dropdown_button_style,
)

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
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Search Instructor", width= 2),
                                                        dbc.Col(
                                                            dbc.Input(
                                                                type='text',
                                                                id='instructorhome_titlefilter',
                                                                placeholder='Instructor Name'
                                                            ),
                                                            width=4
                                                        )
                                                    ],
                                                    className='mb-3'
                                                )
                                            ),
                                        ),
                                        dbc.Col(
                                            sort_add,  # Place the sorting options here
                                            width="auto",  # Set the width to auto to adjust the size
                                            style={'margin-left': 'auto'},  # Align to the right
                                        ),
                                    ],
                                ),
                                html.Div(
                                    "Table with instructors will go here.",
                                    id='instructorhome_instructorlist'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)


#Table
@app.callback(
    [
        Output('instructorhome_instructorlist', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('instructorhome_titlefilter', 'value'),
    ]
)

def instructorhome_loadinstructorlist(pathname, searchterm):
    if pathname == '/instructors/instructors_home':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ SELECT instructor_fname, instructor_lname, instructor_address, instructor_contactnumber,
                         instructor_birthdate, instructor_email, sex_name, civil_status, i.instructor_id
            FROM instructor_info i
                INNER JOIN member_sex s on i.instructor_sex_id = s.sex_id
                INNER JOIN civilstatus c on i.instructor_civilstatus_id = c.civilstatus_id
            WHERE NOT instructor_delete_ind
        """
        values = []
        cols = ['First Name', 'Last Name', 'Address', 'Contact Number', 'Date of Birth', 'Email',
                    'Sex', 'Civil Status', 'ID']

        if searchterm:
            sql += "AND instructor_fname ILIKE %s"
            values += [f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:

            buttons = []
            for instructor_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'instructors_profile?mode=edit&id={instructor_id}',
                                            size = 'sm', color = 'warning'
                        ),
                        style = {'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            
            df = df[['First Name', 'Last Name', 'Address', 'Contact Number', 'Date of Birth', 'Email',
                    'Sex', 'Civil Status', "Action"]]

            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm')
        
            return [table]
        else:
            return ["No Records to Display"]
    else:
        raise PreventUpdate
    
