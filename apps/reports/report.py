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
        html.H1([html.Span("📊", style={'margin-right': '0.5em'}), "REPORTS"],
                style={'background-color': '#ffc404', 'text-align': 'center'}),
        html.Hr(),

        # Row 1
dbc.Row(
    [
        dbc.Col(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H3('Sales of Membership Type')),
                                        dbc.CardBody(
                                            [
                                                html.Hr(),
                                                html.Div(id='report_transact')
                                            ]
                                        )
                                    ]
                                ),
                            ],
                            title='Sales of Membership Type'
                        ),
                    ]
                ),
                html.Br(),  # Add space below the accordion
            ]
        ),
        dbc.Col(
            [
                dbc.Accordion(
                    [
                        dbc.AccordionItem(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(html.H3('Sales per Class per Month')),
                                        dbc.CardBody(
                                            [
                                                html.Hr(),
                                                html.H4(
                                                    dbc.Form(
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    dcc.Dropdown(
                                                                           id='month_filter',
                                                                            options=[
                                                                                {'label': 'January', 'value': 1},
                                                                                {'label': 'February', 'value': 2},
                                                                                {'label': 'March', 'value': 3},
                                                                                {'label': 'April', 'value': 4},
                                                                                {'label': 'May', 'value': 5},
                                                                                {'label': 'June', 'value': 6},
                                                                                {'label': 'July', 'value': 7},
                                                                                {'label': 'August', 'value': 8},
                                                                                {'label': 'September', 'value': 9},
                                                                                {'label': 'October', 'value': 10},
                                                                                {'label': 'November', 'value': 11},
                                                                                {'label': 'December', 'value': 12},
                                                                        ],
                                                                        placeholder='Select a month',
                                                                        multi=False,
                                                                        value=None,
                                                                        style={'font-size': '14px', 'font-family': 'Arial, sans-serif'}
                                                                    ), width=4
                                                                )
                                                            ]
                                                        )
                                                    )
                                                ),
                                                html.Div(id='report_salesmonthly')
                                            ]
                                        )
                                    ]
                                ),
                            ],
                            title='Sales per Class per Month'
                        ),
                    ]
                ),
                html.Br(),  # Add space below the accordion
            ]
        ),
    ]
),
        # Row 2
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3('Age Group of Attendees per Class')),
                                                dbc.CardBody(
                                                    [
                                                        html.Hr(),
                                                        html.H4(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                type='text',
                                                                                id='class_filter',
                                                                                placeholder='Search Class Here'
                                                                            ), width=4
                                                                        )
                                                                    ]
                                                                )
                                                            )
                                                        ),
                                                        html.Div(
                                                            id='report_agegroup'
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    title='Age Group of Attendees per Class'
                                ),
                            ]
                        ),
                        html.Br(),  # Add space below the accordion
                    ]
                ),
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3('Number of Attendees per Membership type Per Class')),
                                                dbc.CardBody(
                                                    [
                                                        html.Hr(),
                                                        html.H4(
                                                            dbc.Form(
                                                                dbc.Row(
                                                                    [
                                                                        dbc.Col(
                                                                            dbc.Input(
                                                                                type='text',
                                                                                id='class2_filter',
                                                                                placeholder='Search Class Here'
                                                                            ), width=4
                                                                        )
                                                                    ]
                                                                )
                                                            )
                                                        ),
                                                        html.Div(
                                                            id='report_membership'
                                                        )
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    title='Number of Attendees per Membership type Per Class'
                                ),
                            ]
                        ),
                        html.Br(),  # Add space below the accordion
                    ]
                ),
            ]
        ),

        # Row 3
        dbc.Row(
            [
                dbc.Col(
                    [
                        dbc.Accordion(
                            [
                                dbc.AccordionItem(
                                    [
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(html.H3('Number of Attendees Per Day')),
                                                dbc.CardBody(
                                                    [
                                                        html.Div([
                                                            dcc.Loading(
                                                                id="reportbodyload",
                                                                children=[
                                                                    dcc.Graph(id='graph_report',)
                                                                ], type="circle")
                                                        ], style={'width': '100%', "border": "3px #5c5c5c solid", }),
                                                    ]
                                                )
                                            ]
                                        ),
                                    ],
                                    title='Number of Attendees Per Day'
                                ),
                            ]
                        ),
                        html.Br(),  # Add space below the accordion
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
        sql = """ SELECT membership, (count(a.amount_paid))
                    FROM attendance a
                    INNER JOIN membershiptype m ON a.typeid = m.typeid
                    GROUP BY membership;
        """
        values = []
        cols = ['Membership Type','Number of Sales']
        
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
            return [table]
        else:
            return["No Records"]
    else:
        raise PreventUpdate



# Table and query for Sales per Class per Month
@app.callback(
    [
        Output('report_salesmonthly', 'children')
    ],
    [
        Input('url', 'pathname'),
        Input('month_filter', 'value')
    ]
)
def monthlysales(pathname, searchterm):
    if pathname == '/reports/report':
        values = []
        cols = ['Month', 'Year', 'Class Name', 'Total Sales']

        if searchterm:
            sql = """
                SELECT
                    EXTRACT(MONTH FROM a.timein) AS month,
                    EXTRACT(YEAR FROM a.timein) AS year,
                    c.class_name,
                    SUM(a.amount_paid) AS total_sales
                FROM
                    attendance a
                JOIN
                    class_info c ON a.class_id = c.class_id
                WHERE
                    EXTRACT(MONTH FROM a.timein) = %s
                GROUP BY
                    EXTRACT(MONTH FROM a.timein),
                    EXTRACT(YEAR FROM a.timein),
                    c.class_name
                ORDER BY
                    year, month, c.class_name;
            """
            values += [searchterm]

        df = db.querydatafromdatabase(sql, values, cols)

        if df.shape[0]:
            table = dbc.Table.from_dataframe(df, striped=True, bordered=True, hover=True, size='sm')
            return [table]
        else:
            return ["No Records to Display"]
    else:
        raise PreventUpdate

#Table and Query for Age Group of Attendees per Class
@app.callback(
    [
        Output('report_agegroup','children')
    ],
    [
        Input('url','pathname'),
        Input('class_filter','value')
    ]
)
def dailyattendees(pathname,searchterm):
    if pathname == '/reports/report':
        values = []
        cols = ['Minor(<18)','Young Adult(18-39)','Middle Aged(40-59)','Senior(>59)']
        if searchterm:
            sql = """ with mem_age as (Select date_part('year', age(member_birthdate)) as mage
                        FROM attendance a
                            INNER JOIN class_info ci ON a.class_id = ci.class_id
                            INNER JOIN member_info mi ON a.member_id = mi.member_id
                            AND class_name ILIKE %s)
                    (Select count(*) filter (where mage<18) as minor, count(*) filter (where mage>=18 and mage<39) as YA,
                        count(*) filter (where mage>=39 and mage<59) as Adult, count(*) filter (where mage>=59) as Senior
                        FROM mem_age)"""
            values += [f"%{searchterm}%"]   
        #sql+= """ Group By class_name"""
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
           table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
           return[table] 
        else:
            return["No Records to Display"]
    else:
        raise PreventUpdate

#Table and query for Number of Attendees per membership type per Class
@app.callback(
    [
        Output('report_membership','children')
     ],
    [
        Input('url','pathname'),
        Input('class2_filter','value')
    ]
)
def memattendees(pathname, searchterm):
    if pathname == '/reports/report':
        values = []
        cols = ['Membership','Attendees Count']
        if searchterm:
            sql = """ SELECT membership, count(distinct(attendance_id))
                        FROM attendance a
                            INNER JOIN class_info c ON a.class_id = c.class_id
                            INNER JOIN member_info m ON a.member_id = m.member_id
                            INNER JOIN membershiptype mt ON a.typeid = mt.typeid 
                            AND class_name ILIKE %s"""
            values += [f"{searchterm}%"]   
        sql+= """Group By membership"""
        df = db.querydatafromdatabase(sql, values, cols)
        if df.shape[0]:
           table = dbc.Table.from_dataframe(df, striped=True, bordered=True,
                    hover=True, size='sm')
           return[table] 
        else:
            return["No Records to Display"]
    else:
        raise PreventUpdate

#Graph for Number of Attendees Per Day
@app.callback(
    [
        Output('graph_report','figure')
    ],
    [
        Input('url','pathname')
    ]
)
def graphday(pathname):
    if pathname == '/reports/report':
        sql = """ Select count(distinct(member_id)), text(extract(DOY FROM timein))
                FROM attendance
                    Group by timein
        """
        values = []
        cols = ['CountA', 'timeindate']
        df = db.querydatafromdatabase(sql, values, cols)
        df = df[['CountA','timeindate']]
        listofdates = df["timeindate"].unique().tolist()
        
        traces = {}
        for indate in listofdates:
            traces['tracebar_' + indate] = go.Scatter(y=df[df["timeindate"]==indate]["CountA"],
                                                  x=df[df["timeindate"]==indate]["timeindate"],
                                                  name=indate)
        data = list(traces.values())
        layout = go.Layout(
                yaxis={'categoryorder':'total ascending', 'title':"Number of Attendees"},
                xaxis={'title':"Day of the Year", "mirror":False, "zeroline":True },
                height=300,
                width = 1000,
                margin={'b': 50,'t':20, 'l':175},
                hovermode='closest',
                autosize= True,
                dragmode = 'zoom',
                scattermode='group',
                boxmode= "overlay",
                )


        figure3 = {'data':data, 'layout':layout }
        if df.shape[0]:
            return[figure3]
        else:
            return['No Figure']
    else:
        raise PreventUpdate



