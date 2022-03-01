from flask import Blueprint , render_template , request , flash ,redirect , url_for
from .models import User 
from werkzeug.security import generate_password_hash , check_password_hash
from . import db
from flask_login import login_user , login_required , logout_user , current_user

auth = Blueprint('auth',__name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password,password):
                flash(f"<3 Bienvenu {user.name} <3", category="success")
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash(f"Mauvais mot de passe !", category="error")
        else:
            flash(f"Cette email n'existe pas!", category="error")
    return render_template("login.html", method=['GET', 'POST'],user=current_user)

@auth.route('/logout',methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign():
    if request.method == 'POST':
        email = request.form.get('email')
        print(email)
        name = request.form.get('name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter_by(email=email).first()
        if user :
            flash("Cette email est déjà enregistré.", category="error")
        elif len(email) <4 :
            flash("Poto ton email n'est pas valide.", category="error")
        elif len(name) <2 :
            flash("2 lettres pour ton nom ? Abuse frére .. ", category="error")
        elif len(password1) < 7 :
            flash("Abuse poto...Mot de passe trop court, 7 lettres minimum.", category="error")
        elif password1 != password2:
            flash("Les mots de passe ne correspondent pas. (ù_ù) ...", category="error")
        else:
            flash("<3 Compte créé avec succès, essaye de te connecter <3", category="success")
            new_user = User(email=email, name = name, password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            return redirect(url_for('views.home'))
    return render_template("sign-up.html",user=current_user)
