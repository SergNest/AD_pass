import os
import subprocess
from loguru import logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Отримуємо поточний каталог
SCRIPTS_DIR = os.path.join(BASE_DIR, '../scripts')  # Шлях до папки з PowerShell-скриптами

logger.remove()
logger.add("app.log", rotation="10 MB", retention="10 days", compression="zip")

def run_powershell_script(script_name, **kwargs):
    script_path = os.path.join(SCRIPTS_DIR, script_name)  # Повний шлях до скрипта

    # Формуємо команду
    command = ["powershell", "-File", script_path]
    for key, value in kwargs.items():
        command.extend([f"-{key}", str(value)])

    logger.info("Запуск PowerShell-скрипта: {}", " ".join(command))

    try:
        # Виконуємо команду
        result = subprocess.run(
            command, text=True, capture_output=True, encoding='utf-8'
        )

        # Логування результату виконання
        if result.returncode == 0:
            logger.info("PowerShell-скрипт успішно виконано. Вивід: {}", result.stdout.strip())
        else:
            logger.error("Помилка виконання PowerShell-скрипта. Код: {}, Помилка: {}", result.returncode,
                         result.stderr.strip())

        return result

    except Exception as e:
        logger.exception("Виникла непередбачена помилка під час виконання PowerShell-скрипта: {}", script_name)
        raise

