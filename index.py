import dash

from dash import html, dcc
from dash.dependencies import Input, Output

import pandas as pd
import numpy as np

import plotly.express as px
import plotly.graph_objects as go


app = dash.Dash(__name__)
server = app.server

df_data = pd.read_csv("supermarket_sales.csv")
df_data["Date"] = pd.to_datetime(df_data['Date'])



#======== Layout ========
app.layout = html.Div(children=[
                html.H5("Cidades:"),
                dcc.Checklist(df_data["City"].value_counts().index,
                df_data["City"].value_counts().index,id="check_city"),

                html.H5("Variável de Análise:"),
                dcc.RadioItems(["gross icome", "Rating"],"gross icome",id="main_variable"),
                
                dcc.Graph(id="city_fig"),
                dcc.Graph(id="pay_fig"),
                dcc.Graph(id="income_per_product_fig")

                ]
            )


#======== Callback ====

@app.callback([
            Output('city_fig', 'figure'),
            Output('pay_fig', 'figure'),
            Output('income_per_product_fig', 'figure')
    ],
        [
            Input('check_city', 'value'),
            Input('main_variable', 'value')
    ])

def render_graphs(cities,main_variable):

    cities = ["Yangon", "Mandalay"]
    main_variable ="gross income"

    operation = np.sum if main_variable == "gross income" else np.mean

    df_filtered = df_data[df_data["City"].isin(cities)]

    df_city = df_filtered.groupby("City") [main_variable].apply(operation).to_frame().reset_index()
    df_payment = df_filtered.groupby("Payment") [main_variable].apply(operation).to_frame().reset_index()
    df_product = df_filtered.groupby("Product Line","City") [main_variable].apply(operation).to_frame().reset_index()

    fig_city = px.bar(df_city, x="City", y="gross incomw")


    return

#======== Run server ====
if __name__ == "__main__":
    app.run_server(port=8050, debug=True)