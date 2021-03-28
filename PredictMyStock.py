#!/usr/bin/env python
# coding: utf-8

# In[1]:


# pip install streamlit fbprophet yfinance plotly
import streamlit as st
from datetime import date
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go
#import time

st.set_page_config(
        page_title='Predict My Stocks                 ',
        page_icon="📈"
        )



hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 



def _max_width_():
    max_width_str = f"max-width: 1500px;"
    st.markdown(
        f"""
    <style>
    .reportview-container .main .block-container{{
        {max_width_str}
    }}
    </style>    
    """,
        unsafe_allow_html=True,
    )


START = "2000-01-01"
TODAY = date.today().strftime("%Y-%m-%d")

st.markdown("<h1 style='text-align: center; color: black;'>Predict My Stocks</h1>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: black;'>Enter your stock and wait 10-20 seconds for the machine learning code to process the data </h2>", unsafe_allow_html=True)


#https://ibb.co/FqhFwD3

st.markdown("<h5 style='text-align: center; color: black;'>(Please note that the results are not a guarantee and you buy stocks at your own risk. With this project I wanted to enable people to apply machine learning to their stocks. If an error occurs the stock is not in my stock list. Prices are in US dollars. Version 2.0 Added cryptocurrencies BTC-USD)</h5>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color: black;'>                 </h5>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color: black;'>                 </h5>", unsafe_allow_html=True)


stocks = (' AAPL', ' GOOG', ' AMZN', ' TSLA', ' FB', ' GME', ' MSFT', ' ADBE', ' ORCL', ' SNPS', ' VRSN', ' ACN', ' IBM', ' CRM', ' NOW', ' FIS',
' FISV', ' ADSK', ' INTU', ' COMMU', ' CSCO', ' AMAT', ' APH', ' HPQ', ' MSI', ' V', ' DIS', ' CMCSA', ' VZ', ' T', ' TMUS', ' NFLX', ' CHTR',
' NVDA', ' AVGO', ' QCOM', ' TXN', ' MU', ' AMD', ' XLNX', ' MCHP', ' ADI', ' JPM', ' BAC', ' BRK-B', ' AXP', ' COF', ' C', ' WFC',
' USB', ' PNC', ' MS', ' GS', ' SCHW', ' RF', ' ICE', ' SPGI', ' CME', ' MSCI', ' BLK', ' BK', ' STT', ' AON', ' MET', ' GL', ' L',
' BSX', ' BIO', ' EW', ' MDT', ' SYK', ' ABT', ' TMO', ' DHR', ' A', ' IQV', ' MTD', ' PFE', ' JNJ', ' MRK', ' ABBV', ' AMGN', ' GILD',
' FISV', ' BMY', ' LYV', ' EA', ' ATVI', ' UNH', ' G' ,' HUM', ' LOW', ' HD', ' MCD', ' SBUX', ' NKE', ' BKNG', ' TJX', ' ROST', ' SPECIA', ' BLL',
' LODGI', ' XOM', ' CVX', ' PSX', ' MPC', ' OKE', ' EOG', ' AMT', ' EQIX', ' SBAC', ' O', ' SPG', ' PSA', ' CCI', ' D', ' SRE', ' PEG',
' ETR', ' ED', ' EIX', ' XEL', ' DUK', ' NEE', ' SO', ' ES', ' WEC', ' APD', ' DD', ' CE', ' SHW', ' LIN', ' WM', ' RSG', ' SWK',
' BA', ' RTX', ' NOC', ' LMT', ' GD', ' LHX', ' GE', ' MMM', ' HON', ' ITW', ' EMR', ' ROP', ' PH', ' IR', ' CAT', ' ADP', ' EFX',
' VRSK', ' ADP', ' JCI', ' GIS', ' KHC', ' K', ' SYY', ' STZ', ' MDLZ', ' MO', ' PM', ' KO', ' PEP', ' COP', ' VTR', ' ASML', ' NVS',
' MRVL', ' BIP', ' AMX', ' FMX', ' FN', ' RE', ' BEP', ' EC', ' VALE', ' ITUB', ' ABEV', ' XP', ' BBD', ' PBR', ' MELI', ' BSBR',
' GOLD', ' NTR', ' CNQ', ' KL', ' GIB', ' SAP', ' TOT', ' AZN', ' BP', ' BTI', ' NGG', ' PUK', ' VOD', ' DEO', ' HSBC', ' RIO', ' UL', ' TT', ' APTV', ' SAN', ' BBVA', ' TEF',
' BUD', ' NXPI', ' PHG', ' DB', ' GSK', ' CCEP', ' FTCH', ' QSR', ' MGA', ' WPM', ' NVO', ' CB', ' SPOT', ' ABB', ' ALC', ' CS', ' MT',
' GFI', ' PAND', ' KOSS', ' DYNT', ' ACY', ' STXS', ' PUBM', ' SEAS', ' PDCE', ' TS', ' WOW', ' CDXC', ' ACIA', ' PTVCB', ' CRTO', ' PMBC',
' LORL', ' PRA', ' ASRV', ' SSNT', ' SFBC', ' INFR', ' ASLN', ' ARD', ' AGR', ' AAON', ' ACIW', ' ADAP', ' ULBI', ' NCTY', ' PING', ' RETO', ' HCC',
' CLGN', ' SOS', ' ITP', ' USPH', ' PNRG', ' RYI', ' IIPR', ' FROG', ' SNSE', ' POSH', ' OPT', ' KUKE', ' UAMY', ' BVS', ' QLI', ' WOOF', ' AMC',
' UVXY', ' T', ' AAOI', ' ABNB', ' ACHC', ' SSY', ' COHU', ' NAKD', ' BCE', ' MRNA', ' TWTR', ' BBY', ' WMT', ' SE', ' OKTA', ' TGT', ' KR',
' SHOP', ' CNI', ' ENB', ' BNS', ' BAM', ' LULU', ' TRP', ' TRI', ' BCE', ' CM', ' BMO', ' CP', ' MFC', ' SLF', ' TU', ' FNV', ' RCI',
' BILI', ' NTES', ' DELL', ' SPLK', ' VIAC', ' BURL', ' COST', ' WDAY', ' TLIS', ' DBTX', ' DVN', ' PLTR', ' AA', ' AADR', ' AAL', ' AAMC', ' AAP',
' MSFT', ' MRVI', ' KSS', ' PRGO', ' AEP', ' SQM', ' DASH', ' COO', ' SNOW', ' AZO', ' ZM', ' IEP', ' NIO', ' VEEV', ' ZLAB', ' DLTR', ' OPEN',
' TSM', ' BABA', ' GOOGL', ' BRK.A', ' BRK.B', ' MA', ' PG', ' PYPL', ' INTC', ' PDD', ' UNP', ' UPS', ' SNE', ' RY', ' DE', ' ARCC',
' SXY', ' IMKTA', ' MSGN', ' KBAL', ' UBA', ' HFC', ' CXW', ' TAP', ' DBI', ' GEO', ' DISCA', ' QRTEA', ' ALL', ' WDC', ' UNIT', ' RPT', ' DNOW',
' LUMN', ' QRVO', ' TCOM', ' ROIC', ' CVS', ' NOV', ' GM', ' MCO', ' LSXMK', ' TKA', ' 1COV', ' LHA', ' WDI', ' RWE', ' HEI', ' DBK', ' DB1',
' EOAN', ' FME', ' IFX', ' BEI', ' CON', ' MUV2', ' HEN3', ' DPW', ' ADS', ' BMW', ' BAYN', ' DAI', ' DTE', ' VOW3', ' SIE', ' ALV', ' SAP',
' LLOY', ' RR', ' IAG', ' BARC', ' GLEN', ' HSBA', ' TSCO', ' NWG', ' SMDS', ' RDSB', ' STAN', ' TW', ' AV', ' BATS', ' NOK', ' QS', ' TDOC',
' PZZA', ' BB', ' LI', ' QQQ', ' SCR', ' ARKK', ' WAMCX', ' IEC', ' TCEHY', ' HLT', ' PINS', ' BIOPX', ' TWLO', ' UPLD', ' W', ' TNC', ' MPGFX',
' MAT', ' FCX', ' IAC', ' ETSY', ' PTON', ' EXPR', ' JAGX', ' CCIV', ' SNDL', ' ZOM', ' MOMO', ' MYO', ' MENXF', ' TM', ' SFTBF', ' NTDMF', ' FRCOF',
' NPPXF', ' NNDNF', ' NTDOF', ' KDDIF', ' SHECF', ' MUFG', ' MRAAF', ' TAK', ' HMC', ' ITOCF', ' SVNDF', ' MFG', ' MIELF', ' ALPMF', ' 7832.T',
' CGC', ' SMG', ' GWPH', ' TLRY', ' CRON', ' ACB', ' NBEV', ' CRBP', ' TGODF', ' TRTC', ' CANN', ' MJ', ' MSBHF', ' MITSY', ' SSUMY',
' ITOCY', ' MARUY', ' TGC', ' TCDA', ' REPH', ' TPIC', ' GTT', ' ANGN', ' RAAS', ' HTOO', ' AGIO', ' SQQQ', ' SVC', ' CDNA', ' COKE',
' AVXL', ' XTNT', ' AFI', ' FSR', ' QUIK', ' CD', ' RILY', ' SLCA', ' LMAT', ' HOVNP', ' QEMM', ' CNNE', ' AIG', ' NURE', ' RFDA',
' PMAR', ' UHAL', ' FLQL', ' ABST', ' ACMR', ' ADTN', ' AEHR', ' AEY', ' AEYE', ' AFRM', ' AGMH', ' AGYS', ' AI', ' AKAM', ' AIRG',
' ALGM', ' ALLT', ' ALOT', ' ALTR', ' ALYA', ' AMBA', ' AMST', ' AMSWA', ' ANET', ' ANSS', ' ANY', ' AOSL', ' APH', ' API', ' APPN',
' ARRY', ' APPS', ' ARW', ' ASUR', ' ASYS', ' ATC', ' ATEN', ' ATOM', ' AUDC', ' AUUD', ' AVGO', ' AVNW', ' AVT', ' AXTI', ' AYX',
' AZPN', ' BDR', ' BCOV', ' BELFB', ' BHE', ' BILL', ' BKI', ' BKTI', ' ABR', ' AAXJ', ' AAME', ' RDS.A', ' RDS.B', ' NTDOY', ' AVID',
' TTWO', ' CCOEF', ' PLTK', ' ZNGA', ' SKLZ', ' UBSFY', ' OTGLY', ' GLUU', ' TSCRD', ' GRVY', ' NGMS', ' ENGMF', ' MSGM', ' SCPL', ' BRGGF',
' INSE', ' RNWK', ' MLLLF', ' VS', ' GMGI', ' SLGG', ' BHAT', ' GIGM', ' YVR', ' F', ' PLUG', ' RKT', ' TSNP', ' RLLCF', ' BAYP',
' LPSN', ' TRIP', ' WW', ' BLUE', ' SFIX', ' MMYT', ' VICR', ' DNLI', ' VST', ' ENV', ' FLR', ' SPCE', ' BKRKF', ' ZIJMF', ' FL',
' REGI', ' APPH', ' FOCS', ' ROOT', ' ADT', ' EIPAF', ' NKLA', ' ABML', ' TSNPD', ' DJI', ' IXIC',
' 9684.T', ' 9697.T', ' 9766.T', ' 3659.T', ' 7974.T', ' TOR', ' OTC', ' CX', ' BECN', ' JELD', ' FRTA', ' MI', ' EME',
' BEKE', ' PLD', ' WELL', ' SPG-PJ', ' PSA-PK', ' PSA-PH', ' DLR', ' CBRE', ' WY', ' O', ' ARE', ' DLR-PJ', ' DLR-PC', ' INVH',
' ESS', ' SCCO', ' NEM', ' MLM', ' MANU', ' ASR', ' MRAAF', ' JUVE.MI', ' RFC', ' SSL.MI', ' BVB.DE', ' AJAX.AS', ' ASR.MI',
' RACE.MI', ' LINK-USD', ' XLM-USD', ' DOGE-USD', ' XEM-USD', ' XMR-USD', ' ATOM1-USD', ' DOT1-USD', ' DOT2-USD', ' BTC-USD', ' ETH-USD', ' BCH-USD',
' ATOM2-USD', ' MIOTA-USD', ' THETA-USD', ' TRX-USD', ' BSV-USD', ' EOS-USD', ' SOL1-USD', ' SOL2-USD', ' USDC-USD', ' NEO-USD', ' XTZ-USD', ' VET-USD',
' DASH-USD', ' ALGO-USD', ' CCOEY', ' KNMCY', ' SQNXF', ' SGAMY', ' ADA-USD', ' BNB-USD', ' XRP-USD', ' LTC-USD',
' NCBDF')


selected_stock = st.selectbox('Select stock you want to predict', stocks)

n_years = st.slider('Years of prediction:', 1, 3)
period = n_years * 365


@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data


data_load_state = st.text('Loading data...')

data = load_data(selected_stock)
data_load_state.text('Loading data... done!')

st.subheader('Raw data')
st.write(data.tail())

# Plot raw data
def plot_raw_data():
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
    fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
    fig.layout.update(title_text='Time Series Data without forcast', xaxis_rangeslider_visible=True)
    st.plotly_chart(fig)

plot_raw_data()




# Predict forecast with Prophet.
df_train = data[['Date','Close']]
df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

m = Prophet()
m.fit(df_train)
future = m.make_future_dataframe(periods=period)
forecast = m.predict(future)

#Show cat GIF
#if m.predict(future) == True:
#    st.markdown("![Alt Text](https://media.giphy.com/media/lLo0vQHigkMzGETtu/giphy.gif)")


# Show and plot forecast
#st.subheader('Forecast data')
st.markdown("<h2 style='text-align: center; color: black;'>Forcast data set</h2>", unsafe_allow_html=True)
st.write(forecast.tail())
    
st.markdown("<h2 style='text-align: center; color: white;'>   </h2>", unsafe_allow_html=True)

#st.write(f'Forecast plot for {n_years} year/s')
st.markdown("<h2 style='text-align: center; color: black;'>Forecast plot </h2>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center; color: black;'>You can use the slider to select the range of years </h3>", unsafe_allow_html=True)
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.markdown("<h2 style='text-align: center; color: black;'>Forcast Trends </h2>", unsafe_allow_html=True)

st.write(" ")
fig2 = m.plot_components(forecast)
st.write(fig2)

st.markdown("<h2 style='text-align: center; color: white;'>   </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>  </h2>", unsafe_allow_html=True)


link = '[Buy me a coffee](https://www.buymeacoffee.com/MaxMnemo)'
st.markdown(link, unsafe_allow_html=True)

link = '[My website](http://mnemo.uk)'
st.markdown(link, unsafe_allow_html=True)

link = '[Instagram](https://www.instagram.com/max_mnemo/)'
st.markdown(link, unsafe_allow_html=True)

link = '[Github Repo](https://github.com/facebook/prophet)'
st.markdown(link, unsafe_allow_html=True)




# In[ ]:




