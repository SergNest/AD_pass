from flask import Flask, request, jsonify, render_template
from ldap3 import Server, Connection, NTLM, ALL, MODIFY_REPLACE, SUBTREE

app = Flask(__name__)


SERVER_ADDRESS = "192.168.137.99"  # Локальний сервер AD
DOMAIN_NAME = "center.com"    # Ваш домен
BASE_DN = "DC=center,DC=com"  # Базовий DN для пошуку користувачів


def get_users():
    try:
        server = Server(SERVER_ADDRESS, get_info=ALL)
        conn = Connection(server, authentication=NTLM, auto_bind=True)

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
    container = [
        "OU=buro,DC=center,DC=com"
    ]
    try:
        server = Server(SERVER_ADDRESS, get_info=ALL)
        conn = Connection(server, authentication=NTLM, auto_bind=True)

        users = []
        for container_dn in container:
            conn.search(search_base=container_dn,
                        search_filter='(objectClass=user)',
                        search_scope=SUBTREE,
                        attributes=['cn', 'userAccountControl'])
            for entry in conn.entries:
                cn = entry['cn']
                user_account_control = entry['userAccountControl']
                is_disabled = int(user_account_control) & 2 != 0
                users.append({'cn': cn, 'disabled': is_disabled})
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
    result = change_user_password(user_dn, new_password)
    return jsonify(result)


# Запуск Flask-додатку
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
