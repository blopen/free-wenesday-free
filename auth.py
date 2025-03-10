
import uuid
from flask import Blueprint, render_template, redirect, url_for, flash, request, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from models import User
from forms import LoginForm, RegistrationForm
from authlib.integrations.flask_client import OAuth
import json
import os

auth_bp = Blueprint('auth', __name__)
oauth = OAuth()

def init_oauth(app):
    oauth.init_app(app)
    
    # Google OAuth konfigurieren
    oauth.register(
        name='google',
        client_id=os.environ.get('GOOGLE_CLIENT_ID', ''),
        client_secret=os.environ.get('GOOGLE_CLIENT_SECRET', ''),
        access_token_url='https://accounts.google.com/o/oauth2/token',
        access_token_params=None,
        authorize_url='https://accounts.google.com/o/oauth2/auth',
        authorize_params=None,
        api_base_url='https://www.googleapis.com/oauth2/v1/',
        client_kwargs={'scope': 'openid email profile'},
    )
    
    return oauth

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.find_by_email(form.email.data)
        if user is None or not user.check_password(form.password.data):
            flash('Ungültige E-Mail oder Passwort')
            return redirect(url_for('auth.login'))
            
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or next_page.startswith('/'):
            next_page = url_for('index')
        return redirect(next_page)
        
    return render_template('login.html', title='Anmelden', form=form)

@auth_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(
            id=str(uuid.uuid4()),
            email=form.email.data,
            name=form.name.data
        )
        user.set_password(form.password.data)
        user.save()
        
        flash('Glückwunsch, Sie sind jetzt registriert!')
        return redirect(url_for('auth.login'))
        
    return render_template('register.html', title='Registrieren', form=form)

@auth_bp.route('/login/google')
def google_login():
    redirect_uri = url_for('auth.google_authorize', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@auth_bp.route('/login/google/authorize')
def google_authorize():
    token = oauth.google.authorize_access_token()
    resp = oauth.google.get('userinfo')
    user_info = resp.json()
    
    # Prüfen, ob der Benutzer bereits existiert
    user = User.find_by_google_id(user_info['id'])
    
    if not user:
        # Prüfen, ob die E-Mail bereits registriert ist
        user = User.find_by_email(user_info['email'])
        
        if user:
            # Aktualisieren des vorhandenen Benutzers mit Google-ID
            user.google_id = user_info['id']
            user.save()
        else:
            # Neuen Benutzer erstellen
            user = User(
                id=str(uuid.uuid4()),
                email=user_info['email'],
                name=user_info['name'],
                google_id=user_info['id']
            )
            user.save()
    
    login_user(user)
    return redirect(url_for('index'))

@auth_bp.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Profil')

@auth_bp.route('/api/current_user')
def get_current_user():
    if current_user.is_authenticated:
        return jsonify({
            'id': current_user.id,
            'email': current_user.email,
            'name': current_user.name,
            'is_admin': current_user.is_admin
        })
    return jsonify(None)
