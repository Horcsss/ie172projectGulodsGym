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


dropdown_button_style = {
    'background-color': '#ffffff',
    'color': '#dark',
    'font-size': 'medium',
    'padding': '0.2rem 0.5rem',  # Adjust padding
    'border-radius': '0.25rem',  # Add border-radius for rounded corners
}

sort_add = dbc.DropdownMenu(
    children=[
        dbc.DropdownMenuItem("No filter", href="/classes/classes_home"),
        dbc.DropdownMenuItem("Classes A-Z", href="/classes/classes_home_atoz"),
        dbc.DropdownMenuItem("Classes Z-A", href="/classes/classes_home_ztoa"),
        dbc.DropdownMenuItem("Instructor A-Z", href="/classes/classes_home_instructor_atoz"),
        dbc.DropdownMenuItem("Instructor Z-A", href="/classes/classes_home_instructor_ztoa"),
    ],
    nav=True,
    in_navbar=True,
    label="Sort Classes by Z to A",
    style=dropdown_button_style,
)

layout = html.Div(
    [
        html.H1([html.Span("\U0001F94B", style={'margin-right': '0.5em'}), "CLASSES"], 
        style={'background-color': '#ffc404', 'text-align': 'center'}),
        html.Hr(),
        dbc.Card( # Card Container
            [
                dbc.CardHeader( # Define Card Header
                    [
                        html.H3('Manage Classes')
                    ]
                ),
                dbc.CardBody( # Define Card Contents
                    [
                        html.Div( # Add Member Btn
                            [
                                # Add class button will work like a
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Class",
                                    color = 'warning',
                                    href='/classes/classes_list?mode=add'
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.Div( # Create section to show list of classes
                            [
                                html.H4('Search for a class'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Search Classs", width= 2),
                                                        dbc.Col(
                                                            dbc.Input(
                                                                type='text',
                                                                id='classhome_titlefilter_ztoa',
                                                                placeholder='Class Name'
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
                                    justify="between",  # Align items to the space between the start and end of the container
                                ),
                                html.Div(
                                    "Table with classes will go here.",
                                    id='classhome_classlist_ztoa'
                                )
                            ]
                        )
                    ]
                )
            ]
        )
    ]
)

# Table
@app.callback(
    [
        Output('classhome_classlist_ztoa', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('classhome_titlefilter_ztoa', 'value'),
    ]
)
def classhome_loadclasslist(pathname, searchterm):
    if pathname == '/classes/classes_home_ztoa':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ 
            SELECT 
                class_name, 
                class_description, 
                CONCAT(instructor_fname, ' ', instructor_lname) as instructor_name, 
                schedule, 
                rates, 
                c.class_id
            FROM 
                class_info c
            LEFT JOIN 
                instructor_info i on c.instructor_id = i.instructor_id
            WHERE 
                (NOT class_delete_ind OR c.instructor_id IS NULL)
                AND (
                    (%s IS NULL OR class_name ILIKE %s) 
                    OR (%s IS NULL OR instructor_fname ILIKE %s) 
                    OR (%s IS NULL OR instructor_lname ILIKE %s)
                    OR (COALESCE(%s::text, '') = '' OR COALESCE(schedule::text, '') ILIKE %s)
                    OR (COALESCE(%s::text, '') = '' OR COALESCE(rates::text, '') ILIKE %s)
                )
            ORDER BY class_name DESC;  -- Add ORDER BY clause for sorting
        """
        values = [searchterm, f"%{searchterm}%", searchterm, f"%{searchterm}%", searchterm, f"%{searchterm}%",
                  searchterm, f"%{searchterm}%", searchterm, f"%{searchterm}%"]
        cols = ['Class Name', 'Class Description', 'Instructor Name', 'Schedule', 'Rates', 'ID']

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:
            buttons = []
            for class_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'classes_list?mode=edit&id={class_id}',
                                   size='sm', color='warning'
                                   ),
                        style={'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons

            df = df[['Class Name', 'Class Description', 'Instructor Name', 'Schedule', 'Rates', "Action"]]

            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

            return [table]
        else:
            return ["No Records to Display"]
    else:
        raise PreventUpdate
