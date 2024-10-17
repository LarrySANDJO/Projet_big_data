import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import json
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import numpy as np



# Charger les données JSON en spécifiant l'encodage UTF-8
with open('produits.json', encoding='utf-8') as f:
    data = json.load(f)


# Convertir en DataFrame pour faciliter le traitement
df = pd.DataFrame(data)

# Initialisation de l'application et choix du theme
external_stylesheets = [dbc.themes.LUMEN] # dbc.themes.BOOTSTRAP, dbc.themes.CERULEAN
app = Dash(__name__, external_stylesheets=external_stylesheets)


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}
# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}
sidebar = html.Div(
    [
        html.H2("Menu", className="display-4"),
        html.Hr(),
        html.P(
            "Cette applicaton a ete concu pour suivre le prix des produits de Auchan.", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Acceuil", href="/", active="exact"),
                dbc.NavLink("Visualisation", href="/visualisation", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('DASHBORD DE SUIVI DES PRIX DE AUCHAN', className="text-primary text-center fs-1", style={'textAlign': 'right', 'padding-left': '270px', 'font-weight': 'bold'})
    ]),

    dbc.Row([
        dbc.Card([
            html.Div([
    dcc.Location(id='url', refresh=False),
    sidebar,
    html.Div(id='page-content', style=CONTENT_STYLE)
])
        ])
    ]),
], fluid=True)

@callback(Output("page-content", "children"), Input("url", "pathname"))
def render_page_content(pathname):
    if pathname == "/":
        return home_layout
    elif pathname == "/visualisation":
        return dashbord_layout

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )




home_layout = dbc.Container([
    dbc.Col([
        html.Div([
    html.H1("Bienvenue sur la page d'accueil du dashbord", style={'textAlign': 'center', 'font-weight': 'bold'}),
    ])
    ]),
    dbc.CardImg(src="/assets/Photo1.jpeg", top=True),
    html.H2('DESCRIPTION DE L`APPLICATION'),
    html.H2("L'objectif de cette application est de faire le suivi des prix de Auchan."),
])



# Layout de l'application
dashbord_layout = html.Div([
    html.H1("Catalogue de Produits", style={'textAlign': 'center', 'font-weight': 'bold'}),
    
    # Dropdown pour sélectionner la catégorie
    html.Label("Sélectionnez une catégorie", style={'textAlign': 'center', 'font-weight': 'bold'}),
    dcc.Dropdown(
        id='category-dropdown',
        options=[{'label': cat, 'value': cat} for cat in df['category'].unique()],
        value=df['category'].unique()[0]
    ),
    
    # Section pour afficher les produits
    dbc.Row(id='product-list')
])

# Callback pour mettre à jour la liste des produits en fonction de la catégorie sélectionnée
@callback(
    Output('product-list', 'children'),
    Input('category-dropdown', 'value')
)
def update_products(selected_category):
    # Filtrer les produits par catégorie
    filtered_df = df[df['category'] == selected_category]

    # Créer des cartes de produit
    products = []
    for _, row in filtered_df.iterrows():
        product_card = dbc.Col([
            html.Div([
            html.Img(src=row['image_url'], style={'width': '100px', 'height': '100px'}),
            html.H4(row['title']),
            html.P(f"Prix : {row['price']}", style={'font-weight': 'bold'}),
            html.P("Disponible" if not row['is_out_of_stock'] else "Rupture de stock")
            ], style={'border': '1px solid #ccc', 'padding': '10px', 'margin': '10px'})
            ], width=3)  
        products.append(product_card)
    
    return products

# Lancer l'application
if __name__ == '__main__':
    app.run_server(debug=True)
