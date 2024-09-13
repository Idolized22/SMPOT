#%%
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Function to download stock data and plot with hover info

def calc_prec_change(stock_data, buy_price):
    stock_data['Profit'] = 100 * (stock_data['Close'] - buy_price) / buy_price
    return stock_data['Profit']

def plot_stock_moving_averages_plotly(stock_symbols, start_date):
    if isinstance(stock_symbols, str):
        stock_symbols = [stock_symbols]
    
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    # fig = go.Figure()

    sliders = []
    # Store the percentage traces for updating later
    
    fig_data_per_stock = dict()
    # stocks_data_list = dict()
    
    for idx, stock_symbol in enumerate(stock_symbols):
        # Download stock data
        stock_data = yf.download(stock_symbol, start=start_date)
        fig_data_per_stock[stock_symbol] = []
        buy_price = stock_data['Close'].mean()  # Default buy price as the mean close price
        
        # Calculate moving averages
        stock_data['MA50'] = stock_data['Close'].rolling(window=50).mean()
        stock_data['MA150'] = stock_data['Close'].rolling(window=150).mean()
        stock_data['MA200'] = stock_data['Close'].rolling(window=200).mean()

        # Calculate the percentage and value distance from the MA150
        stock_data['Dist_MA150_Abs'] = stock_data['Close'] - stock_data['MA150']
        stock_data['Dist_MA150_Percent'] = (stock_data['Dist_MA150_Abs'] / stock_data['MA150']) * 100
        # Calculate the percentage and value distance from the MA200
        stock_data['Dist_MA200_Abs'] = stock_data['Close'] - stock_data['MA200']
        stock_data['Dist_MA200_Percent'] = (stock_data['Dist_MA200_Abs'] / stock_data['MA200']) * 100
        stock_data['Profit'] = 100 * (stock_data['Close'] - buy_price) / stock_data['Close']
        
        # Create slider step for setting the buy price
        
        # Add stock price line with hover info showing distance from the buy price
        
        
        
        y_close=stock_data['Close']
        fig_data_per_stock[stock_symbol].append(y_close)
        # Add stock price line with hover info showing distance from MA150 and MA200
        fig.add_trace(go.Scatter(x=stock_data.index, y=stock_data['Close'], 
                                 mode='lines', name=f'{stock_symbol} Close Price', 
                                 line=dict(color='green', width=2),
                                #  yaxis='y2',  # Use secondary y-axis
                                 hovertemplate=(
                                     f'Ticker: {stock_symbol}<br>' +
                                     'Close: %{y:.2f} USD<br>' +
                                     'Date: %{x}<br>' +
                                     'Dist from MA150d: %{customdata[0]:.2f} USD ' + '%{customdata[1]:.2f}%<br>' +
                                     'Dist from MA200d: %{customdata[2]:.2f} USD ' + '%{customdata[3]:.2f}%'),
                                     customdata=stock_data[['Dist_MA150_Abs', 'Dist_MA150_Percent', 
                                                            'Dist_MA200_Abs', 'Dist_MA200_Percent', ]].values),
                                # secondary_y=True,
                             )
        
        y_profit =calc_prec_change(stock_data, buy_price) 
        fig_data_per_stock[stock_symbol].append(y_profit)
        percentage_trace = go.Scatter(
            x=stock_data.index,
            y= stock_data['Profit'], #100 * ((stock_data['Close'] - buy_price) / buy_price), #(100 * (stock_data['Close'] / buy_price)) - 100 ,  # Relative to default buy price
            mode='lines',
            name=f'{stock_symbol} percentages from buy price',
            line=dict(color='blue', width=2),
            yaxis='y1',
            hovertemplate=(
                f'Ticker: {stock_symbol}<br>' +
                'Profit: %{y:.2f}%<br>'+ 
                'Close: %{customdata[0]:.2f} USD<br>' +
                'Date: %{x}<br>'                ),
                customdata=stock_data[['Close', 'Dist_MA150_Percent', 'Dist_MA200_Abs', 'Dist_MA200_Percent']].values
                )   
        
        fig.add_trace(percentage_trace, secondary_y=True)
        
        
        mva50 = stock_data['MA50']
        fig_data_per_stock[stock_symbol].append(mva50)
        # Add 50-day, 150-day, and 200-day moving averages for the stock
        fig.add_trace(go.Scatter(
            x=stock_data.index,
            y=stock_data['MA50'],
            mode='lines',
            name=f'{stock_symbol} MA50days',
            line=dict(width=2, color='green', dash='dash'),
            hovertemplate=f'{stock_symbol} MA50d: <br>' + '%{y:.2f} USD<br>Date: %{x}'
        ))
        
        mva150 = stock_data['MA150']
        fig_data_per_stock[stock_symbol].append(mva150)
        fig.add_trace(go.Scatter(
            x=stock_data.index,
            y=stock_data['MA150'],
            mode='lines',
            name=f'{stock_symbol} MA150days',
            line=dict(width=2, color='yellow', dash='dashdot'),
            hovertemplate=f'{stock_symbol} MA150d: <br>' + '%{y:.2f} USD<br>Date: %{x}'
        ))
        
        mva200 = stock_data['MA200']
        fig_data_per_stock[stock_symbol].append(mva200)
        fig.add_trace(go.Scatter(
            x=stock_data.index,
            y=stock_data['MA200'],
            mode='lines',
            name=f'{stock_symbol} MA200days',
            line=dict(width=2, color='red', dash='dot'),
            hovertemplate=f'{stock_symbol} MA200d: <br>' + '%{y:.2f} USD<br>Date: %{x}'
        ))
    
        steps = []
        for buy_price in range(int(stock_data['Close'].min()-2), int(stock_data['Close'].max()+2), 1):
            stock_data['Profit'] =  100 * (stock_data['Close'] - buy_price) / buy_price
            fig_data_per_stock[stock_symbol][1] = stock_data['Profit']
            
            # arg_y_list = []
            # for sb in fig_data_per_stock.keys():
            #     arg_y_list += fig_data_per_stock[sb]
            
            steps.append(dict(
                # method='update',
                args=[{'y': [stock_data['Close'], stock_data['Profit'], stock_data['MA50'],  stock_data['MA150'], stock_data['MA200'], ]}],
                label=f'Buy @ {buy_price:.2f} USD'
            ))

        sliders.append({
            'active': len(steps) // 2,
            'currentvalue': {"prefix": f"{stock_symbol} Buy Price: "},
            'pad': {"t": 15},
            # 'y': 0 + idx * 0.2,
            'steps': steps})

    # Update layout to add the secondary y-axis
    fig.update_layout(
        sliders=sliders,
        title='Stock Prices and Moving Averages (Percentages from Buy Price)',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        yaxis2_title='Profit %',
        # yaxis=dict(
        #     title='Change from buy price %',
        #     side='left',
        # ),
        # yaxis1=dict(
        #     title='Change from buy price %',
        #     autorange=True,
        #     side='left',
        #     overlaying='y1'
        # ),
        # yaxis2=dict(
        #     title='Price (USD)',
        #     side='right',
        #     autorange=True,
        #     overlaying='y2'
        # ),
        width=1000,
        height=600,
        legend_title="Legend",
        template='plotly_dark'
    )

    return fig
    
def show(fig):
    # Show the plot
    fig.show()


# Example usage:

if __name__ == '__main__':
    fig = plot_stock_moving_averages_plotly(['NDAQ'],
                                        #'VT', 'SPY', 'TSLA'], 
                                        '2018-01-01')
    show(fig)

# %%
