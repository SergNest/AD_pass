from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from services.ldap_service import get_users_for_role

main_bp = Blueprint('main', __name__)

USERS = {
    "admin": {"password": "Addmin123", "role": "admin", "ou": "all"},
    "buro": {"password": "buro123", "role": "user", "ou": "OU=buro,DC=center,DC=com"},
}


@main_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = USERS.get(username)
        if user and user['password'] == password:
            session['username'] = username
            session['role'] = user['role']
            session['ou'] = user['ou']
            return redirect(url_for('main.index'))

        flash('Неправильний логін або пароль')
    return render_template('login.html')


@main_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.login'))


@main_bp.route('/')
def index():
    if 'username' not in session:
        return redirect(url_for('main.login'))

    username = session['username']
    role = session['role']
    view_scope = session['ou']

    users = get_users_for_role(view_scope)
    return render_template('index.html', users=users, username=username, role=role)
