from calendar import c
from flask import Blueprint , render_template , request , flash ,redirect
import pandas as pd
from binance.client import Client
import ta
import pandas_ta as pda
import json
import plotly
from statistics import mean
import plotly.express as px
import datetime;
from dateutil import relativedelta


market = Blueprint('market',__name__)




@market.route('/',methods=['GET', 'POST'])
def home():
    if request.method == 'POST':
        coin = str(request.form.get("inputcoin"))+"USDT"
        timeframe= request.form.get("timeframe")
        period = int(request.form.get("period"))
        startime= timecalculator(period)
        df = getcleandf(coin,timeframe,startime)
        dt=  getcleandf(coin,"1d",startime)
        bite = plot_level(df=dt)
        boulot = "60"
        if(timeframe == "1d"):
            boulot="D"
        elif (timeframe =="1w"):
            boulot="W"
        print(timeframe)
        return render_template("analyse.html",coin=coin,graph_supertrend=superTrend(df,timeframe),graph_aligator =aligator_graph(df,timeframe),graph_williams =WillR_graph(df,timeframe),graph_rsi=stock_rsi_graph(df,timeframe),timeframe=boulot,graph_price=price_Graph(df,bite),awesome =round(df.iloc[-1]['AO'],2),wililiam =round(df.iloc[-1]['WillR'],2),stock_rsi =round(df.iloc[-1]['STOCH_RSI'],2))
    return render_template("home.html")


def timecalculator(period):
    n = datetime.datetime.now()
    bg = n - relativedelta.relativedelta(months=period)
    res =bg.strftime("%d %B %Y")
    return res

def getcleandf(coin,timeframe,startime):
    client = Client()
    klinesT = client.get_historical_klines(coin,timeframe,startime)
    client.close_connection()
    df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['open'] = pd.to_numeric(df['open'])
    df['volume'] = pd.to_numeric(df['volume'])
    
    del df['ignore']
    del df['close_time']
    del df['quote_av']
    del df['trades']
    del df['tb_base_av']
    del df['tb_quote_av']

    df = df.set_index(df['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')
    del df['timestamp']
    df = addrumble(df)
    return df

def addrumble(df):
    #AWESOME OSCI -------------MOMENTUM 
    df['AO']= ta.momentum.awesome_oscillator(df['high'],df['low'],window1=6,window2=22)
    #Williams-R
    df['WillR'] = ta.momentum.williams_r(high=df['high'], low=df['low'], close=df['close'], lbp=14)
    #Stock_rsi
    df['STOCH_RSI'] = ta.momentum.stochrsi(df['close'], window=14 , smooth1=3, smooth2=3)

    #
    #crocodile -----------TREND ----------------
    df['21Jours']= ta.trend.ema_indicator(close=df['close'], window=21)
    df['8Jours']= ta.trend.ema_indicator(close=df['close'], window=8)
    df['3Jours']= ta.trend.ema_indicator(close=df['close'], window=3)
    #SIMPLE EMA
    df['SIMPLE_EMA']=ta.trend.ema_indicator(df['close'], 100)
    #SuperTrend
    ST_length = 20
    ST_multiplier = 3.0
    superTrend = pda.supertrend(df['high'], df['low'], df['close'], length=ST_length, multiplier=ST_multiplier)
    df['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)]
    df['SUPER_TREND_DIRECTION1'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)]
    ST_length = 20
    ST_multiplier = 4.0
    superTrend = pda.supertrend(df['high'], df['low'], df['close'], length=ST_length, multiplier=ST_multiplier)
    df['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)]
    df['SUPER_TREND_DIRECTION2'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)]
    ST_length = 40
    ST_multiplier = 8.0
    superTrend = pda.supertrend(df['high'], df['low'], df['close'], length=ST_length, multiplier=ST_multiplier)
    df['SUPER_TREND'] = superTrend['SUPERT_'+str(ST_length)+"_"+str(ST_multiplier)]
    df['SUPER_TREND_DIRECTION3'] = superTrend['SUPERTd_'+str(ST_length)+"_"+str(ST_multiplier)]
    df['final']= df['SUPER_TREND_DIRECTION1'] + df['SUPER_TREND_DIRECTION2']  + df['SUPER_TREND_DIRECTION3']


    df['EMAX']=ta.trend.ema_indicator(df['close'], 28)
    df['EMAY']=ta.trend.ema_indicator(df['close'], 48)

    #VOLUME
    df['MFI']=ta.volume.money_flow_index(df['high'],df['low'],df['close'],df['volume'],window=14)
    df['eom']=ta.volume.ease_of_movement(df['high'],df['low'],df['volume'],window=14)
    df['eomema']=ta.volume.sma_ease_of_movement(df['high'],df['low'],df['volume'],window=14)
    df['previouscloseobv']=df['close'].shift(1)
    df['previousvolumeobv']=df['volume'].shift(1)
    df['ppreviouscloseobv']=df['close'].shift(2)
    df['ppreviousvolumeobv']=df['volume'].shift(2)
    df['ppobv'] = ta.volume.on_balance_volume(df['ppreviouscloseobv'],df['ppreviousvolumeobv'])
    df['pobv'] = ta.volume.on_balance_volume(df['previouscloseobv'],df['previousvolumeobv'])
    df['obv'] = ta.volume.on_balance_volume(df['close'],df['volume'])
    del df['previouscloseobv']
    del df['previousvolumeobv']
    del df['ppreviouscloseobv']
    del df['ppreviousvolumeobv']
    return df


def price_Graph(df,bite):
    fig = px.line(df['close'],title='Le prix et les resistances')
    for i in bite:
        fig.add_hline(y=i[0] ,line_width=i[1], line_color="blue")
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def stock_rsi_graph(df,chiant):
    taille =200
    if(chiant == "1d" ):
        taille = 50
    elif(chiant == "1w" ):
        taille = 15
    fata = px.line(df.tail(taille)[['STOCH_RSI']], title="Stock RSI des derniers quelques jours" )
    fata.add_hrect(y0=0.8, y1=0.2, line_width=0, fillcolor="green", opacity=0.2)
    fata.add_hrect(y0=0.8, y1=1, line_width=0, fillcolor="red", opacity=0.2)
    fata.add_hrect(y0=0.2, y1=0, line_width=0, fillcolor="red", opacity=0.2)
    graphJSON = json.dumps(fata, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON
def WillR_graph(df,chiant):
    taille =200
    if(chiant == "1d" ):
        taille = 50
    elif(chiant == "1w" ):
        taille = 15
    fata = px.line(df.tail(taille)[['WillR']], title="Williams R des derniers quelques jours" )
    fata.add_hrect(y0=-85, y1=-15, line_width=0, fillcolor="green", opacity=0.2)
    fata.add_hrect(y0=-85, y1=-100, line_width=0, fillcolor="red", opacity=0.2)
    fata.add_hrect(y0=-15, y1=0, line_width=0, fillcolor="red", opacity=0.2)
    graphJSON = json.dumps(fata, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def aligator_graph(df,chiant):
    taille =100
    if(chiant == "1d" ):
        taille = 30
    elif(chiant == "1w" ):
        taille = 15
    fata = px.line(df.tail(taille)[['21Jours','8Jours','3Jours']], title="Aligator des derniers quelques jours")
    graphJSON = json.dumps(fata, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

def superTrend(df,chiant):
    taille =200
    if(chiant == "1d" ):
        taille = 50
    elif(chiant == "1w" ):
        taille = 30
    fata = px.line(df.tail(taille)[['final']], title="3Super_trend des derniers quelques jours")
    fata.add_hrect(y0=1, y1=3, line_width=0, fillcolor="green", opacity=0.2)
    fata.add_hrect(y0=1, y1=-3, line_width=0, fillcolor="red", opacity=0.2)
    graphJSON = json.dumps(fata, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


#Crypto robot : https://github.com/CryptoRobotFr/General-code-trading-bot/blob/main/Support_Resistance.ipynb


def get_n_columns(df, columns, n=1):
    dt = df.copy()
    for col in columns:
        dt["n"+str(n)+"_"+col] = dt[col].shift(n)
    return dt

def get_top_and_bottom(df, candle_min_window=3):
    originals_columns = list(df.columns.copy())
    originals_columns.append("top")
    originals_columns.append("bottom")
    dt = df.copy()
    dt["bottom"] = 1
    dt["top"] = 1

    for i in range(1, candle_min_window + 1, 1):
        dt = get_n_columns(dt, ['close'], i)
        dt = get_n_columns(dt, ['close'], -i)

        dt.loc[
            (dt["n" + str(-i) + "_close"] < dt["close"]) 
            | (dt["n" + str(i) + "_close"] < dt["close"])
            , "bottom"
        ] = 0

        dt.loc[
            (dt["n" + str(-i) + "_close"] > dt["close"]) 
            | (dt["n" + str(i) + "_close"] > dt["close"])
            , "top"
        ] = 0
    # print(dt)
    dt = dt.loc[:,originals_columns]

    return dt

def group_level(df, group_multiplier = 1):
    df_test = df.copy()
    d = list(df_test.loc[df_test["bottom"]==1, "close"])
    d.extend(list(df_test.loc[df_test["top"]==1, "close"]))

    d.sort()

    diff = [y - x for x, y in zip(*[iter(d)] * 2)]
    avg = sum(diff) / len(diff)

    important_levels = [[d[0]]]

    for x in d[1:]:
        if x - important_levels[-1][0] < group_multiplier * avg:
            important_levels[-1].append(x)
        else:
            important_levels.append([x])

    return important_levels

def plot_level(df,top_bottom_window = 5, group_multiplier = 3, min_group_number = 2):
    df = get_top_and_bottom(df, top_bottom_window)
    levels = group_level(df, group_multiplier)
    
    tv_paste_text = []

    df["iloc_val"] = list(range(0,len(df),1))
    if levels:
        for i in range(len(levels)):
            if len(levels[i]) >= min_group_number:
                tv_paste_text.append([mean(levels[i]),len(levels[i]) - (min_group_number - 1)])
    return tv_paste_text