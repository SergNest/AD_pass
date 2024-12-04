async function showLoading() {
    document.getElementById('loading-overlay').style.display = 'flex'; // Показати спінер
    // Заблокувати всі елементи на сторінці
    document.body.style.pointerEvents = 'none';
}

async function hideLoading() {
    document.getElementById('loading-overlay').style.display = 'none'; // Сховати спінер
    // Поновити доступ до елементів на сторінці
    document.body.style.pointerEvents = 'auto';
}

async function resetPassword(userCn) {
    try {
        showLoading(); // Показати спінер

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
    } catch (error) {
        console.error('Error:', error);
        alert('Сталася помилка при виконанні запиту.');
    } finally {
        hideLoading(); // Сховати спінер після завершення
    }
}

async function toggleStatus(samAccountName, action) {
    try {
        showLoading(); // Показати спінер

        const response = await fetch('/toggle_status', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ sam_account_name: samAccountName, action: action })
        });

        const result = await response.json();
        alert(result.message);

        if (result.success) {
            location.reload();
        }
    } catch (error) {
        console.error('Error:', error);
        alert('Сталася помилка при виконанні запиту.');
    } finally {
        hideLoading(); // Сховати спінер після завершення
    }
}
