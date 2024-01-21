from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash import dash_table
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import pandas as pd
import plotly.graph_objs as go

from app import app
from apps import dbconnect as db

layout = html.Div(
    [
        html.H2('Reports'),
        html.Hr(),
        dbc.Card(
            [
                dbc.CardBody( 
                    [
                        html.Div(
                            [
                                html.H5('Sales of Membership Type'),
                                html.Div(
                                    id='report_transact'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H5('Sales per Class per Month'),
                                html.H4(
                            dbc.Form(
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            dcc.Dropdown(
                                                id='month_filter',
                                                options=[
                                                    {'label': 'January', 'value': 'January'},
                                                    {'label': 'February', 'value': 'February'},
                                                    {'label': 'March', 'value': 'March'},
                                                    {'label': 'April', 'value': 'April'},
                                                    {'label': 'May', 'value': 'May'},
                                                    {'label': 'June', 'value': 'June'},
                                                    {'label': 'July', 'value': 'July'},
                                                    {'label': 'August', 'value': 'August'},
                                                    {'label': 'September', 'value': 'September'},
                                                    {'label': 'October', 'value': 'October'},
                                                    {'label': 'November', 'value': 'November'},
                                                    {'label': 'December', 'value': 'December'},
                                                ],
                                                placeholder='Select a month',
                                                multi=False,
                                                value=None,
                                                style={'font-size': '14px', 'font-family': 'Arial, sans-serif'}
                                            ),
                                            width=4
                                        )
                                    ]
                                )
                            )
                        ),
                                html.Div(
                                    id='report_salesmonthly'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H5('Age Group of Attendees per Class'),
                                html.Div(
                                    id='report_movielist'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H5('Number of Attendees per Membership type Per Class'),
                                html.Div(
                                    id='report_movielist'
                                )
                            ]
                        ),
                        html.Hr(),
                        html.Div(
                            [
                                html.H5('Number of Attendees Per Day'),
                                html.Div(
                                    id='report_movielist'
                                )
                            ]
                        )
                        
                    ]
                )
            ]
        )
    ]
)

#Table for Sales of Membership Type
@app.callback(
    [
        Output('report_transact','children')
     ],
    [
        Input('url','pathname')
    ]
)
def memtype(pathname):
    if pathname == '/reports/report':
        sql = """ SELECT  membership, count(distinct(transact_id))
            FROM transact t
                INNER JOIN membershiptype m ON t.typeid = m.typeid
                Group By membership    
        """
        values = []
        cols = ['Membership Type', 'Number of Sales']

        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                             hover=True, size='sm')
            return [table]
        else:
            return ["No Records"]
    else:
        raise PreventUpdate

#Table and query for Sales per Class per Month  
@app.callback(
    [
        Output('report_salesmonthly','children')
     ],
    [
        Input('url','pathname'),
        Input('month_filter','value')
    ]
)
def monthlysales(pathname, searchterm):
    if pathname == '/reports/report':
        # Define sql before attempting to concatenate
        sql = """ SELECT class_name, SUM(transactionamount)
                        FROM classtransactions t
                            INNER JOIN class_info c ON t.class_id = c.class_id
                            INNER JOIN months m ON t.month_id = m.month_id 
                            AND transactionmonth ILIKE %s"""
        values = [None]  # Initialize with None
        cols = ['Class', 'Sales for Specific Month']
        if searchterm:
            values[0] = f"{searchterm}%"  # Update the first element if searchterm is provided
        sql += """ GROUP BY class_name, transactionmonth"""
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                                             hover=True, size='sm')
            return [table]
        else:
            return ["No Records to Display"]
    else:
        raise PreventUpdate

#Table for Age Group of Attendees per Class

#Table and query for Number of Attendees per membership type per Class

#Table for Number of Attendees Per Day