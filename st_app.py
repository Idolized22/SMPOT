import streamlit as st
import numpy as np
from show_stock_graph_about_buy_price import plot_stock_moving_averages_plotly
import datetime

def main():
    st. set_page_config(layout="wide") 
    start_date_str = '2018-01-01'
    # Sidebar inputs
    st.sidebar.header('Stock Data Input')

    # Ticker input
    ticker = st.sidebar.text_input('Enter ticker name', 'SPY')

    # Start date input with a calendar
    start_date = st.sidebar.date_input('Select start date', value=datetime.date(2018,1,1), min_value=datetime.date(1980,1,1))

    # Convert the selected date to a string in YYYY-MM-DD format
    if start_date:
        start_date_str = start_date.strftime('%Y-%m-%d')

    # Main content
    st.title('SMPOT')

    # st.write(f"**Ticker:** {ticker}")
    # st.write(f"**Start Date:** {start_date_str}")

    show_fig(ticker, start_date_str)

def show_fig(ticker ='SPY', start_date='2018-01-01'):
    fig = plot_stock_moving_averages_plotly(ticker, start_date)
    st_fig = st.plotly_chart(fig, use_container_width=True, theme=None)
    # st_fig

if __name__ == '__main__':
    main()