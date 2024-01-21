# Dash related dependencies
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

# To open browser upon running your app
import webbrowser

from app import app
from apps import commonmodules as cm
from apps.members import members_home, members_profile, members_home_atoz, members_home_ztoa,   members_home_walkin, members_home_member, members_home_view
from apps.classes import classes_home, classes_list, classes_home_class_atoz, classes_home_class_ztoa, classes_home_instructor_atoz, classes_home_instructor_ztoa
from apps.instructors import instructors_home, instructors_profile, instructors_classes, instructors_home_atoz, instructors_home_ztoa
from apps.home import homepage
from apps import login, signup
from apps.attendance import attendance_list, attendance_home
from apps.reports import report
from apps.aboutus import about_us

from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
import dash
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate
import webbrowser


CONTENT_STYLE = {
    "margin-top": "1em",
    "margin-left": "1em",
    "margin-right": "1em",
    "padding": "1em 1em",
}

app.layout = html.Div(
    [
        dcc.Location(id='url', refresh=True),

        # LOGIN DATA
        # 1) logout indicator, storage_type='session' means that data will be retained
        #  until browser/tab is closed (vs clearing data upon refresh)
        dcc.Store(id='sessionlogout', data=False, storage_type='session'),
        
        # 2) current_user_id -- stores user_id
        dcc.Store(id='currentuserid', data=-1, storage_type='session'),
        
        # 3) currentrole -- stores the role
        # we will not use them but if you have roles, you can use it
        dcc.Store(id='currentrole', data=-1, storage_type='session'),

        html.Div(
            cm.navbar,
            id='navbar_div'
        ),

        # Page Content -- Div that contains page layout  
        html.Div(id='page-content', style=CONTENT_STYLE),
    ]
)


@app.callback(
    [
        Output('page-content', 'children'),
        Output('navbar_div', 'style'),
        Output('sessionlogout', 'data'),
    ],
    [
        Input('url', 'pathname'),
    ],
    [
        State('sessionlogout', 'data'),
        State('currentuserid', 'data'),
    ]
)
def displaypage(pathname, sessionlogout, currentuserid):
    ctx = dash.callback_context
    if ctx.triggered:
        eventid = ctx.triggered[0]['prop_id'].split('.')[0]
    else:
        raise PreventUpdate

    print(f"Event ID: {eventid}, Current User ID: {currentuserid}, Pathname: {pathname}")

    if currentuserid < 0:
        if pathname in ['/', '/login', '/signup']:
            if pathname == '/signup':
                return signup.layout, {'display': 'none'}, sessionlogout
            else:
                return login.layout, {'display': 'none'}, sessionlogout
        else:
            return 'Please log in', {'display': 'none'}, sessionlogout
    else:
        if pathname == '/logout':
            return login.layout, {'display': 'none'}, True
        elif pathname == '/home':
            return homepage.layout, {'display': 'unset'}, sessionlogout

        elif pathname == '/members/members_home':
            return members_home.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/members/members_home_atoz':
            return members_home_atoz.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/members/members_home_ztoa':
            return members_home_ztoa.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/members/members_home_walkin':
            return members_home_walkin.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/members/members_home_member':
            return members_home_member.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/members/members_profile':
            return members_profile.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/members/members_home_view':
            return members_home_view.layout, {'display': 'unset'}, sessionlogout
        


        elif pathname == '/attendance/attendance_home':
            return attendance_home.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/attendance/attendance_list':
            return attendance_list.layout, {'display': 'unset'}, sessionlogout

        elif pathname == '/classes/classes_home':
            return classes_home.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/classes/classes_home_atoz':
            return classes_home_class_atoz.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/classes/classes_home_ztoa':
            return classes_home_class_ztoa.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/classes/classes_home_instructor_atoz':
            return classes_home_instructor_atoz.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/classes/classes_home_instructor_ztoa':
            return classes_home_instructor_ztoa.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/classes/classes_list':
            return classes_list.layout, {'display': 'unset'}, sessionlogout

        elif pathname == '/instructors/instructors_home':
            return instructors_home.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/instructors/instructors_home_atoz':
            return instructors_home_atoz.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/instructors/instructors_home_ztoa':
            return instructors_home_ztoa.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/instructors/instructors_profile':
            return instructors_profile.layout, {'display': 'unset'}, sessionlogout
        elif pathname == '/instructors/instructors_classes':
            return instructors_classes.layout, {'display': 'unset'}, sessionlogout

        elif pathname == '/reports/report':
            return report.layout, {'display': 'unset'}, sessionlogout

        elif pathname == '/about_us':
            return about_us.layout, {'display': 'unset'}, sessionlogout


        else:
            return 'error404', {'display': 'unset'}, sessionlogout



if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:8050/', new=0, autoraise=True)
    app.run_server(debug=False)