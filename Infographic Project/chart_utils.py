import plotly.graph_objs as go
import plotly.express as px

def create_candlestick_chart(data, company):
    fig = go.Figure(data=[go.Candlestick(
        x=data['date'],
        open=data['open_price'],
        high=data['high_price'],
        low=data['low_price'],
        close=data['close_price'],
        name=company
    )])
    return fig

def create_line_chart(data):
    fig = go.Figure(data=go.Scatter(x=data['date'], y=data['close_price'], mode='lines', name='Close Price'))
    return fig

def create_bar_chart(data):
    fig = go.Figure(data=go.Bar(x=data['date'], y=data['close_price'], name='Close Price'))
    return fig

def create_area_chart(data):
    fig = go.Figure(data=go.Scatter(x=data['date'], y=data['close_price'], fill='tozeroy', name='Close Price'))
    return fig



