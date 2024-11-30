import os
from ldap3 import Server, Connection, NTLM, ALL, SUBTREE
from dotenv import load_dotenv

load_dotenv()

SERVER_ADDRESS = "127.0.0.1"
BASE_DN = "DC=center,DC=com"
USER = os.getenv("USER")
PASSWORD = os.getenv("PASS")

SERVER = Server(SERVER_ADDRESS, get_info=ALL)


def get_users_for_role(view_scope):

    server = Server(SERVER_ADDRESS, get_info=ALL)
    try:
        conn = Connection(server, authentication=NTLM, user=USER, password=PASSWORD, auto_bind=True)
        if view_scope == "all":
            containers = [
                "OU=Polimer,DC=center,DC=com",
                "OU=buro,DC=center,DC=com",
                "OU=Users,DC=center,DC=com"
            ]
        else:
            containers = [view_scope]

        users = []
        for container_dn in containers:
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


def get_users_from_multiple_containers():
    container = [
        "OU=buro,DC=center,DC=com"
    ]
    try:
        conn = Connection(SERVER, authentication=NTLM, auto_bind=True, user=USER, password=PASSWORD)
        users = []
        for container_dn in container:
            conn.search(
                search_base=container_dn,
                search_filter='(objectClass=user)',
                search_scope=SUBTREE,
                attributes=['cn', 'userAccountControl', 'sAMAccountName']
            )
            for entry in conn.entries:
                cn = entry['cn']
                sam_account_name = entry['sAMAccountName'].value
                user_account_control = entry['userAccountControl'].value
                is_disabled = int(user_account_control) & 2 != 0
                users.append({'cn': cn, 'disabled': is_disabled, 'sam_account_name': sam_account_name})
        return users
    except Exception as e:
        print(f"Помилка отримання користувачів: {str(e)}")
        return []
