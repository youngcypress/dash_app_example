from pathlib import Path
import plotly.graph_objs as go
import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

path = Path(__file__).resolve().parent.parent.parent


df_allPrt = pd.read_excel(f'{path}/result/所有基金分资产仓位探测结果.xlsx', sheet_name='df_prtStoct')

app = dash.Dash(__name__)

# Declare server for Heroku deployment. Needed for Procfile.
server = app.server
# 设置应用程序布局
app.layout = html.Div([
    dcc.Dropdown(
        id='field-dropdown',
        options=[{'label': column, 'value': column} for column in df_allPrt.columns if column != 'date'],
        value=df_allPrt.columns[1]
    ),
    dcc.Graph(id='field-trend')
])

# 设置回调以根据所选字段更新折线图
@app.callback(
    Output('field-trend', 'figure'),
    [Input('field-dropdown', 'value')]
)
def update_trend(selected_field):
    fig = go.Figure(
        data=[go.Scatter(x=df_allPrt['date'], y=df_allPrt[selected_field], mode='lines')],
        layout=dict(title=f'Trend for {selected_field}', xaxis_title='Date', yaxis_title='Value')
    )
    return fig

# 启动应用程序
if __name__ == '__main__':
    app.run_server(debug=True)




# def draw_subplots(data):
#     # 创建一个子图
#     fig = make_subplots(rows=1, cols=1, shared_xaxes=True)
#
#     # 为每个字段添加一条折线
#     for column in data.columns:
#         if column != 'date':
#             fig.add_trace(go.Scatter(x=data['date'], y=data[column], name=column, mode='lines'))
#
#     # 更新图表布局
#     fig.update_layout(title='Fields over Time', xaxis_title='Date', yaxis_title='Value')
#
#     # 显示图表
#     fig.show()
# draw_subplots(df_allPrt)
