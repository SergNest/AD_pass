from flask import Blueprint, render_template
from services.ldap_service import get_users_from_multiple_containers

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    users = get_users_from_multiple_containers()
    return render_template('index.html', users=users)
