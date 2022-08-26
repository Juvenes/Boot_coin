from importlib.resources import path
from flask import Blueprint , render_template , request , flash, url_for, redirect
from . import db
from .models import Wallet,Transaction,Explication
import json
import requests
import os


backtest_menu = Blueprint('backtest_menu',__name__)

@backtest_menu.route('/backtest_menu',methods=['GET', 'POST'])
def portefeuille():
    if request.method == 'POST':
        coin = request.form.get('inputcoin') if request.form.get('inputcoin') !=None else "BTC"
        strat = request.form.get('inputStat') if request.form.get('inputStat') !=None else "crocodile"
        optimiser = True if request.form.get('optimise') =="on" else False
        prix = int(request.form.get('prix')) if request.form.get('prix') !=None and request.form.get('prix')!=''  else 1000
        timing = request.form.get('timing') if request.form.get('timing') !=None else "All"
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
                print(timing2)
            timing1 = ""+str(d1)+" "+str(m1)+" "+str(y1)
            print(timing1)
        
        return render_template("backtest_menu.html")
    else:
        return render_template("backtest_menu.html")

