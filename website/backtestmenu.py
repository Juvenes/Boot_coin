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
    return render_template("backtest_menu.html")