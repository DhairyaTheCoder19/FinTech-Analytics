# FinTech Analytics

FinTech Analytics is a stock market dashboard I developed using Python and Streamlit. The dashboard helps me search for a company and view some important stock information about it.

## Functionality

The user can enter the name of the company or its stock ticker in order to find information about it. After entering, it displays:

* current stock price
* P/E ratio
* 52 week high
* 30 day stock price trend
* 30 day trading volume
* recent news about the company

There is a ticker bar on the top of the screen, which shows prices of other companies.

## Implementation

"dashboard.py" file is the main part of this project. Python takes care of data manipulation and calculations, while Streamlit is responsible for dashboard development.

I also used financial data and charting API in order to obtain information about stocks and display it in the dashboard.

## How to run it

Firstly, install the required libraries with the following command:

text
pip install -r requirements.txt


Then run the dashboard:


streamlit run dashboard.py


Running it opens the dashboard in the web browser.

## Project files

text
FinTech-Analytics/
dashboard.py
requirements.txt
.gitignore
README.md


## Motivation

I was motivated by my interest in finance, analytics, and now programming and decided to develop a useful project related to it. I didn't want to make some simple practice program, but something useful instead.

I initially had an idea about searching up stocks and implemented additional functionality like charts, trading volume, ticker bar, and company news along the way.

## Current progress

Main features are functional. I tested the search functionality with different companies and stock tickers and it is able to show the information about the stock and recent news about the company.

I might add some additional features in the future.
