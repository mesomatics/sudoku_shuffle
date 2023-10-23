from flask import Flask
from dash import Dash, dash_table, dcc, html, Input, Output, State, no_update
import pandas as pd
import numpy as np


df = pd.DataFrame(np.full(shape=(10, 10), fill_value=np.nan, dtype=object),
                 columns=[f"col{c}" for c in range(10)])

server = Flask(__name__)
app = Dash(__name__, server=server)

app.layout = html.Div([
    dash_table.DataTable(
        id="data",
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df],
        editable=True,
        style_header={'display': 'none'},
        style_cell={
            "width": "50px",
            "height": "50px",
            "textAlign": "center",
            "fontSize": 20,
            "fontWeight": "bold"
        },
        style_data_conditional=[
            {
                "if": {"row_index": np.arange(0, 10, 3)},
                "border-top": "3px solid black"
            },
            {
                "if": {"column_id": [f"col{x}" for x in range(0, 10, 3)]},
                "border-left": "3px solid black"
            },
            {
                "if": {"row_index": 9},
                "display": "None"
            },
            {
                "if": {"column_id": "col9"},
                "display": "None"
            }
        ],
        fill_width=False
    ),
    html.Button("Shuffle", id="shuffle", n_clicks=0)
])

@app.callback(
    Output("data", "data"),
    Output("shuffle", "n_clicks"),
    Output("data", "active_cell"),
    Output("data", "selected_cells"),
    Input("shuffle", "n_clicks"),
    State("data", "data")
)
def shuffle(click, data):
    if click > 0:
        df = pd.DataFrame(data)
        cols = df.columns
        idx = np.arange(9).reshape(3, 3)
        row_block_p = np.random.choice(3, 3, replace=False)
        col_block_p = np.random.choice(3, 3, replace=False)
        row_block_p = idx[row_block_p]
        col_block_p = idx[col_block_p]
        row_p = np.concatenate((
            np.random.choice(row_block_p[0], 3, replace=False),
            np.random.choice(row_block_p[1], 3, replace=False),
            np.random.choice(row_block_p[2], 3, replace=False),
            [9]
        ))
        col_p = np.concatenate((
            np.random.choice(col_block_p[0], 3, replace=False),
            np.random.choice(col_block_p[1], 3, replace=False),
            np.random.choice(col_block_p[2], 3, replace=False),
            [9]
        ))
        transpose = np.random.choice([False, True], 1)
        if transpose:
            df = df.T
        df = df.iloc[row_p, col_p]
        df.reset_index(drop=True, inplace=True)
        df.columns = cols
        empty = {"row": 9, "column":9, "column_id": "col9"}
        return df.to_dict("records"), 0, empty, [empty]
    else:
        return [no_update] * 4


if __name__ == '__main__':
    server.run(port=73)
