import os
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Отримуємо поточний каталог
SCRIPTS_DIR = os.path.join(BASE_DIR, '../scripts')     # Шлях до папки з PowerShell-скриптами


def run_powershell_script(script_name, **kwargs):
    script_path = os.path.join(SCRIPTS_DIR, script_name)  # Повний шлях до скрипта
    command = ["powershell", "-File", script_path]
    for key, value in kwargs.items():
        command.extend([f"-{key}", str(value)])

    result = subprocess.run(
        command, text=True, capture_output=True, encoding='utf-8'
    )
    return result
