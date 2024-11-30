async function resetPassword(userCn) {
    const response = await fetch('/reset_password', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_cn: userCn })
    });
    const result = await response.json();
    alert(result.message);
    if (result.success) {
        location.reload();
    }
}

async function toggleStatus(samAccountName, action) {
    const response = await fetch('/toggle_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sam_account_name: samAccountName, action: action })
    });

    const result = await response.json();
    alert(result.message);

    if (result.success) {
        // Знайти відповідний рядок у таблиці за допомогою samAccountName
        const row = document.querySelector(`tr[data-username="${samAccountName}"]`);

        if (row) {
            // Змінити клас рядка в залежності від статусу
            if (action === 'disable') {
                row.classList.add('disabled-user');  // Додаємо клас для "відключеного"
                row.cells[2].innerText = "Відключений";  // Оновлюємо статус у таблиці
            } else {
                row.classList.remove('disabled-user');  // Видаляємо клас для "активного"
                row.cells[2].innerText = "Активний";  // Оновлюємо статус у таблиці
            }
        }
    }
}

