# Usual Dash dependencies
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd

# callbacks here
from app import app

from apps import dbconnect as db

layout = html.Div(
    [
        html.H1([html.Span("\U0001F464", style={'margin-right': '0.5em'}), "MEMBERS"],
                style={'background-color': '#ffc404', 'text-align': 'center'}),
        html.Hr(),
        dbc.Card(  # Card Container
            [
                dbc.CardHeader(  # Define Card Header
                    [
                        html.H3('Manage Records')
                    ]
                ),
                dbc.CardBody(  # Define Card Contents
                    [
                        html.Div(  # Add Member Btn
                            [
                                # Add movie button will work like a
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Member",
                                    color='warning',
                                    href='/members/members_profile?mode=add',
                                    style={'margin-left': '10px'}
                                ),
                                dbc.Button(
                                    "View Member Details",
                                    color='primary',
                                    href='/members/members_home',
                                    style={'margin-left': '10px'}  # Adjust the margin as needed
                                ),
                                dbc.Button(
                                    "View Subscription",
                                    color='primary',
                                    href='/members/members_view',
                                    style={'margin-left': '10px'}
                                ),
                            ],
                            style={'display': 'flex'}  # Set display to flex for horizontal alignment
                        ),
                        html.Hr(),
                        html.Div(  # Create section to show list of movies
                            [
                                html.H4('Find Member'),
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dbc.Form(
                                                dbc.Row(
                                                    [
                                                        dbc.Label("Search Member", width=2),
                                                        dbc.Col(
                                                            dbc.Input(
                                                                type='text',
                                                                id='memberhome_view_titlefilter',
                                                                placeholder='Member Name'
                                                            ),
                                                            width=4
                                                        )
                                                    ],
                                                    className='mb-3'
                                                )
                                            ),
                                        ),
                                    ],
                                    justify="between",  # Align items to the space between the start and end of the container
                                ),
                                html.Div(
                                    "Table with members will go here.",
                                    id='memberhome_memberview'
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
        Output('memberhome_memberview', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('memberhome_view_titlefilter', 'value'),
    ]
)
def memberhome_loadmemberlist(pathname, searchterm):
    if pathname == '/members/members_home_view':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """
            SELECT 
                mi.member_fname, 
                mi.member_mname, 
                mi.member_lname, 
                mi.subscription_amount_paid,  -- New column
                mi.date_added,   -- New column
                to_char(mi.date_added + INTERVAL '365 days', 'YYYY-MM-DD') as subscription_valid_until  -- New column
            FROM 
                member_info mi
            JOIN
                membershiptype mt ON mi.typeid = mt.typeid
            WHERE 
                mi.member_delete_ind = FALSE  -- Exclude deleted members
                AND mt.membership != 'Walk-in'  -- Exclude Walk-in members
        """

        values = []
        cols = ['First Name', 'Middle Name', 'Last Name', 'Amount Paid', 'Date Added', 'Subscription Valid Until']

        if searchterm:
            sql += " AND (member_fname ILIKE %s OR member_lname ILIKE %s)"
            values += [f"%{searchterm}%", f"%{searchterm}%"]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')

            return [table]
        else:
            return ["No Records to Display"]
    else:
        raise PreventUpdate
