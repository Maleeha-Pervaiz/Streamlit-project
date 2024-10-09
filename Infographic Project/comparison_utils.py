import plotly.graph_objs as go
from indicator_utils import *
def create_comparison_chart(data1, data2, chart_type="Line Chart", indicator=None, window=20, chart_width=1000, chart_height=600):
    fig = go.Figure()

    # Add data for first company
    if chart_type == "Line Chart":
        fig.add_trace(go.Scatter(x=data1['date'], y=data1['close_price'], mode='lines', name=data1['stock_symbol'].iloc[0]))
        fig.add_trace(go.Scatter(x=data2['date'], y=data2['close_price'], mode='lines', name=data2['stock_symbol'].iloc[0]))

    # Add indicator if selected
    if indicator == "SMA":
        sma1 = calculate_sma(data1, window=window)
        sma2 = calculate_sma(data2, window=window)
        fig.add_trace(go.Scatter(x=data1['date'], y=sma1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} SMA ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=sma2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} SMA ({window})'))
    elif indicator == "EMA":
        ema1 = calculate_ema(data1, window=window)
        ema2 = calculate_ema(data2, window=window)
        fig.add_trace(go.Scatter(x=data1['date'], y=ema1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} EMA ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=ema2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} EMA ({window})'))
    elif indicator == "Bollinger Bands":
        sma1, upper_band1, lower_band1 = calculate_bollinger_bands(data1, window=window)
        sma2, upper_band2, lower_band2 = calculate_bollinger_bands(data2, window=window)
        fig.add_trace(go.Scatter(x=data1['date'], y=upper_band1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} Upper Band ({window})'))
        fig.add_trace(go.Scatter(x=data1['date'], y=lower_band1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} Lower Band ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=upper_band2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} Upper Band ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=lower_band2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} Lower Band ({window})'))
    elif indicator == "Keltner Channels":
        ema_typical_price1, upper_channel1, lower_channel1 = calculate_keltner_channels(data1, window=window)
        ema_typical_price2, upper_channel2, lower_channel2 = calculate_keltner_channels(data2, window=window)
        fig.add_trace(go.Scatter(x=data1['date'], y=upper_channel1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} Upper Keltner Channel ({window})'))
        fig.add_trace(go.Scatter(x=data1['date'], y=lower_channel1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} Lower Keltner Channel ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=upper_channel2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} Upper Keltner Channel ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=lower_channel2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} Lower Keltner Channel ({window})'))
    elif indicator == "Envelopes":
        upper_envelope1, lower_envelope1 = calculate_envelopes(data1, window=window)
        upper_envelope2, lower_envelope2 = calculate_envelopes(data2, window=window)
        fig.add_trace(go.Scatter(x=data1['date'], y=upper_envelope1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} Upper Envelope ({window})'))
        fig.add_trace(go.Scatter(x=data1['date'], y=lower_envelope1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} Lower Envelope ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=upper_envelope2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} Upper Envelope ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=lower_envelope2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} Lower Envelope ({window})'))
    elif indicator == "Price Channels":
        high_channel1, low_channel1 = calculate_price_channels(data1, window=window)
        high_channel2, low_channel2 = calculate_price_channels(data2, window=window)
        fig.add_trace(go.Scatter(x=data1['date'], y=high_channel1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} High Channel ({window})'))
        fig.add_trace(go.Scatter(x=data1['date'], y=low_channel1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} Low Channel ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=high_channel2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} High Channel ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=low_channel2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} Low Channel ({window})'))
    elif indicator == "ATR":
        atr1 = calculate_atr(data1, window=window)
        atr2 = calculate_atr(data2, window=window)
        fig.add_trace(go.Scatter(x=data1['date'], y=atr1, mode='lines', name=f'{data1["stock_symbol"].iloc[0]} ATR ({window})'))
        fig.add_trace(go.Scatter(x=data2['date'], y=atr2, mode='lines', name=f'{data2["stock_symbol"].iloc[0]} ATR ({window})'))

    # Update layout for comparison chart
    fig.update_layout(
        title='Comparison Chart',
        xaxis_title='Date',
        yaxis_title='Price',
        height=chart_height,
        width=chart_width
    )

    return fig
