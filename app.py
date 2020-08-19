import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table
import dash_table.FormatTemplate as FormatTemplate
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash.dependencies import Input, Output, State
import geopandas as gpd
import os
import json
from flask_caching import Cache
import folium

app = dash.Dash(__name__)
cache = Cache(app.server, config={
    'CACHE_TYPE': 'filesystem',
    'CACHE_DIR': 'cache-directory'
})

def discrete_background_color_bins(df, n_bins=5, columns='all'):
    import colorlover
    bounds = [i * (1.0 / n_bins) for i in range(n_bins + 1)]
    if columns == 'all':
        if 'id' in df:
            df_numeric_columns = df.select_dtypes('number').drop(['id'], axis=1)
        else:
            df_numeric_columns = df.select_dtypes('number')
    else:
        df_numeric_columns = df[columns]
    df_max = df_numeric_columns.max().max()
    df_min = df_numeric_columns.min().min()
    ranges = [
        ((df_max - df_min) * i) + df_min
        for i in bounds
    ]
    styles = []
    legend = []
    for i in range(1, len(bounds)):
        min_bound = ranges[i - 1]
        max_bound = ranges[i]
        backgroundColor = colorlover.scales[str(n_bins)]['seq']['Blues'][i - 1]
        color = 'white' if i > len(bounds) / 2. else 'inherit'

        for column in df_numeric_columns:
            styles.append({
                'if': {
                    'filter_query': (
                        '{{{column}}} >= {min_bound}' +
                        (' && {{{column}}} < {max_bound}' if (i < len(bounds) - 1) else '')
                    ).format(column=column, min_bound=min_bound, max_bound=max_bound),
                    'column_id': column
                },
                'backgroundColor': backgroundColor,
                'color': color
            })
        legend.append(
            html.Div(style={'display': 'inline-block', 'width': '60px'}, children=[
                html.Div(
                    style={
                        'backgroundColor': backgroundColor,
                        'borderLeft': '1px rgb(50, 50, 50) solid',
                        'height': '10px'
                    }
                ),
                html.Small(round(min_bound, 2), style={'paddingLeft': '2px'})
            ])
        )

    return (styles, html.Div(legend, style={'padding': '5px 0 5px 0'}))


# os.chdir("D:\SOCIOECONOMIC CLASSES")
@cache.memoize()
def read_json_files():
    with open("D:\SHP_JSON_FILES\Barangay_SOCIO2.geojson") as geofile:
        brgy_json = json.load(geofile)
    with open("D:\SHP_JSON_FILES\City_SOCIO.geojson") as geofile:
        city_json = json.load(geofile)
    return brgy_json, city_json

@cache.memoize()
def read_dfs():
    # df_brgy = gpd.read_file("D:\SOCIOECONOMIC CLASSES\df_brgy.shp")
    df_brgy = pd.read_csv("D:\SOCIOECONOMIC CLASSES\DATA\df_brgy.csv")
    df_city = pd.read_csv("D:\SOCIOECONOMIC CLASSES\DATA\df_city.csv")
    bpi = pd.read_csv("D:\SOCIOECONOMIC CLASSES\DATA\BRANCH.csv")
    return df_brgy, df_city, bpi

df_brgy, df_city, bpi = read_dfs()
brgy_json, city_json = read_json_files()

sidebar_header = dbc.Row(
    [
        html.H1("PP-Metric"),
        dbc.Col(
            [
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        "border-color": "rgba(0,0,0,0)",
                        # "margin-top":"5px",
                    },
                    id="navbar-toggle",
                ),
                html.Button(
                    # use the Bootstrap navbar-toggler classes to style
                    html.Span(className="navbar-toggler-icon"),
                    className="navbar-toggler",
                    # the navbar-toggler classes don't set color
                    style={
                        "color": "rgba(0,0,0,.5)",
                        # "margin-top":"5px",
                        "border-color": "rgba(0,0,0,0)",
                    },
                    id="sidebar-toggle",
                ),
            ],
            # the column containing the toggle will be only as wide as the
            # toggle, resulting in the toggle being right aligned
            # width={"size":1,  "offset":12},
            width="auto",
            # vertically align the toggle in the center
            align="center",
        ),
        
    ],
    justify = "end"
)

sidebar = html.Div(
    [
        sidebar_header,
        # we wrap the horizontal rule and short blurb in a div that can be
        # hidden on a small screen
        html.Div(
            [
                html.Hr(),
                html.P(
                    "A metric substitude for determining ABC socioenomic classes ",
                    className="lead",
                ),
                html.H6("Choose a region"),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[
                        {'label': i, 'value': i} for i in df_brgy.REGION.unique()
                    ],
                    value='METROPOLITAN MANILA'
                ),
                html.Br(),
                html.H6("Choose a province"),
                dcc.Dropdown(
                    id='province-dropdown',
                ),

                html.Br(),
                html.H6("Choose a city"),
                dcc.Dropdown(
                    id='city-dropdown',
                ),
            ],
            id="blurb",
        ),
        # use the Collapse component to animate hiding / revealing links
        dbc.Collapse(
            dbc.Nav(
                [
                    dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                    dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
                    dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
                ],
                vertical=True,
                pills=True,
            ),
            id="collapse",
        ),
    ],
    id="sidebar",
)
# html.Div([html.Iframe(id = "folium_map", srcDoc = open("D:\\SOCIOECONOMIC CLASSES\\folium_map_dash.html", 'r').read(), width='100%')], id="folium-div"),
        
content = html.Div(
    [   html.Div([dash_table.DataTable(
                        id='summary_table',
                        columns=[{"name": i, "id": i} for i in [ 'BRGY', 'land_value', 'AGRICULTURAL', 'FINANCING', 'MANUFACTURING']],
                        data=df_brgy[[ 'BRGY', 'land_value', 'sum', 'AGRICULTURAL', 'FINANCING', 'MANUFACTURING', ]].to_dict("records"), 
                        style_table={'height': '800px', 'overflowY': 'auto', 'width':'400px' })], 
                    id = "boop-da-snoot-4-da-tbl", style = {"background-color":"#FFFFFF"}),
                    html.Div([
            html.Div([dcc.Graph(id="my-graph")],
                     id = "for the maps", 
                     style = {"background-color":"#f1c40f"}),
            html.Div([
                html.Div([dcc.Graph(id="subgraph1")], id= "Thing 1", style = {"height":'500px'}),
                html.Div([html.Iframe(id = "folium_map", srcDoc = open("D:\\SOCIOECONOMIC CLASSES\\folium_map_dash.html", 'r').read(), width='100%')], id= "Thing 2"),
                html.Div([dcc.Graph(id="subgraph3")], id= "Thing 3"),
            ], id = "metrics-wrapper", style = {"display":"inline-grid", "column-gap":"1em", "grid-template-columns":"1fr 1fr 1fr"})
        ], style = {"display":"grid", "grid-template-rows":"4fr 1fr", "row-gap":"1em"})
    ],
    style = {
        "display":"grid",
        "grid-template-columns":"1fr 2fr",
        "column-gap":"1em"
    },
    id="page-content")

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])


# this callback uses the current pathname to set the active state of the
# corresponding nav link to true, allowing users to tell see page they are on
@app.callback(
    [Output(f"page-{i}-link", "active") for i in range(1, 4)],
    [Input("url", "pathname")],
)
def toggle_active_links(pathname):
    if pathname == "/":
        # Treat page 1 as the homepage / index
        return True, False, False
    return [pathname == f"/page-{i}" for i in range(1, 4)]

@app.callback(
    Output('province-dropdown', 'options'),
    [Input('region-dropdown', 'value')])
def set_cities_options(selected_region):
    return [{'label': i, 'value': i} for i in df_brgy[df_brgy.REGION==selected_region].PROV.unique()]

@app.callback(
    Output('city-dropdown', 'options'),
    [Input('region-dropdown', 'value'), 
    Input('province-dropdown', 'value')])
def set_cities_options(selected_region, selected_prov):
    return [{'label': i, 'value': i} for i in df_brgy[(df_brgy.REGION==selected_region) & (df_brgy.PROV==selected_prov)].CITY.unique()]

@cache.memoize()
def create_choropleth(df, json, column, geo_column, hover_column):
    fig = px.choropleth(df, 
                    geojson=json, 
                    color=column,
                    locations=geo_column, featureidkey=f"properties.{geo_column}",
                    projection="mercator", hover_data=hover_column
                   )
    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

@cache.memoize()
def create_folium(sub_bpi, sub_df, filename, zoom = 14):
    m = folium.Map(location=[sub_bpi.Latitude.median(), sub_bpi.Longitude.median()], zoom_start=zoom)
    folium.TileLayer('CartoDB positron',name="Light Map",control=False).add_to(m)
    for i in range(len(sub_bpi)):
        folium.Marker(
            location=[sub_bpi.iloc[i,:].Latitude, sub_bpi.iloc[i,:].Longitude],
        ).add_to(m)
    choropleth = folium.Choropleth(
                    geo_data='D:\SHP_JSON_FILES\Barangay_SOCIO.geojson',
                    name='choropleth',
                    data=sub_df,
                    columns=['ID', 'sum'],
                    key_on='feature.properties.ID',
                    fill_color='YlGn',
                    fill_opacity=0.7,
                    line_opacity=0.2
                ).add_to(m)
    m.save(filename)

# Output('summary_table', 'style_data_conditional')
@app.callback(
    [Output("my-graph", "figure"),
    Output("subgraph1", "figure"),
    Output('summary_table', 'data')],
    [Input('region-dropdown', 'value'), 
    Input('province-dropdown', 'value'),
    Input('city-dropdown', 'value')])
@cache.memoize()
def set_cities_options(selected_region, selected_prov, selected_city):
    df_sub = df_brgy.loc[(df_brgy.REGION==selected_region) & (df_brgy.PROV==selected_prov) & (df_brgy.CITY==selected_city)]
    # styles, legend = discrete_background_color_bins(df_sub.drop(columns=['ID']))
    fig = create_choropleth(df_sub, brgy_json, "land_value", "ID", ["BRGY"])
    sub1 = create_choropleth(df_sub, brgy_json, "sum", "ID", ["BRGY"])
    # fig = px.choropleth_mapbox(df_sub, 
    #                        geojson=brgy_json, 
    #                        color="land_value",
    #                        locations="ID", featureidkey="properties.ID",
    #                        center={"lat": 12.8797, "lon": 121.7740},
    #                        mapbox_style="carto-positron", zoom=9)
    # fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig, sub1, df_sub.drop(columns=['ID']).to_dict("records")

# @app.callback(Output("page-content", "children"), [Input("url", "pathname")])
# def render_page_content(pathname):
#     if pathname in ["/", "/page-1"]:
#         return html.P("This is the content of page 1!")
#     elif pathname == "/page-2":
#         return html.P("This is the content of page 2. Yay!")
#     elif pathname == "/page-3":
#         return html.P("Oh cool, this is page 3!")
#     # If the user tries to reach a different page, return a 404 message
#     return dbc.Jumbotron(
#         [
#             html.H1("404: Not found", className="text-danger"),
#             html.Hr(),
#             html.P(f"The pathname {pathname} was not recognised..."),
#         ]
#     )


@app.callback(
    Output("sidebar", "className"),
    [Input("sidebar-toggle", "n_clicks")],
    [State("sidebar", "className")],
)
def toggle_classname(n, classname):
    if n and classname == "":
        return "collapsed"
    return ""


@app.callback(
    Output("collapse", "is_open"),
    [Input("navbar-toggle", "n_clicks")],
    [State("collapse", "is_open")],
)
def toggle_collapse(n, is_open):
    if n:
        return not is_open
    return is_open

# app.layout = html.Div(
#     [
#         html.Div("Sidebar", style = {"background-color":"crimson"}),
#         html.Div("Content"),
#     ],
#     style = {
#         "display":"grid",
#         "grid-template-columns":"1fr 1fr"
#     }
# )

if __name__ == '__main__':
    app.run_server(debug=True)