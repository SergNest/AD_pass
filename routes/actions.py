from flask import Blueprint, request, jsonify
from services.powershell_service import run_powershell_script

actions_bp = Blueprint('actions', __name__)


@actions_bp.route('/reset_password', methods=['POST'])
def reset_password():
    sam_account_name = request.json.get('user_cn')
    if not sam_account_name:
        return jsonify({"success": False, "message": "Не вказано SamAccountName"}), 400

    new_password = "qwerty+1"

    result = run_powershell_script(
        "reset_password.ps1", SamAccountName=sam_account_name, NewPassword=new_password
    )
    if result.returncode == 0:
        return jsonify({"success": True, "message": result.stdout.strip()})
    else:
        return jsonify({"success": False, "message": result.stderr.strip()}), 500


@actions_bp.route('/toggle_status', methods=['POST'])
def toggle_status():
    sam_account_name = request.json.get('sam_account_name')
    action = request.json.get('action')  # "enable" або "disable"

    if not sam_account_name or action not in ["enable", "disable"]:
        return jsonify({"success": False, "message": "Invalid parameters."}), 400

    result = run_powershell_script(
        "toggle_account_status.ps1", SamAccountName=sam_account_name, Action=action
    )
    if result.returncode == 0:
        return jsonify({"success": True, "message": result.stdout.strip()})
    else:
        return jsonify({"success": False, "message": result.stderr.strip()}), 500
