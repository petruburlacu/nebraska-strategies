import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import logging

pd.set_option('display.max_colwidth', 25)

# Set up scraper
screener_url = "https://finviz.com/screener.ashx"

def get_market_data():
    # append each in different method: ?v=111&p=m&f=fa_div_pos,fa_quickratio_o1,ind_stocksonly&ft=4&o=-company
    # v=111: only stocks
    # p=m: only stocks on major exchanges
    # f=fa_div_pos: only stocks with positive dividend yield
    # f=fa_quickratio_o1: only stocks with quick ratio over 1
    # ind_stocksonly: only stocks
    url = screener_url + '?v=111&p=m&f=fa_div_pos,fa_quickratio_o1,ind_stocksonly&ft=4&o=-company'

    try:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req)
        html = BeautifulSoup(webpage, "html.parser")
        #find html table with class screener_table
        data = html.find('table', {'class': 'screener_table'})

        # Get headers
        headers = []
        table_head = data.find('thead')
        for th in table_head.find_all('th'):
            headers.append(th.text)
            logging.debug(th.text)
        
        # Get data
        rows = []
        for tr in data.find_all('tr'):
            rows.append([td.text for td in tr.find_all('td')])
        # Create dataframe
        df = pd.DataFrame(rows, columns=headers)
        # df = df.dropna() # drop rows with NaN values
        df = df.drop([0]) # drop first row (headers)
        df = df.reset_index(drop=True) # reset index
        
        # Need to iterate and get all pages from the table
        # Get the number of pages
        # pages = []
        # for td in data.find_all('td'):
        #     if td.text.isdigit():
        #         pages.append(td.text)
        #         # Get the last page
        #         last_page = pages[-1]
        #         logging.debug(last_page)

        logging.debug(df)
        return df.to_json(orient='records')
    except Exception as e:
        print('Error opening the URL')
        print(e)
        return e