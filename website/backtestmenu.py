from importlib.resources import path
from sys import maxunicode
from flask import Blueprint , render_template , request , flash, url_for, redirect
from . import db
from .models import Wallet,Transaction,Explication
import json
import requests
import os
import pandas as pd
from binance.client import Client
import ta
import pandas_ta as pda
import matplotlib.pyplot as plt
import numpy as np
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import plotly



backtest_menu = Blueprint('backtest_menu',__name__)

@backtest_menu.route('/backtest_menu',methods=['GET', 'POST'])
def portefeuille():
    if request.method == 'POST':
        coin = request.form.get('inputcoin') if request.form.get('inputcoin') !=None else "BTC"
        coin = coin+"USDT"
        strat = request.form.get('inputStat') if request.form.get('inputStat') !=None else "crocodile"
        optimiser = True if request.form.get('optimise') =="on" else False
        prix = int(request.form.get('prix')) if request.form.get('prix') !=None and request.form.get('prix')!=''  else 1000
        timing = request.form.get('timing') if request.form.get('timing') !=None else "All"
        timing1=None
        timing2=None
        if timing == "choice":
            d1 = int(request.form.get('dayIn')) if request.form.get('dayIn') !=None and request.form.get('dayIn')!=''  else 1
            m1 = request.form.get('monthIn') if request.form.get('monthIn') !=None and request.form.get('monthIn')!=''  else "january"
            y1 = int(request.form.get('yearIn')) if request.form.get('yearIn') !=None and request.form.get('yearIn')!=''  else 2021
            tonow  = True if request.form.get('autoSizingCheck') =="on" else False
            print(tonow)
            if tonow == False:
                d2 = int(request.form.get('dayout')) if request.form.get('dayout') !=None and request.form.get('dayout')!=''  else 1
                m2 = request.form.get('monthout') if request.form.get('monthout') !=None and request.form.get('monthout')!=''  else "february"
                y2 = int(request.form.get('yearout')) if request.form.get('yearout') !=None and request.form.get('yearout')!=''  else 2022
                timing2 = ""+str(d2)+" "+str(m2)+" "+str(y2)
            timing1 = ""+str(d1)+" "+str(m1)+" "+str(y1)
        supertrend_trades(download_data(timing,timing1,timing2,coin))
        
        return render_template("backtest_menu.html")
    else:
        return render_template("backtest_menu.html")


 








def download_data(cat,start_date,end_date,coin):
    print(cat)
    print(start_date)
    print(end_date)
    print(coin)
    client = Client()
    if cat =="bullrun":
        klinesT = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, "12 july 2021","8 november 2021")
    elif cat == "crash" :
        klinesT = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, "8 november 2021","20 juin 2022")
    elif cat == "normal" :
        klinesT = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, "12 july 2021","24 january 2022")
    else:
        klinesT = client.get_historical_klines(coin, Client.KLINE_INTERVAL_1HOUR, start_date , end_date)

    df = pd.DataFrame(klinesT, columns = ['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_av', 'trades', 'tb_base_av', 'tb_quote_av', 'ignore' ])
    df['close'] = pd.to_numeric(df['close'])
    df['high'] = pd.to_numeric(df['high'])
    df['low'] = pd.to_numeric(df['low'])
    df['open'] = pd.to_numeric(df['open'])

    df = df.set_index(df['timestamp'])
    df.index = pd.to_datetime(df.index, unit='ms')
    del df['timestamp']
    return df.copy()

def crocodile_trades(df,window1=7,window2=30,window3=50,window4=100,window5=121,window6=200,rsi_window=14,fiat=1000):
    df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)
    df['EMA1']=ta.trend.ema_indicator(close=df['close'], window=window1)
    df['EMA2']=ta.trend.ema_indicator(close=df['close'], window=window2)
    df['EMA3']=ta.trend.ema_indicator(close=df['close'], window=window3)
    df['EMA4']=ta.trend.ema_indicator(close=df['close'], window=window4)
    df['EMA5']=ta.trend.ema_indicator(close=df['close'], window=window5)
    df['EMA6']=ta.trend.ema_indicator(close=df['close'], window=window6)
    df['STOCH_RSI'] = ta.momentum.stochrsi(close=df['close'], window=rsi_window, smooth1=3, smooth2=3)
    dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])
    usdt = fiat
    coin = 0
    wallet = fiat
    lastAth = 0
    takerFee = 0.0007
    buyReady = True
    sellReady = True

    def buyCondition(row):
        if row['EMA1'] > row['EMA2'] and row['EMA2'] > row['EMA3'] and row['EMA3'] > row['EMA4'] and row['EMA4'] > row['EMA5'] and row['EMA5'] > row['EMA6'] and row['STOCH_RSI']<0.82:
            return True
        else:
            return False
    def sellCondition(row):
        if row['EMA6'] > row['EMA1'] and row['STOCH_RSI']>0.2:
            return True
        else:
            return False
    for index, row in df.iterrows():
      #Buy market order
        if buyCondition(row) == True and usdt > 0 and buyReady == True:
            buyPrice = row['close']

            #Define the price of you SL and TP or comment it if you don't want a SL or TP
            # stopLoss = buyPrice - 2 * row['ATR']
            # takeProfit = buyPrice + 4 * row['ATR']

            coin = usdt / buyPrice
            fee = takerFee * coin
            coin = coin - fee
            usdt = 0
            wallet = coin * row['close']
            # print("Buy COIN at",buyPrice,'$ the', index)
            myrow = {'date': index,'position': "Buy", 'reason': 'Buy Market','price': buyPrice,'frais': fee*row['close'],'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/lastAth}
            dt = dt.append(myrow,ignore_index=True)
        elif sellCondition(row) == True:
            buyReady = True
            if coin > 0 and sellReady == True:
                sellPrice = row['close']
                usdt = coin * sellPrice
                frais = takerFee * usdt
                usdt = usdt - frais
                coin = 0
                wallet = usdt
                if wallet > lastAth:
                    lastAth = wallet
                # print("Sell COIN at",sellPrice,'$ the', index)
                myrow = {'date': index,'position': "Sell", 'reason': 'Sell Market', 'price': sellPrice, 'frais': frais, 'fiat': usdt, 'coins': coin, 'wallet': wallet, 'drawBack':(wallet-lastAth)/lastAth}
                dt = dt.append(myrow,ignore_index=True)
    return dt


def supertrend_trades(df,fiat=1000):
    df.drop(df.columns.difference(['open','high','low','close','volume']), 1, inplace=True)
    df['EMA90']=ta.trend.ema_indicator(df['close'], 90)
    df['STOCH_RSI']=ta.momentum.stochrsi(df['close'])
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
    dt = pd.DataFrame(columns = ['date','position', 'reason', 'price', 'frais' ,'fiat', 'coins', 'wallet', 'drawBack'])
    usdt = fiat
    initalWallet = usdt
    coin = 0
    wallet = fiat
    lastAth = 0
    takerFee = 0.0007
    buyReady = True
    sellReady = True
    for index, row in df.iterrows():
            #Buy
        # if row['SUPER_TREND_DIRECTION'] == 1 and row['STOCH_RSI'] < 0.8 and row['close']>row['EMA50'] and usdt > 0:
        if row['SUPER_TREND_DIRECTION1']+row['SUPER_TREND_DIRECTION2']+row['SUPER_TREND_DIRECTION3'] >= 1 and row['STOCH_RSI'] < 0.8 and row['close']>row['EMA90'] and usdt > 0 and goOn == True:
            buyPrice = row['close']
            # stopLoss = buyPrice - 0.02 * buyPrice
            coin = usdt / buyPrice
            frais = takerFee * coin
            coin = coin - frais
            usdt = 0
            wallet = coin * row['close']
            # print("Buy COIN at",buyPrice,'$ the', index)
            myrow = {'date': index,'position': "Buy",'price': buyPrice,'frais': frais * row['close'],'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/lastAth}
            dt = dt.append(myrow,ignore_index=True)
        
        #Stop Loss
        # elif row['low'] < stopLoss and coin > 0:
        #   sellPrice = stopLoss
        #   usdt = coin * sellPrice
        #   frais = 0.005 * usdt
        #   usdt = usdt - frais
        #   coin = 0
        #   goOn = False
        #   wallet = usdt
        #   if wallet > lastAth:
        #     lastAth = wallet
        #   # print("Sell COIN at Stop Loss",sellPrice,'$ the', index)
        #   myrow = {'date': index,'position': "Sell",'price': sellPrice,'frais': frais,'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/lastAth}
        #   dt = dt.append(myrow,ignore_index=True)    

        # Sell
        elif row['SUPER_TREND_DIRECTION1']+row['SUPER_TREND_DIRECTION2']+row['SUPER_TREND_DIRECTION3'] < 1 and row['STOCH_RSI'] > 0.2:
            goOn = True
            if coin > 0:
                sellPrice = row['close']
                usdt = coin * sellPrice
                frais = takerFee * usdt
                usdt = usdt - frais
                coin = 0
                wallet = usdt
                # print("Sell COIN at",sellPrice,'$ the', index)
                myrow = {'date': index,'position': "Sell",'price': sellPrice,'frais': frais,'fiat': usdt,'coins': coin,'wallet': wallet,'drawBack':(wallet-lastAth)/lastAth}
                dt = dt.append(myrow,ignore_index=True)
    

def mfi_graph(df):
    taille = 50
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(go.Scatter(x=list(df.tail(taille).index),y=list(df.tail(taille).close),name="prix"), secondary_y=False)
    fig.add_trace(go.Scatter(x=list(df.tail(taille).index),y=list(df.tail(taille).MFI),name="MFI"), secondary_y=True)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON