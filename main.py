from flask import Flask, request, jsonify, render_template
from ldap3 import Server, Connection, NTLM, ALL, MODIFY_REPLACE, SUBTREE
from dotenv import load_dotenv
import os

app = Flask(__name__)

load_dotenv()
SERVER_ADDRESS = "127.0.0.1"  # Локальний сервер AD
DOMAIN_NAME = "center.com"    # Ваш домен
BASE_DN = "DC=center,DC=com"  # Базовий DN для пошуку користувачів
USER = os.getenv("USER")
PASSWORD = os.getenv("PASS")

SERVER = Server(SERVER_ADDRESS, get_info=ALL)

def get_users():
    try:
        server = Server(SERVER_ADDRESS, get_info=ALL)
        conn = Connection(server, authentication=NTLM, auto_bind=True, user=user, password=password)

        conn.search(search_base=BASE_DN,
                    search_filter='(objectClass=user)',
                    search_scope=SUBTREE,
                    attributes=['cn', 'userAccountControl'])
        users = []
        for entry in conn.entries:
            cn = entry['cn']
            user_account_control = entry['userAccountControl']
            is_disabled = int(user_account_control) & 2 != 0  # Перевірка прапорця відключеного акаунта
            users.append({'cn': cn, 'disabled': is_disabled})
        return users
    except Exception as e:
        print(f"Помилка отримання користувачів: {str(e)}")
        return []


def get_users_from_multiple_containers():
    print(USER)
    print(PASSWORD)
    container = [
        "OU=buro,DC=center,DC=com"
    ]
    try:

        conn = Connection(SERVER, authentication=NTLM, auto_bind=True, user=USER, password=PASSWORD)

        users = []
        for container_dn in container:
            conn.search(search_base=container_dn,
                        search_filter='(objectClass=user)',
                        search_scope=SUBTREE,
                        attributes=['cn', 'userAccountControl', 'sAMAccountName'])
            for entry in conn.entries:
                cn = entry['cn']
                user_account_control = entry['userAccountControl'].value
                sam_account_name = entry['sAMAccountName'].value if 'sAMAccountName' in entry else 'N/A'
                is_disabled = int(user_account_control) & 2 != 0
                users.append({'cn': cn, 'disabled': is_disabled, 'sam_account_name': sam_account_name})
        return users
    except Exception as e:
        print(f"Помилка отримання користувачів: {str(e)}")
        return []


def change_user_password(user_dn, new_password):
    try:
        server = Server(SERVER_ADDRESS, get_info=ALL)
        conn = Connection(server, authentication=NTLM, auto_bind=True)
        conn.modify(user_dn, {'unicodePwd': [(MODIFY_REPLACE, [f'"{new_password}"'.encode('utf-16-le')])]})
        if conn.result['result'] == 0:
            return {"success": True, "message": f"Пароль для {user_dn} змінено."}
        else:
            return {"success": False, "message": conn.result['description']}
    except Exception as e:
        return {"success": False, "message": str(e)}


@app.route('/')
def index():
    users = get_users_from_multiple_containers()
    return render_template('index.html', users=users)


@app.route('/reset_password', methods=['POST'])
def reset_password():
    user_cn = request.json.get('user_cn')
    if not user_cn:
        return jsonify({"success": False, "message": "CN користувача не вказано."}), 400

    user_dn = f"CN={user_cn},{BASE_DN}"
    new_password = "qwerty+1"

    try:

        conn = Connection(
            SERVER,
            user=USER,  # У форматі "domain\username"
            password=PASSWORD,
            authentication=NTLM,
            auto_bind=True
        )

        # Зміна пароля
        conn.modify(
            dn=user_dn,
            changes={'unicodePwd': [(MODIFY_REPLACE, [f'"{new_password}"'.encode('utf-16-le')])]}
        )

        if conn.result['result'] == 0:
            return jsonify({"success": True, "message": f"Пароль для {user_cn} змінено на {new_password}."})
        else:
            return jsonify({"success": False, "message": f"Не вдалося змінити пароль: {conn.result['message']}"}), 400

    except Exception as e:
        return jsonify({"success": False, "message": f"Помилка: {str(e)}"}), 500


# Запуск Flask-додатку
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
