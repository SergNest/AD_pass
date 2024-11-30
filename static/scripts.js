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
        location.reload();
    }
}
