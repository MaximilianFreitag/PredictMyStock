from datetime import date
import streamlit as st
import yfinance as yf
from fbprophet import Prophet
from fbprophet.plot import plot_plotly
from plotly import graph_objs as go



st.set_page_config(
        page_title='Predict My Stocks                 ',
        page_icon="📈"
        )

st.markdown("<h1 style='text-align: center; color: black;'>Predict My Stocks</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: black;'>Enter your stock and wait 10-20 seconds for the machine learning code to process the data </h2>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'>(Please note that the results are not a guarantee and you buy stocks at your own risk. With this project I wanted to enable people to apply machine learning code to their stocks for free. If an error occurs the stock is not in my stock list. Prices are in US dollars. I also added crypto currencies (e.g. BTC-USD, ETH-USD,...)</h5>", unsafe_allow_html=True)
st.markdown("<h5 style='text-align: center; color: black;'>                 </h5>", unsafe_allow_html=True)


st.markdown("<h2 style='text-align: center; color: white;'>  </h2>", unsafe_allow_html=True)

stock_name = (' AAPL', ' GOOG', ' AMZN', ' TSLA', ' FB', ' GME', ' MSFT', ' ADBE', ' ORCL', ' SNPS', ' VRSN', ' ACN', ' IBM', ' CRM', ' NOW', ' FIS', ' FISV', ' ADSK', ' INTU', ' COMMU', ' CSCO', ' AMAT', ' APH', ' HPQ', ' MSI', ' V', ' DIS',
' CMCSA', ' VZ', ' T', ' TMUS', ' NFLX', ' CHTR', ' NVDA', ' AVGO', ' QCOM', ' TXN', ' MU', ' AMD', ' XLNX', ' MCHP', ' ADI', ' JPM', ' BAC', ' BRK-B', ' AXP', ' COF', ' C', ' WFC', ' USB', ' PNC', ' MS', ' GS', ' SCHW', ' RF', ' ICE', ' SPGI',
' CME', ' MSCI', ' BLK', ' BK', ' STT', ' AON', ' MET', ' GL', ' L', ' BSX', ' BIO', ' EW', ' MDT', ' SYK', ' ABT', ' TMO', ' DHR', ' A', ' IQV', ' MTD', ' PFE', ' JNJ', ' MRK', ' ABBV', ' AMGN', ' GILD',
' BMY', ' LYV', ' EA', ' ATVI', ' UNH', ' G' ,' HUM', ' LOW', ' HD', ' MCD', ' SBUX', ' NKE', ' BKNG', ' TJX', ' ROST', ' SPECIA', ' BLL', ' LODGI', ' XOM', ' CVX', ' PSX', ' MPC', ' OKE', ' EOG', ' AMT', ' EQIX', ' SBAC', ' O', ' SPG',
' PSA', ' CCI', ' D', ' SRE', ' PEG', ' ETR', ' ED', ' EIX', ' XEL', ' DUK', ' NEE', ' SO', ' ES', ' WEC', ' APD', ' DD', ' CE', ' SHW', ' LIN', ' WM', ' RSG', ' SWK', ' BA', ' RTX', ' NOC', ' LMT', ' GD', ' LHX', ' GE', ' MMM', ' HON', ' ITW', 
' EMR', ' ROP', ' PH', ' IR', ' CAT', ' ADP', ' EFX', ' VRSK', ' JCI', ' GIS', ' KHC', ' K', ' SYY', ' STZ', ' MDLZ', ' MO', ' PM', ' KO', ' COP', ' VTR', ' ASML', ' NVS', ' MRVL', ' BIP', ' AMX', ' FMX', ' FN', ' RE', ' BEP', ' EC', 
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
' CVC1.DE', ' HMSB.DE', ' CAR.F', ' TCO.F', ' SRB.DE', ' SY1.DE', ' FME.DE', ' RHKG.DE', ' AFX.DE', ' MOR.DE', ' BNTX', ' ^STOXX50E', ' DDOG', ' AAGH', ' ROKU', ' EH', ' SFIX', ' VLDR', ' TOSYY', ' INVU', ' SNCY', ' AFTPY', ' IQ', ' RVLV', 
' STLFF', ' GOEV', ' QTRX', ' LOGI', ' ZS', ' RCKT', ' UCTT', ' DSP', ' RLAY', ' GSAT', ' SAIA', ' BEAM', ' GCTAY', ' APHA', ' WKEY', ' XL', ' HYLN', ' PTEN', ' DHT', ' FGEN', ' WPG', ' FBASF', ' RMO', ' LTRPB', ' MKTY', ' IKNA', ' ACHL',
' GASS', ' MERC', ' CGEM', ' AMR', ' JT', ' VCTR', ' CTG', ' VIVO', ' EXPR', ' HOLX', ' BWA', ' DHI', ' SBSW', ' EBAY', ' LEN', ' CE', ' TLK', ' SNP', ' TEF', ' EBR-B', ' EBR', ' PPL', ' SHG', ' PKX', ' ORAN', ' VIV', ' REGN', ' FE',
' FMS', ' FRE.DE', ' 11C.F', ' PSHD.L', ' GXI.DE', ' HFG.DE', ' PLUG.DE', ' COIN', ' SEED', ' NOEC', ' COUR', ' AVD', ' IPI', ' EEM', ' MFS=F', ' MME=F', ' EWZ', ' EFA', ' DOCN', ' OLO', ' ACVA', ' IMCR', ' TUYA', ' DSGN', ' IO', ' SEEL', 
' BBQ', ' FIXX', ' GALT', ' MAXN', ' GRAY', ' LHX', ' ODT', ' LW', ' LHDX', ' ISIG', ' BSIG', ' NFH', ' JRO', ' OUST', ' TPCO', ' ALRM', ' CAG', ' BNSO', ' JDCMF', ' YUMC', ' EDU', ' TAL', ' WEED.TO', ' TAB', ' TGOD.TO', ' TGODF', ' YM=F', 
' ES=F', ' NQ=F', ' RTY=F', ' ^FTSE', ' ^CMC200', ' BIDU', ' VIPS', ' WB', ' YY', ' DADA', ' ZH', ' DOYU', ' DAO', ' SOGO', ' BZUN', ' CANG', ' SOHU', ' JFIN', ' LIZI', ' BLCT', ' MTD', ' ILMN', ' USDRUB=X', ' USDJPY=X', ' USDCAD=X',
' JWEL', ' OCG', ' JD', ' KWEB', ' CQQQ', ' KBA', ' MCHI', ' CHIQ', ' 03690', ' QTEC', ' IXN', ' IGV', ' FTEC', ' IYW', ' FDN', ' VGT', ' XLK', ' VOO', ' ESGU', ' O', ' IPO', ' LTC', ' STAG', ' DX', ' MAIN', ' PSEC', ' GLAD', ' GOOD',
' DSL', ' FOF', ' GLD', ' TEAF', ' VCSH', ' YELP', ' TTD', ' ZG', ' MMC', ' RH', ' ADJ.DE', ' PAT.DE', ' TLG.DE', ' TEG.DE', ' DWNI.DE', ' AOX.DE', ' HHFA.DE', ' HABA.DE', ' INS.F', ' IVZ', ' BRPHF', ' FUTU', ' OXY', ' O1E.SG', ' POQ.F', ' B7BA.SG',
' DBK.DE', ' SIGL', ' SAX.DE', ' H50E.L', ' H5E.DE', ' CVCO', ' D2BA.HM', ' XLE', ' SDGR', ' UBER', ' LILA', ' LILAK', ' BXP', ' URG', ' DNN', ' UUUU', ' CCJ', ' NXE', ' UEC', ' KWS.DE', ' SKB.DE', ' CWC.DE', ' STLD', ' NUE', ' TX', ' SQ',
' GPN', ' U', ' CRWD', ' NET', ' CSGP', ' LBRDK', ' VUG', ' SAIC', ' HHC', ' LOV', ' SRG', ' ESTC', ' PFSI', ' GTYH', ' MAXR', ' ADV', ' AHCO', ' SMHI', ' GOCO', ' APO', ' KEYS', ' OSPN', ' ANF', ' VICI', ' KDP', ' CMI', ' NLS',
' SONO', ' ED', ' SPG', ' ATEX', ' FAST', ' IRWD', ' OTIS', ' VTA', ' NSC', ' ATGE', ' FUBO', ' CET', ' CERN', ' HBB', ' W', ' DXC', ' FPH', ' SRGA', ' GTX', ' FCNCA', ' ORI', ' EDP', ' EPD', ' TALO', ' YALA', ' LRCX', ' DEN', ' ALLY', ' LRCX',
' JEF', ' SIBN', ' ATKR', ' TCS', ' MBUU', ' VWS', ' ISRG', ' SJM', ' NVT', ' PGR', ' NTRS', ' OMC', ' AN', ' ATCO', ' GRBK', ' NGA', ' BNGO', ' BFT', ' SPWR', ' MVIS', ' CAPA', ' CLII', ' THCX', ' Z', ' SPRT', ' LAZR', ' UPST', ' RH', ' INTC', ' INX',
' PSAC', ' ENPH', ' LI', ' FSLY', ' SSPK', ' AABB', ' LMND', ' MP', ' SPY', ' DYAI', ' RCKY', ' SLQD', ' PLAY', ' GGTTF', ' KDSS', ' RDFN', ' CCL', ' LTUM', ' TMBR', ' ARCT', ' PLNHF', ' EYES', ' FLT', ' IP', ' FTNT', ' OM', ' SHV', ' XLV', ' THO', ' AGRX',
' HOFV', ' GHVI', ' CPNG', ' 5Q5.F', ' BC8.DE', ' NEM.DE', ' QIA.DE', ' COK.DE', ' SOW.DE', ' CON.DE', ' VOW.DE', ' DB1.DE', ' STOR', ' IRM', ' APTS', ' NLY', ' NRZ', ' AFL', ' TD', ' TROW', ' LQT', ' BNDX', ' IEF', ' IEI', ' SHY', ' EL',
' AEON-USD', ' NPC-USD', ' GBYTE-USD', ' OWC-USD', ' ARRR-USD', ' MCO-USD', ' ATB-USD', ' FLASH-USD', ' DIME-USD', ' SFT-USD', ' EMC2-USD', ' GRC-USD', ' BCA-USD', ' DCY-USD', ' META-USD', ' NYZO-USD', ' MGO-USD', ' ALIAS-USD', ' CET-USD', ' COMP1-USD',
' BDX-USD', ' BRC-USD', ' PART-USD', ' PAI-USD', ' NMC-USD', ' XAS-USD', ' CURE-USD', ' CUT-USD', ' BCH-USD', ' FRST-USD', ' DDK-USD', ' HNC-USD', ' FSN-USD', ' DFI-USD', ' KDA-USD', ' LOKI-USD', ' PLC-USD', ' GAS-USD', ' DTEP-USD', ' OTO-USD',
' RINGX-USD', ' PI-USD', ' NULS-USD', ' ZVC-USD', ' CCA-USD', ' DERO-USD', ' PLC-USD', ' XMC-USD', ' MINT-USD', ' NVCR', ' DFIFF', ' MSTR', ' ANGI', ' NVAX', ' CSPCY', ' LTCN', ' FLGT', ' LKNCY', ' HMBL', ' KHOTF', ' SSL', ' OSTK', ' TWST', ' EM', ' SUMO',
' MRRTY', ' AJMPF', ' TTM', ' CDE', ' IRTC', ' OMAB', ' NSTG', ' ALBKF', ' SPT', ' PLAN', ' DOCU', ' USNZY', ' TEAM', ' HL', ' VNOM', ' ACH', ' AGI', ' SKM', ' ACOPF', ' MYTE', ' WISH', ' TKAYY', ' OLK', ' RARE', ' TRUMY', ' UPWK', ' GGB', ' ATDRY', ' SSTK',
' TXG', ' SYIEY', ' PPRUY', ' KC', ' CRSP', ' TMVWY', ' WIX', ' VIR', ' NPSNY', ' SBRCY', ' NG', ' HOKCF', ' AUOTY', ' ORGO', ' XISHY', ' CDLX', ' SANA', ' PPERF', ' TIL', ' ADS', ' ARVL', ' YNDX', ' AEIS', ' RDY', ' CROX', ' EBS', ' SAGE', ' LGORF',  
' WHD', ' VCEL', ' UAA', ' OI', ' SYF', ' BKE', ' GDRX', ' JWN', ' MATX', ' CADE', ' JW-A', ' WRK', ' THRM', ' MPNGY', ' CLVLY', ' CMSQY', ' VTVT', ' MFNC', ' DMRC', ' MFCN', ' CBLI', ' MUDS', ' OBAS', ' AGC', ' BTX', ' ATXI', ' LHDX', ' GBOX',
' UK', ' PLBY', ' GFED', ' CGA', ' AGCUU', ' AEE', ' MSB', ' CSSE', ' WCN', ' TIRX', ' OGI', ' NLSP', ' SNDL', ' CTRM', ' CNET', ' KRUS', ' SCR', ' RVPH', ' AMOM', ' CLIQ.DE', ' WEW.DE', ' WCH.DE', ' JUN3.DE', ' GLJ.DE', ' CL', ' FDX', ' WBA', ' ALXN',
' BYND', ' 0Q3.DE', ' IRBT', ' AXON', ' COPN.SW', ' ILM1.DE', ' CVAC', ' PANA', ' DKNG', ' DDD', ' SPFR', ' PCAR', ' EXAS', ' PHR', ' PSTI', ' MASS', ' BLI', ' IRDM', ' AVAV', ' RTP', ' ZEN', ' IDXX', ' TSP', ' FATE', ' CXW', ' LFC', ' ALGN',
' LEA', ' WAB', ' EQH', ' NWL', ' PVH', ' GIL', ' HAL', ' NRG', ' CTSH', ' LYB', ' ECL', ' TXT', ' HPE', ' BKR', ' MHK', ' DOW', ' AXS', ' MCK', ' VOYA', ' DOX', ' ALNY', ' UBS', ' SKX', ' CAH', ' CVE', ' VTRS',
' SNY', ' CI', ' HPE', ' TEL', ' INCY', ' WMB', ' RHHBY', ' SLB', ' DISH', ' FOXA', ' BMRN', ' FOX', ' LNC', ' AEG', ' HAL', ' DCI', ' GPS', ' ON', ' ET', ' LUV', ' SONY', ' ELAN', ' PRLB', ' ZBH', ' NVEC', ' PXD', ' ERES', ' BOKF', ' GLW', ' ROK', ' JAMF', 
' LNT', ' DGII', ' WK', ' OMF', ' SPR', ' LSXMA', ' LFUS', ' HRL', ' FUL', ' COR', ' DCI', ' PFG', ' CHRW', ' VLKAF', ' UNM', ' TOL', ' MARUF', ' GT', ' BIIB', ' SBNY', ' ETN', ' ULTA', ' HI', ' MAR', ' ABCL', ' FTV', ' AIZ', ' NUAN', ' KRTX', ' ARNA', ' KLDIW',
' XEC', ' ALBO', ' CEIX', ' ZTS', ' TREE', ' AHS', ' EXPO', ' SLP', ' ACWI', ' CLB', ' RMD', ' ALLE', ' PENN', ' AEGN', ' REZI', ' ZBH', ' APA', ' HNGR', ' FAF', ' KKR', ' TISI', ' IT', ' BL', ' DT', ' HEI', ' SEER', ' ACA', ' NOMD', ' MMSI', ' GPC', ' CC', 
' SNA', ' MOS', ' NLSN', ' LAZ', ' LH', ' MSGE', ' WU', ' AQUA', ' CHNG', ' ZUO', ' PCPH', ' TECK', ' DXCM', ' ECV.F', ' OCGN', ' MWW', ' ITOS', ' TDOC', ' PATH', ' PHX', ' RPHM', ' EPSM', ' WORK', ' BWEN', ' BLFS', ' STON', ' CUK',
' AMRS', ' PAYC', ' PCRX', ' GH', ' ZI', ' OSH', ' MEDP', ' NCNO', ' IART', ' MTEM', ' PPG', ' WEX', ' TTCF', ' CUK', ' GMS', ' SPAC', ' QUBT', ' 7CD.F', ' 3CP.F', ' 11C.F', ' VAR1.DE', ' NNND.F', ' D7G.F', ' AHLA.DE', ' XSDG.F', ' HYMTF', ' 005930.KS', ' SSUN.F',
' MTX.DE', ' NDA.DE', ' AIR.DE', ' S92.DE', ' MMQ', ' 5CV.DE', ' VBK.DE', ' EVD.DE', ' GFT.DE', ' DEQ.DE', ' MEI', ' EMAN', ' ZION', ' ORCC', ' SNMP', ' CRM', ' CLI', ' NPCE', ' VSEC', ' SFBS', ' HMN', ' MTZ', ' NJR', ' AX', ' PBLA', ' AE', ' AFT', ' AGM',
' ALG', ' BBSI', ' EBIX', ' IGI', ' IGIC', ' SMP', ' VRS', ' VKI', ' TACT', ' ARDC', ' BLX', ' GTN', ' HNNA', ' FRO', ' AMPY', ' NSRGY', ' SUZ', ' NTCO', ' TIMB', ' AZRE', ' YTRA', ' SIFY', ' IBN', ' WIT', ' WNS', ' INFY', ' VEDL', ' PAGS', ' IX',
' NMR', ' LN', ' AU', ' HMY', ' DRD', ' UEPS', ' SMFG', ' CAJ', ' JMIA', ' IMTX', ' AFMD', ' CNTG', ' CLLS', ' CNHI', ' CPRI', ' CSTM', ' TLND', ' TRVG', ' VIAO', ' ERYP', ' LBTYA', ' JHG', ' IVA', ' EDAP', ' SQNS', ' IFRX', ' GNFT', ' WPP',
' ABCM', ' ALDX', ' VXRT', ' TBI', ' BHSEU', ' DBVT', ' IHG', ' DAVA', ' MYT', ' RIBT', ' FCBP', ' NTWK', ' IPHA', ' LBTYK', ' FTI', ' YFI-EUR', ' LIQT', ' AAN', ' BFRA', ' INFO', ' PNR', ' AY', ' RELX', ' BCS', ' LYG', ' FCAU', ' SNN', ' PSO', ' LIVN',
' PTR', ' XPEV', ' LU', ' HTHT', ' GDS', ' BGNE', ' ZTO', ' MNSO', ' ZNH', ' GSX', ' CEA', ' YSG', ' HNP', ' OCFT', ' SID', ' SBS', ' BRFS', ' CZZ', ' VSTA', ' LINX', ' UGP', ' BAK', ' CBD', ' ARCE', ' ERJ', ' LND', ' CIG', ' ELP', ' AZUL',
' AFYA', ' GOL', ' VTRU', ' GLOB', ' TIGO', ' NEXA', ' AGRO', ' WF', ' KEP', ' CAAP', ' MX', ' ASPS', ' ATTO', ' KB', ' KT', ' IPOE', ' PE', ' CRSR', ' R', ' CLF', ' SF', ' TDOC', ' E', ' B', ' DM', ' TV', ' HUYA', ' PUMP', ' EBET', ' TDUP', ' COMP', ' HNST', 
' ANAT', ' CNXC', ' GGG', ' SCHL', ' OMI', ' DAR', ' DECK', ' MOSI', ' III', ' ZYME', ' SXC', ' TBT', ' VACQ', ' HP', ' PDS', ' ARPO', ' MRNS', ' MDP', ' GNK', ' GOGL', ' STNG', ' LLIT', ' MOSY', ' GRBK', ' POOL', ' MSM', ' CABO', ' XM', ' VAPO', ' IFF', ' RADI', ' QUAD',
' NXRT', ' GPRO', ' UNVR', ' BE', ' VTNR', ' GOED', ' RSI', ' MAX', ' BXC', ' CRC', ' FELE', ' LB', ' GAN', ' MPWR', ' CNMD', ' PGNY', ' OTRK', ' ALLK', ' RM', ' ROLL', ' VITL', ' FDP', ' HCAT', ' APLT', ' CONN', ' LSCC', ' CHEF', ' WDL.DE', ' BLDP', ' ZIP', ' FLUX',
' IVR', ' CLNE', ' WKHS', ' WEN', ' MAN', ' FLY', ' RC', ' X', ' HHO', ' JWF',' KWQ', ' IIQ', ' ORA', ' ILD.PA', ' UHR',' TKWI', ' ABI', ' TSCO', ' TTE', ' FTI',' SLB', ' INGA', ' LSEG', ' ADVU', ' CFX', ' SHIB-USD',
' AXS-USD', ' MATIC-USD', ' HEX-USD', ' META-USD', ' ICP1-EUR', ' AVAX-USD', ' MANA-EUR', ' HBAR-USD', ' FTT1-EUR', ' BTT1-EUR',' HOT1-EUR', ' COMP-EUR')


col1, col2 = st.columns(2)

with col1:

    selected_stock = st.selectbox('Select Stock Ticker', stock_name)
    



with col2:

        option = st.selectbox(
            'Choose starting point',
            ('2000-01-01', '2005-01-01', '2010-01-01', '2015-01-01', '2018-01-01', '2020-01-01', '2021-01-01', '2022-01-01', '2022-02-02'))


START = option
TODAY = date.today().strftime("%Y-%m-%d")



month = st.slider(' Predict XY months into the future:', 1,12 )
period = month*30 

@st.cache
def load_data(ticker):
    data = yf.download(ticker, START, TODAY)
    data.reset_index(inplace=True)
    return data




data_load_state = st.text('Please wait...')
data = load_data(selected_stock)
data_load_state.text('Loading data done!')

st.write(data.tail())



def plot_raw_data():
	fig = go.Figure()
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Open'], name="stock_open"))
	fig.add_trace(go.Scatter(x=data['Date'], y=data['Close'], name="stock_close"))
	fig.layout.update(title_text='Time Chart', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig)
	
plot_raw_data()


def plot_raw_data2():
	fig2 = go.Figure()
	fig2.add_trace(go.Scatter(x=data['Date'], y=data['Volume'], name="stock_volume"))
	
	fig2.layout.update(title_text='Volume', xaxis_rangeslider_visible=True)
	st.plotly_chart(fig2)
	
plot_raw_data2()


col1, col2, col3 = st.columns(3)

with col2:

    button = st.button('Predict My Stocks')

if button == True:

    data_load_state = st.image('https://media.giphy.com/media/gu9XBXiz60HlO5p9Nz/giphy.gif')
    # Predict forecast with Prophet.
    df_train = data[['Date','Close']]
    df_train = df_train.rename(columns={"Date": "ds", "Close": "y"})

    m = Prophet(seasonality_mode='multiplicative',
    daily_seasonality = True,
    weekly_seasonality= True,
    yearly_seasonality = True)
    m.fit(df_train)
    future = m.make_future_dataframe(periods=period)
    forecast = m.predict(future)


    # Show and plot forecast
    st.subheader('Forecast data')
    st.write(forecast.tail())
    #st.subheader("Predicted Stock price ")
   # st.write(forecast[['ds','yhat']].tail(1))

    st.subheader('Forecast for Months')
    fig1 = plot_plotly(m, forecast)
    st.plotly_chart(fig1)

    st.write("Forecast components")
    fig2 = m.plot_components(forecast)
    st.write(fig2)

    data_load_state.text('Predicting data done ✔️')



st.markdown("<h2 style='text-align: center; color: white;'>   </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>  </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>   </h2>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align: center; color: white;'>  </h2>", unsafe_allow_html=True)

link = '[Activity of super investors and insiders](https://www.dataroma.com/m/home.php)'
st.markdown(link, unsafe_allow_html=True)

link = '[Finviz, great for filtering stocks](https://finviz.com/screener.ashx)'
st.markdown(link, unsafe_allow_html=True)

link = '[Another insider buy and sales site](http://openinsider.com/)'
st.markdown(link, unsafe_allow_html=True)

link = '[Github Repo](https://github.com/facebook/prophet)'
st.markdown(link, unsafe_allow_html=True)

link = '[My Instagram self-study page](https://www.instagram.com/max_mnemo/)'
st.markdown(link, unsafe_allow_html=True)

link = '[Buy me a coffee](https://www.buymeacoffee.com/MaxMnemo)'
st.markdown(link, unsafe_allow_html=True)

