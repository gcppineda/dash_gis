import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output, State
from sidebar import sidebar_content, sidebar_header

# PAGE CONTENTS ---------------------------------------------------------------------
# ---- SIDEBAR ----------------------------------------------------------------------
sidebar = html.Div(
    [
        sidebar_header,
        html.Div(sidebar_content, id="blurb")
    ],
    id="sidebar",
)

# ---- DIVS ------------------------------------------------------------------------
table_div = []
map_div = []
metrics_div = []

content = html.Div(
    [
        html.Div(table_div, style = {"background-color":"#3498db"}),
        html.Div([
            html.Div(map_div, style = {"background-color":"#f1c40f"}),
            html.Div(metrics_div, id = "metrics-wrapper", style = {"display":"inline-grid", "column-gap":"1em", "grid-template-columns":"1fr 1fr 1fr"})
        ], style = {"display":"grid", "grid-template-rows":"4fr 1fr", "row-gap":"1em"})
    ],
    style = {
        "display":"grid",
        "grid-template-columns":"1fr 2fr",
        "column-gap":"1em"
    },
    id="page-content")

# ADD THE CONTENTS HERE ----------------------------------------------------------------------------------
table_div.append(html.H3("Add table here"))
map_div.append(html.H3("map box"))
metrics_div.append(html.Div("Thing 1"))
metrics_div.append(html.Div("Thing 2"))
metrics_div.append(html.Div("Thing 3"))

# MAKE APP AND LAYOUT ------------------------------------------------------------------------------------
app = dash.Dash(__name__)
app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# CALLBACKS

# FOR RESPONSIVE / COLLAPSE SIDEBAR
@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)

def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""

if __name__ == '__main__':
    app.run_server(debug=True)