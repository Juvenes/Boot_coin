from importlib.resources import path
from flask import Blueprint , render_template , request , flash, url_for, redirect
from . import db
from .models import Wallet,Transaction,Explication
import json
import requests
import os


wallet = Blueprint('wallet',__name__)

@wallet.route('/portefeuille',methods=['GET', 'POST'])
def portefeuille():
    if request.method == 'POST':
        if(request.form.get("id")!=None):
            id = request.form.get('id')
            return redirect(url_for('wallet.wallet_display', id=id))
        else:
            print(request.form)
            autor= request.form.get("auteur")
            if(autor==""):
                flash(f"Ajoutez un nom d'auteur.", category="error")
            desc= request.form.get("desc")
            if(desc==""):
                flash(f"Ajouter une description", category="error")
            mdp= request.form.get("mdp")
            coiname= request.form.get("inputcoin")
            new_wallet =None
            if(mdp==""):
                new_wallet = Wallet(isPrivate=False,mdp="",startmoney=0,name=autor,descript=desc,money=0,coin=0,coinname=coiname)
            else:
                new_wallet = Wallet(isPrivate=True,mdp=mdp,startmoney=0,name=autor,descript=desc,money=0,coin=0,coinname=coiname)
            db.session.add(new_wallet)
            db.session.commit()
            flash('Portefeuille ajouté !', category='success')
    wallets =Wallet.query.all()
    return render_template("wallet.html",wallets=wallets)

@wallet.route('/delete-note', methods=['POST'])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Wallet.query.get(noteId)
    if note:
        db.session.delete(note)
        db.session.commit()
    return 'a string'

@wallet.route('/wallet_display', methods=['POST','GET'])
def wallet_display():
    if request.method == 'GET':
        id = int(request.args.get('id', None))
        wallet =Wallet.query.get(id)
        return render_template("wallet_display.html",wallet=wallet)
    if request.method == 'POST':
        if(request.form.get("type")!=None):
            id = int(request.form.get('id'))
            wallet =Wallet.query.get(id)
            type =request.form.get("type")
            if(type=="addliquid"):
                addmoney = float(request.form.get('addmoney'))
                wallet.money= wallet.money +addmoney
                wallet.startmoney= wallet.startmoney +addmoney
                db.session.commit()
            if(type=="tocoin"):
                if(wallet.money ==0.0):
                    flash(f"Tu n'as pas de liquidité", category="error")
                else:
                    response= requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+wallet.coinname+'USDT')
                    data = response.json()
                    close= float(data['price'])
                    transaction = Transaction(walletid=wallet.id,type="ACHAT",close=close,wallet=wallet.money,reanalyse="Non-RA")
                    wallet.coin = round(wallet.money / close,6)
                    wallet.money =0.0
                    db.session.add(transaction)
                    db.session.commit()
            if(type=="tomoney"):
                if(wallet.coin ==0.0):
                    flash(f"Tu n'as pas de Coins", category="error")
                else:
                    response= requests.get('https://api.binance.com/api/v3/ticker/price?symbol='+wallet.coinname+'USDT')
                    data = response.json()
                    close= float(data['price'])
                    wallet.money = round(wallet.coin * close,6)
                    transaction = Transaction(walletid=wallet.id, type="VENTE",close=close,wallet=wallet.money,reanalyse="Non-RA")
                    wallet.coin =0.0
                    db.session.add(transaction)
                    db.session.commit()
            if(type=="goex"):
                id = int(request.form.get('tid'))
                return redirect(url_for('wallet.explication', id=id))
        return render_template("wallet_display.html",wallet=wallet)

@wallet.route('/explication', methods=['POST','GET'])
def explication():
    if request.method == 'GET':
        id = int(request.args.get('id', None))
        transaction =Transaction.query.get(id)
        return render_template("explication.html",transaction=transaction)
    if request.method == 'POST':
        if(request.form.get("type")!=None):
            id = int(request.form.get('id'))
            transaction =Transaction.query.get(id)
            type =request.form.get("type")
            if(type=='retour'):
                return redirect(url_for('wallet.wallet_display', id=transaction.walletid))
            if(type=="addExplication"):
                id =int(request.form.get('id'))
                des =request.form.get('explication')
                explication =Explication(transacid=id,havepic=False,pic="None",descript=des,statement="Unknow")
                db.session.add(explication)
                if(request.files["image"]):
                    obj = db.session.query(Explication).order_by(Explication.id.desc()).first()
                    file=request.files.to_dict()["image"]
                    name=str(id)+"-"+str(obj.id)+".png"
                    file.save(os.path.join("./website/static/img/",name))
                    obj.havepic=True
                    obj.pic=name
                db.session.commit()

    return render_template("explication.html",transaction=transaction)


@wallet.route('/change-ex', methods=['POST'])
def change():
    note = json.loads(request.data)
    noteId = note['noteId']
    noteState= note['state']
    expli = Explication.query.get(noteId)
    expli.statement = noteState
    db.session.commit()
    return 'a string'


@wallet.route('/del_ex', methods=['POST'])
def del_ex():
    print("SUPPPRIEMR ")
    note = json.loads(request.data)
    noteId = note['noteId']
    expli = Explication.query.get(noteId)
    if expli:
        db.session.delete(expli)
        db.session.commit()
    return 'a string'
