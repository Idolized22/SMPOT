import streamlit as st
import numpy as np
from show_stock_graph_about_buy_price import plot_stock_moving_averages_plotly

def main():
    fig = plot_stock_moving_averages_plotly(['NDAQ'],
                                            #'VT', 'SPY', 'TSLA'], 
                                            '2018-01-01')
    st_fig = st.plotly_chart(fig, use_container_width=True)
    # st_fig

if __name__ == '__main__':
    main()