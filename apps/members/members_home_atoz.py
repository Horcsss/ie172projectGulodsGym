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
        dbc.DropdownMenuItem("No filter", href="/members/members_home"),
        dbc.DropdownMenuItem("A-Z", href="/members/members_home_atoz"),
        dbc.DropdownMenuItem("Z-A", href="/members/members_home_ztoa"),
        dbc.DropdownMenuItem("Walk-in", href="/members/members_home_walkin"),
        dbc.DropdownMenuItem("Member", href="/members/members_home_member"),
    ],
    nav=True,
    in_navbar=True,
    label="Sort Members from A to Z (First Name)",
    style=dropdown_button_style,
)


layout = html.Div(
    [
        html.H1([html.Span("\U0001F464", style={'margin-right': '0.5em'}), "MEMBERS"], 
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
                        html.Div( # Add Member Btn
                            [
                                # Add member button will work like a
                                # hyperlink that leads to another page
                                dbc.Button(
                                    "Add Member",
                                    color='warning',
                                    href='/members/members_profile?mode=add'
                                ),
                            ]
                        ),
                        html.Hr(),
                        html.Div( # Create section to show list of movies
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
                                                                id='memberhome_titlefilter_atoz',
                                                                placeholder='Member Name'
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
                                    "Table with members will go here.",
                                    id='memberhome_memberlist_atoz'
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
        Output('memberhome_memberlist_atoz', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('memberhome_titlefilter_atoz', 'value'),
    ]
)

def memberhome_loadmemberlist(pathname, searchterm):
    if pathname == '/members/members_home_atoz':
        # 1. Obtain records from the DB via SQL
        # 2. Create the html element to return to the Div
        sql = """ SELECT member_fname, member_mname, member_lname, member_address,member_contactnumber,
                         member_birthdate, member_email, member_medicaldetails, member_emergencycontact,
                         member_emergencycontactnumber, sex_name, civil_status, membership, member_id
            FROM member_info m
                INNER JOIN member_sex s on m.sex_id = s.sex_id
                INNER JOIN civilstatus c on m.civilstatus_id = c.civilstatus_id
                INNER JOIN membershiptype t on m.typeid = t.typeid
            WHERE NOT member_delete_ind
        """

        values = []
        cols = ['First Name','Middle Name', 'Last Name', 'Address', 'Contact Number', 'Date of Birth', 'Email', 'Medical Details', 'Emergency Contact',
                'Emergency Contact Number', 'Sex', 'Civil Status', 'Membership Type', 'ID']

        if searchterm:
            sql += " AND (member_fname ILIKE %s OR member_lname ILIKE %s)"
            values += [f"%{searchterm}%", f"%{searchterm}%"]

        sql += " ORDER BY member_fname"
        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape:

            buttons = []
            for member_id in df['ID']:
                buttons += [
                    html.Div(
                        dbc.Button('Edit', href=f'members_profile?mode=edit&id={member_id}',
                                            size = 'sm', color = 'warning'
                        ),
                        style = {'text-align': 'center'}
                    )
                ]
            df['Action'] = buttons
            
            df = df[['First Name','Middle Name', 'Last Name', 'Address', 'Contact Number', 'Date of Birth', 'Email', 'Medical Details', 'Emergency Contact',
                'Emergency Contact Number', 'Sex', 'Civil Status', 'Membership Type', "Action"]]

            table = dbc.Table.from_dataframe(df, striped = True, bordered = True, hover = True, size = 'sm')
        
            return [table]
        else:
            return ["No Records to Display"]
    else:
        raise PreventUpdate
