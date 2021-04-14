
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

st.markdown("<h5 style='text-align: center; color: black;'>(Please note that the results are not a guarantee and you buy stocks at your own risk. With this project I wanted to enable people to apply machine learning to their stocks. If an error occurs the stock is not in my stock list. Prices are in US dollars. I also added crypto currencies </h5>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color: black;'>                 </h5>", unsafe_allow_html=True)

st.markdown("<h5 style='text-align: center; color: black;'>                 </h5>", unsafe_allow_html=True)



stocks = (' AAPL', ' GOOG', ' AMZN', ' TSLA', ' FB', ' GME', ' MSFT', ' ADBE', ' ORCL', ' SNPS', ' VRSN', ' ACN', ' IBM', ' CRM', ' NOW', ' FIS', ' FISV', ' ADSK', ' INTU', ' COMMU', ' CSCO', ' AMAT', ' APH', ' HPQ', ' MSI', ' V', ' DIS',
' CMCSA', ' VZ', ' T', ' TMUS', ' NFLX', ' CHTR', ' NVDA', ' AVGO', ' QCOM', ' TXN', ' MU', ' AMD', ' XLNX', ' MCHP', ' ADI', ' JPM', ' BAC', ' BRK-B', ' AXP', ' COF', ' C', ' WFC', ' USB', ' PNC', ' MS', ' GS', ' SCHW', ' RF', ' ICE', ' SPGI',
' CME', ' MSCI', ' BLK', ' BK', ' STT', ' AON', ' MET', ' GL', ' L', ' BSX', ' BIO', ' EW', ' MDT', ' SYK', ' ABT', ' TMO', ' DHR', ' A', ' IQV', ' MTD', ' PFE', ' JNJ', ' MRK', ' ABBV', ' AMGN', ' GILD',
' FISV', ' BMY', ' LYV', ' EA', ' ATVI', ' UNH', ' G' ,' HUM', ' LOW', ' HD', ' MCD', ' SBUX', ' NKE', ' BKNG', ' TJX', ' ROST', ' SPECIA', ' BLL', ' LODGI', ' XOM', ' CVX', ' PSX', ' MPC', ' OKE', ' EOG', ' AMT', ' EQIX', ' SBAC', ' O', ' SPG',
' PSA', ' CCI', ' D', ' SRE', ' PEG', ' ETR', ' ED', ' EIX', ' XEL', ' DUK', ' NEE', ' SO', ' ES', ' WEC', ' APD', ' DD', ' CE', ' SHW', ' LIN', ' WM', ' RSG', ' SWK', ' BA', ' RTX', ' NOC', ' LMT', ' GD', ' LHX', ' GE', ' MMM', ' HON', ' ITW', 
' EMR', ' ROP', ' PH', ' IR', ' CAT', ' ADP', ' EFX', ' VRSK', ' ADP', ' JCI', ' GIS', ' KHC', ' K', ' SYY', ' STZ', ' MDLZ', ' MO', ' PM', ' KO', ' COP', ' VTR', ' ASML', ' NVS', ' MRVL', ' BIP', ' AMX', ' FMX', ' FN', ' RE', ' BEP', ' EC', 
' VALE', ' ITUB', ' ABEV', ' XP', ' BBD', ' PBR', ' MELI', ' BSBR', ' GOLD', ' NTR', ' CNQ', ' KL', ' GIB', ' SAP', ' TOT', ' AZN', ' BP', ' BTI', ' NGG', ' PUK', ' VOD', ' DEO', ' HSBC', ' RIO', ' UL', ' TT', ' APTV', ' SAN', ' BBVA', ' TEF',
' BUD', ' NXPI', ' PHG', ' DB', ' GSK', ' CCEP', ' FTCH', ' QSR', ' MGA', ' WPM', ' NVO', ' CB', ' SPOT', ' ABB', ' ALC', ' CS', ' MT', ' GFI', ' PAND', ' KOSS', ' DYNT', ' ACY', ' STXS', ' PUBM', ' SEAS', ' PDCE', ' TS', ' WOW', ' CDXC', ' ACIA', 
' PTVCB', ' CRTO', ' PMBC', ' LORL', ' PRA', ' ASRV', ' SSNT', ' SFBC', ' INFR', ' ASLN', ' ARD', ' AGR', ' AAON', ' ACIW', ' ADAP', ' ULBI', ' NCTY', ' PING', ' RETO', ' HCC', ' CLGN', ' SOS', ' ITP', ' USPH', ' PNRG', ' RYI', ' IIPR', ' FROG', 
' SNSE', ' POSH', ' OPT', ' KUKE', ' UAMY', ' BVS', ' QLI', ' WOOF', ' AMC', ' UVXY', ' T', ' AAOI', ' ABNB', ' ACHC', ' SSY', ' COHU', ' NAKD', ' BCE', ' MRNA', ' TWTR', ' BBY', ' WMT', ' SE', ' OKTA', ' TGT', ' KR',
' SHOP', ' CNI', ' ENB', ' BNS', ' BAM', ' LULU', ' TRP', ' TRI', ' BCE', ' CM', ' BMO', ' CP', ' MFC', ' SLF', ' TU', ' FNV', ' RCI', ' BILI', ' NTES', ' DELL', ' SPLK', ' VIAC', ' BURL', ' COST', ' WDAY', ' TLIS', ' DBTX', ' DVN', ' PLTR', 
' AA', ' AADR', ' AAL', ' AAMC', ' AAP', ' MSFT', ' MRVI', ' KSS', ' PRGO', ' AEP', ' SQM', ' DASH', ' COO', ' SNOW', ' AZO', ' ZM', ' IEP', ' NIO', ' VEEV', ' ZLAB', ' DLTR', ' OPEN', ' TSM', ' BABA', ' GOOGL', ' BRK-A', ' MA', ' PG', 
' PYPL', ' INTC', ' PDD', ' UNP', ' UPS', ' SNE', ' RY', ' DE', ' ARCC', ' SXY', ' IMKTA', ' MSGN', ' KBAL', ' UBA', ' HFC', ' CXW', ' TAP', ' DBI', ' GEO', ' DISCA', ' QRTEA', ' ALL', ' WDC', ' UNIT', ' RPT', ' DNOW',
' LUMN', ' QRVO', ' TCOM', ' ROIC', ' CVS', ' NOV', ' GM', ' MCO', ' LSXMK', ' TKA', ' 1COV', ' DBK', ' DB1', ' FME', ' CON', ' HEN3', ' ALV', ' LLOY', ' RR', ' IAG', ' BARC', ' GLEN', ' HSBA', ' TSCO', ' NWG', ' SMDS', ' RDSB', ' STAN', ' TW', 
' AV', ' BATS', ' NOK', ' QS', ' TDOC', ' PZZA', ' BB', ' LI', ' QQQ', ' SCR', ' ARKK', ' WAMCX', ' IEC', ' TCEHY', ' HLT', ' PINS', ' BIOPX', ' TWLO', ' UPLD', ' W', ' TNC', ' MPGFX', ' MAT', ' FCX', ' IAC', ' ETSY', ' PTON', ' JAGX', ' CCIV', 
' SNDL', ' ZOM', ' MOMO', ' MYO', ' MENXF', ' TM', ' SFTBF', ' NTDMF', ' FRCOF', ' NPPXF', ' NNDNF', ' NTDOF', ' KDDIF', ' SHECF', ' MUFG', ' MRAAF', ' TAK', ' HMC', ' ITOCF', ' SVNDF', ' MFG', ' MIELF', ' ALPMF', ' 7832.T',
' CGC', ' SMG', ' GWPH', ' TLRY', ' CRON', ' ACB', ' NBEV', ' CRBP', ' TGODF', ' TRTC', ' CANN', ' MJ', ' MSBHF', ' MITSY', ' SSUMY', ' ITOCY', ' MARUY', ' TGC', ' TCDA', ' REPH', ' TPIC', ' GTT', ' ANGN', ' RAAS', ' HTOO', ' AGIO', ' SQQQ', ' SVC', 
' CDNA', ' COKE', ' AVXL', ' XTNT', ' AFI', ' FSR', ' QUIK', ' CD', ' RILY', ' SLCA', ' LMAT', ' HOVNP', ' QEMM', ' CNNE', ' AIG', ' NURE', ' RFDA', ' PMAR', ' UHAL', ' FLQL', ' ABST', ' ACMR', ' ADTN', ' AEHR', ' AEY', ' AEYE', ' AFRM', ' AGMH', 
' AGYS', ' AI', ' AKAM', ' AIRG', ' ALGM', ' ALLT', ' ALOT', ' ALTR', ' ALYA', ' AMBA', ' AMST', ' AMSWA', ' ANET', ' ANSS', ' ANY', ' AOSL', ' APH', ' API', ' APPN', ' ARRY', ' APPS', ' ARW', ' ASUR', ' ASYS', ' ATC', ' ATEN', ' ATOM', ' AUDC', 
' AUUD', ' AVNW', ' AVT', ' AXTI', ' AYX', ' AZPN', ' BDR', ' BCOV', ' BELFB', ' BHE', ' BILL', ' BKI', ' BKTI', ' ABR', ' AAXJ', ' AAME', ' RDS.A', ' RDS.B', ' NTDOY', ' AVID', ' TTWO', ' CCOEF', ' PLTK', ' ZNGA', ' SKLZ', ' UBSFY', ' OTGLY', 
' GLUU', ' TSCRD', ' GRVY', ' NGMS', ' ENGMF', ' MSGM', ' SCPL', ' BRGGF', ' INSE', ' RNWK', ' MLLLF', ' VS', ' GMGI', ' SLGG', ' BHAT', ' GIGM', ' YVR', ' F', ' RKT', ' TSNP', ' RLLCF', ' BAYP', ' LPSN', ' TRIP', ' WW', ' BLUE', ' SFIX', ' MMYT', 
' VICR', ' DNLI', ' VST', ' ENV', ' FLR', ' SPCE', ' BKRKF', ' ZIJMF', ' FL', ' REGI', ' APPH', ' FOCS', ' ROOT', ' ADT', ' EIPAF', ' NKLA', ' ABML', ' TSNPD', ' DJI', ' IXIC', ' 9684.T', ' 9697.T', ' 9766.T', ' 7974.T', ' 3659.T', ' 7974.T', ' TOR', 
' OTC', ' CX', ' BECN', ' JELD', ' FRTA', ' MI', ' EME', ' BEKE', ' PLD', ' WELL', ' SPG-PJ', ' PSA-PK', ' PSA-PH', ' DLR', ' CBRE', ' WY', ' O', ' ARE', ' DLR-PJ', ' DLR-PC', ' INVH', ' ESS', ' SCCO', ' NEM', ' MLM', ' MANU', ' ASR', ' MRAAF', 
' JUVE.MI', ' RFC', ' SSL.MI', ' BVB.DE', ' AJAX.AS', ' ASR.MI', ' RACE.MI', ' LINK-USD', ' XLM-USD', ' DOGE-USD', ' XEM-USD', ' XMR-USD', ' ATOM1-USD', ' DOT1-USD', ' DOT2-USD', ' BTC-USD', ' ETH-USD', ' BCH-USD', ' ATOM2-USD', ' MIOTA-USD', 
' THETA-USD', ' TRX-USD', ' BSV-USD', ' EOS-USD', ' SOL1-USD', ' SOL2-USD', ' USDC-USD', ' NEO-USD', ' XTZ-USD', ' VET-USD', ' DASH-USD', ' ALGO-USD', ' CCOEY', ' KNMCY', ' SQNXF', ' SGAMY', ' ADA-USD', ' BNB-USD', ' XRP-USD', ' LTC-USD',
' NCBDF', ' NVFY', ' GC=F', ' BZ=F', ' SI=F', ' HG=F', ' EURUSD=X', ' GBPUSD=X', ' EURGBP=X', ' EURCHF=X', ' EURJPY=X', ' JPYUSD=X', ' AUDUSD=X', ' CADUSD=X', ' 0Q0C.L', ' 0SOM.L', ' 0IBD.L', ' 0SJQ.L', ' WRES.L', ' 0DZ3.L', ' 7B7.F', ' TGKB.ME', 
' VTBR.ME', ' SYME.L', ' FEES.ME', ' TGKBP.ME', ' 88E.L', ' F', ' GUNKUL-R.BK', ' GUNKUL.BK', ' 000725.SZ', ' VIVA.JK', ' TRITN.BK', ' TRITN-R.BK', ' 003535.KS', ' 066910.KQ', ' 1543.HK', ' STOXX50E', ' XIACF', ' BMW.DE', ' BAYN.DE', 
' BAYRY', ' SIE.DE', ' VOW3.DE', ' BAS.DE', ' DAI.DE', ' SAP.DE', ' ALV.DE', ' RWE.DE', ' EOAN.DE', ' DTE.DE', ' MUV2.DE', ' ^IXIC', ' ^DJI', ' ^RUT', ' CL=F', ' ^GSPC', ' HBAR-USD', ' CTC1-USD', ' EGLD-USD', ' LUNA2-USD', ' ZIL-USD', ' STX1-USD', 
' DCR-USD', ' ZEC-USD', ' TFUEL-USD', ' BAT-USD', ' ETC-USD', ' CCXX-USD', ' RVN-USD', ' SC-USD', ' ICX-USD', ' ONT-USD', ' ONE2-USD', ' CEL-USD', ' ZRX-USD', ' WAVES-USD', ' QTUM-USD', ' BNT-USD', ' OMG-USD', ' XWC-USD', ' IOST-USD', ' BTG-USD',
' NANO-USD', ' ZEN-USD', ' LRC-USD', ' STORJ-USD', ' MED-USD', ' KNC-USD', ' SNT-USD', ' GLM-USD', ' ARK-USD', ' ANT-USD', ' FUN-USD', ' MAID-USD', ' EWT-USD', ' IOTX-USD', ' VLX-USD', ' WAXP-USD', ' WAN-USD', ' ARDR-USD', ' REP-USD', ' STEEM-USD', 
' MARO-USD', ' STRAX-USD', ' TT-USD', ' NKN-USD', ' BTM-USD', ' TOMO-USD', ' ATRI-USD', ' BCD-USD', ' COTI-USD', ' GNO-USD', ' RLC-USD', ' IRIS-USD', ' NCLH', ' TME', ' ^IXIC', ' ^VIX', ' IMOEX.ME', ' ^N225', ' UNFI', ' ASO', ' LPL', ' RIOT', 
' AMKR', ' IGMS', ' KLIC', ' MARA', ' CNNC', ' NNOX', ' NINOF', ' RBLX', ' CAN', ' ETSY', ' CEMI', ' ZOM', ' JBLU', ' ACAD', ' CHPT', ' ABC.L', ' ATHM', ' HSTM', ' JOBS', ' TUI1.DE', ' TKA.DE', ' LHA.DE', ' CBK.DE', ' LIN.DE', ' GILT', ' UAV.L', 
' WDI.F', ' ZEF.F', ' P5TA.F', ' W6O.F', ' GSG.F', ' AWL1.F', ' IFX.DE', ' SRT3.DE', ' RAA.DE', ' WIN.DE', ' LEO.DE', ' JEN.DE', ' SSU.DE', ' INL.F', ' CIS.F', ' TII.F', ' TSFA.F', ' RMO', ' ^GDAXI', ' HEN.DE', ' EVK.DE', ' SY1.DE', ' LXS.DE', 
' FPE3.DE', ' WCH.DE', ' SDF.DE', ' DUP.F', ' DCH1.F', ' AIL.F', ' DLY.F', ' ADS.DE', ' BEI.DE', ' PSM.DE', ' SPR.DE', ' BOSS.DE', ' PUM.DE', ' JNJ.F', ' PRG.F', ' CCC3.DE', ' ITK.DE', ' WDP.F', ' PEP.DE', ' 4I1.DE', ' PHM7.F', ' MMM.F', ' LOR.F', 
' MOH.F', ' AOL1.F', ' GUI.DE', ' CPA.F', ' NFC.DE', ' FRE.DE', ' MRK.DE', ' PFE.F', ' NOT.F', ' UNH.F', ' AMG.DE', ' 2M6.DE', ' SNW.F', ' GIS.DE', ' 4AB.F', ' GS7.DE', ' LLY.F', ' AGN', ' IDP.DE', ' DPW.DE', ' VNA.DE', ' DWNI.DE', ' FRA.DE', 
' LEG.DE', ' GIB.F', ' GIB.F', ' SIX2.DE', ' NNZA.BE', ' UPAB.F', ' SPG.F', ' CY2.F', ' AOT.F', ' SOBA.F', ' DRI.DE', ' BAC.DE', ' MCN.F', ' NTT.F', ' VODI.DE', ' MNW.F', ' DIP.F', ' TM5.F', ' TSTA.F', ' BTQ.F', ' TNE5.F', ' FTE.F', ' CIS.F', 
' GEC.F', ' AAPL.F', ' ZAL.DE', ' G24.DE', ' WDI.DE', ' FNTN.DE', ' RKET.DE', ' ABEC.DE', ' MSF.F', ' AMZ.F', ' FB2A.DE', ' NNND.DE', ' AHLA.F', ' ORC.F', ' QCI.F', ' CSA.F', ' IOY.SG', ' SFT.F', ' ADB.F', ' FOO.DE', ' YHO.F', ' 2HP.DE', ' EBA.DE', 
' NSU.DE', ' UAL1.F', ' TOM.DE', ' HDM.F', ' GM.SW', ' FMC1.DE', ' NISA.F', ' TL0.DE', ' HYU.F', ' RNL.F', ' VOL1.F', ' PEU.F', ' SUK.F', ' FMC.DE', ' HOT.DE', ' HEI.DE', ' CAT1.F', ' IXD1.DE', ' UTC1.DE', ' LWE.F', ' ILT.F', ' KMY.DE', ' SQU.F', 
' ACOF.F', ' DCO.DE', ' KD8.HM', ' MEO.DE', ' UTDI.DE', ' PAH3.DE', ' INH.DE', ' BRH.F', ' ALD.F', ' TN8.F', ' SOT.F', ' ENL.F', ' H4W.F', ' WF3.F', ' FIE.DE', ' TTK.DE', ' HBH.DE', ' WMT.F', ' HDI.DE', ' MDO.F', ' PCE1.DE', ' CTO.F', ' DYH.F', 
' CVC1.DE', ' HMSB.DE', ' CAR.F', ' TCO.F', ' SRB.DE', ' SY1.DE', ' FME.DE', ' RHKG.DE', ' AFX.DE', ' MOR.DE', ' BNTX', ' ^STOXX50E', ' BEKE', ' DDOG', ' AAGH', ' ROKU', ' EH', ' SFIX', ' VLDR', ' TOSYY', ' INVU', ' SNCY', ' AFTPY', ' IQ', ' RVLV', 
' STLFF', ' GOEV', ' QTRX', ' LOGI', ' ZS', ' RCKT', ' UCTT', ' DSP', ' RLAY', ' GSAT', ' SAIA', ' BEAM', ' GCTAY', ' APHA', ' WKEY', ' XL', ' HYLN', ' PTEN', ' DHT', ' FGEN', ' WPG', ' FBASF', ' RMO', ' LTRPB', ' MKTY', ' IKNA', ' ACHL',
' GASS', ' MERC', ' CGEM', ' AMR', ' JT', ' VCTR', ' CTG', ' VIVO', ' EXPR', ' HOLX', ' BWA', ' DHI', ' SBSW', ' EBAY', ' LEN', ' CE', ' TLK', ' SNP', ' TEF', ' EBR-B', ' EBR', ' PPL', ' SHG', ' PKX', ' ORAN', ' VIV', ' REGN', ' FE',
' FMS', ' FRE.DE', ' 11C.F', ' PSHD.L', ' GXI.DE', ' HFG.DE', ' PLUG.DE', ' COIN', ' SEED', ' NOEC', ' COUR', ' AVD', ' IPI', ' EEM', ' MFS=F', ' MME=F', ' EWZ', ' EFA', ' DOCN', ' OLO', ' ACVA', ' ACHL', ' IMCR', ' TUYA', ' DSGN', ' IO', ' SEEL', 
' BBQ', ' FIXX', ' CXW', ' GALT', ' MAXN', ' GRAY', ' LHX', ' ODT', ' LW', ' LHDX', ' ISIG', ' BSIG', ' NFH', ' JRO', ' OUST', ' TPCO', ' ALRM', ' CAG', ' BNSO', ' JDCMF', ' YUMC', ' EDU', ' TAL', ' WEED.TO', ' TAB', ' TGOD.TO', ' TGODF', ' YM=F', 
' ES=F', ' NQ=F', ' RTY=F', ' ^FTSE', ' ^CMC200', ' PDD', ' BIDU', ' VIPS', ' WB', ' YY', ' DADA', ' ZH', ' DOYU', ' DAO', ' SOGO', ' BZUN', ' CANG', ' SOHU', ' JFIN', ' LIZI', ' BLCT', ' MTD', ' ILMN', ' USDRUB=X', ' USDJPY=X', ' USDCAD=X',
' JWEL', ' OCG', ' JD', ' KWEB', ' CQQQ', ' KBA', ' MCHI', ' CHIQ', ' 03690', ' QTEC', ' IXN', ' IGV', ' FTEC', ' IYW', ' FDN', ' VGT', ' XLK', ' VOO', ' ESGU', ' O', ' IPO', ' LTC', ' STAG', ' DX', ' MAIN', ' PSEC', ' GLAD', ' GOOD',
' DSL', ' FOF', ' GLD', ' TEAF', ' VCSH', ' YELP', ' TTD', ' ZG', ' MMC', ' RH', ' ADJ.DE', ' PAT.DE', ' TLG.DE', ' TEG.DE', ' DWNI.DE', ' AOX.DE', ' HHFA.DE', ' HABA.DE', ' INS.F', ' IVZ', ' BRPHF', ' FUTU', ' OXY', ' O1E.SG', ' POQ.F', ' B7BA.SG',
' DBK.DE', ' SIGL', ' SAX.DE', ' H50E.L', ' H5E.DE', ' CVCO', ' D2BA.HM', ' XLE', ' SDGR', ' UBER', ' LILA', ' LILAK', ' BXP', ' URG', ' DNN', ' UUUU', ' CCJ', ' NXE', ' UEC', ' KWS.DE', ' SKB.DE', ' CWC.DE', ' STLD', ' NUE', ' TX', ' SQ',
' GPN', ' U', ' CRWD', ' NET', ' CSGP', ' LBRDK', ' VUG', ' CCL', ' SAIC', ' HHC', ' LOV', ' SRG', ' ESTC', ' PFSI', ' GTYH', ' MAXR', ' ADV', ' AHCO', ' SMHI', ' GOCO', ' APO', ' KEYS', ' OSPN', ' ANF', ' VICI', ' KDP', ' CMI', ' NLS',
' SONO', ' ED', ' SPG', ' ATEX', ' FAST', ' IRWD', ' OTIS', ' VTA', ' NSC', ' ATGE', ' FUBO', ' CET', ' CERN', ' HBB', ' W', ' DXC', ' FPH', ' ORCL', ' SRGA', ' GTX', ' FCNCA', ' ORI', ' EDP', ' EPD', ' TALO', ' YALA', ' LRCX', ' DEN', ' ALLY', ' LRCX',
' JEF', ' SIBN', ' ATKR', ' TCS', ' MBUU', ' VWS', ' ISRG', ' SJM', ' NVT', ' PGR', ' NTRS', ' OMC', ' AN', ' ATCO', ' GRBK', ' NGA', ' BNGO', ' BFT', ' SPWR', ' MVIS', ' CAPA', ' CLII', ' THCX', ' Z', ' SPRT', ' LAZR', ' UPST', ' RH', ' INTC', ' INX',
' PSAC', ' ENPH', ' LI', ' FSLY', ' SSPK', ' AABB', ' LMND', ' MP', ' SPY', ' DYAI', ' RCKY', ' SLQD', ' PLAY', ' GGTTF', ' KDSS', ' RDFN', ' CCL', ' LTUM', ' TMBR', ' ARCT', ' PLNHF', ' EYES', ' FLT', ' IP', ' FTNT', ' OM', ' SHV', ' XLV', ' THO', ' AGRX',
' HOFV', ' GHVI', ' CPNG', ' 5Q5.F', ' BC8.DE', ' NEM.DE', ' QIA.DE', ' COK.DE', ' SOW.DE', ' CON.DE', ' VOW.DE', ' DB1.DE', ' STOR', ' IRM', ' APTS', ' NLY', ' NRZ', ' AFL', ' TD', ' TROW', ' LQT', ' BNDX', ' IEF', ' IEI', ' SHY', ' EL',
' AEON-USD', ' NPC-USD', ' GBYTE-USD', ' OWC-USD', ' ARRR-USD', ' MCO-USD', ' ATB-USD', ' FLASH-USD', ' DIME-USD', ' SFT-USD', ' EMC2-USD', ' GRC-USD', ' BCA-USD', ' DCY-USD', ' META-USD', ' NYZO-USD', ' MGO-USD', ' ALIAS-USD', ' CET-USD', ' COMP1-USD',
' BDX-USD', ' BRC-USD', ' PART-USD', ' PAI-USD', ' NMC-USD', ' XAS-USD', ' CURE-USD', ' CUT-USD', ' BCH-USD', ' FRST-USD', ' DDK-USD', ' HNC-USD', ' FSN-USD', ' DFI-USD', ' KDA-USD', ' LOKI-USD', ' PLC-USD', ' GAS-USD', ' DTEP-USD', ' OTO-USD',
' RINGX-USD', ' PI-USD', ' NULS-USD', ' ZVC-USD', ' CCA-USD', ' DERO-USD', ' PLC-USD', ' XMC-USD', ' MINT-USD', ' NVCR', ' DFIFF', ' MSTR', ' ANGI', ' NVAX', ' CSPCY', ' LTCN', ' FLGT', ' LKNCY', ' HMBL', ' KHOTF', ' SSL', ' OSTK', ' TWST', ' EM', ' SUMO',
' MRRTY', ' AJMPF', ' TTM', ' CDE', ' IRTC', ' OMAB', ' NSTG', ' ALBKF', ' SPT', ' PLAN', ' DOCU', ' USNZY', ' TEAM', ' HL', ' VNOM', ' ACH', ' AGI', ' SKM', ' ACOPF', ' MYTE', ' WISH', ' TKAYY', ' OLK', ' RARE', ' TRUMY', ' UPWK', ' GGB', ' ATDRY', ' SSTK',
' TXG', ' SYIEY', ' PPRUY', ' KC', ' CRSP', ' TMVWY', ' WIX', ' VIR', ' NPSNY', ' SBRCY', ' NG', ' HOKCF', ' AUOTY', ' ORGO', ' XISHY', ' CDLX', ' SANA', ' PPERF', ' TIL', ' ADS', ' ARVL', ' YNDX', ' AEIS', ' RDY', ' CROX', ' EBS', ' SAGE', ' LGORF',  
' WHD', ' VCEL', ' UAA', ' OI', ' SYF', ' BKE', ' GDRX', ' JWN', ' MATX', ' CADE', ' JW-A', ' WRK', ' THRM', ' MPNGY', ' CLVLY', ' CMSQY', ' VTVT', ' MFNC', ' DMRC', ' MFCN', ' CBLI', ' MUDS', ' OBAS', ' AGC', ' BTX', ' ATXI', ' LHDX', ' GBOX',
' UK', ' PLBY', ' GFED', ' CGA', ' AGCUU', ' AEE', ' MSB', ' CSSE', ' WCN', ' TIRX', ' OGI', ' NLSP', ' SNDL', ' CTRM', ' CNET', ' KRUS', ' SCR', ' RVPH')



selected_stock = st.selectbox('Select the ticker symbol for the stock you want to predict', stocks)

n_years = st.slider('Years of prediction:', 1, 2)
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
st.markdown("<h3 style='text-align: center; color: black;'>Use the slider to select the range of years </h3>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Data entries above the blue line = overvalued </h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: black;'>Data entries underneath the blue line = undervalued </h4>", unsafe_allow_html=True)
fig1 = plot_plotly(m, forecast)
st.plotly_chart(fig1)

st.markdown("<h2 style='text-align: center; color: black;'>Forcast Trends </h2>", unsafe_allow_html=True)

st.write(" ")
fig2 = m.plot_components(forecast)
st.write(fig2)

st.markdown("<h2 style='text-align: center; color: white;'>   </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>  </h2>", unsafe_allow_html=True)


st.markdown("<h4 style='text-align: center; color: black;'>The yearly chart is the most interesting one. It shows you the buy and sell trends for each month.      </h4>", unsafe_allow_html=True)


st.markdown("<h4 style='text-align: center; color: black;'>Chart goes down = People were selling stocks       </h4>", unsafe_allow_html=True)


st.markdown("<h4 style='text-align: center; color: black;'>Chart goes up = People were buying stocks       </h4>", unsafe_allow_html=True)


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

link = '[Activity of super investors](https://www.dataroma.com/m/home.php)'
st.markdown(link, unsafe_allow_html=True)


st.markdown("<h2 style='text-align: center; color: white;'>   </h2>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: white;'>  </h2>", unsafe_allow_html=True)


st.markdown("<h4 style='text-align: center; color: black;'>________________________________________________________________________________</h4>", unsafe_allow_html=True)

st.markdown("<h2 style='text-align: center; color: white;'>   </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>  </h2>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: black;'>                                                                                                                           </h4>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: black;'>Use my app as a longterm tool to guide your decisions, not as a short final answer to make quick profits. There are so many factors influencing the stock market.      </h4>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: black;'>Whether Elon Musk tweets to use signal and everyone agrees to buy a random stock named signal that has nothing to do with the messenger app or antagonist behaviour like people massively betting against hedgefunds on the Gamestop stock, these activities are hard to predict. </h4>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: black;'>Some basic tips: Stay away from day trading. Hold your stocks. Don't panic sell when your stocks hit a low phase. Diversify, don't put everything into 1 or 2 stocks and inform yourself about the company you are invested in. What are the profits, market cap, does the company have competitors, is the overall branch of the company worth investing, does the company care for adding more value (investing in their IT infrastructure), what's the behaviour of insider trades (do people accumulate or sell stocks), is the country politically stable, what is the legal framework of the company, is the stock cyclic and volatile or does it grow stable and steadily, does the barfin smell something fishy, .......    </h4>", unsafe_allow_html=True)

st.markdown("<h4 style='text-align: center; color: black;'>Also take overall excitement and recommendations of people about a stock with a grain of salt and see people with a 100% guarantee to buy something as a big red flag.</h4>", unsafe_allow_html=True)

st.markdown("<h3 style='text-align: center; color: black;'>Inflation: </h3>", unsafe_allow_html=True)



st.markdown("<h4 style='text-align: center; color: black;'>My predictions are saying that there are so many overvalued stocks that we are heading towards inflation in the next years. Buyers are getting greedy right now and a market crash is not that unlikely. </h4>", unsafe_allow_html=True)


st.markdown("<h4 style='text-align: center; color: black;'>There must be a counter value to these rising stocks. People invest in real estate while at the same time the unemployment rate rises and people can't pay their rent anymore. People are investing into businesses and expect the stock to rise while at the same time businesses keep fighting for their existence because of the pandemic...</h4>", unsafe_allow_html=True)



st.markdown("<h4 style='text-align: center; color: black;'>But ending with a positive thought, I must say that I see correlations between my predictions and people's behaviour in the stock market. Buy the roumour, sell the news. Over valued stocks in my predictions are oftentimes in the news or they are mentioned in economic newspapers as a buy recommendation. Think rational, use statistics as in my app, evaluate the numbers and hold. </h4>", unsafe_allow_html=True)

