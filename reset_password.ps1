
param (
    [string]$SamAccountName,
    [string]$NewPassword
)

# Перевіряємо, чи вказаний SamAccountName
if (-not $SamAccountName) {
    Write-Output "Error: Не вказано SamAccountName"
    exit 1
}

try {
    # Імпорт модуля Active Directory (вимагає встановлений RSAT)
    Import-Module ActiveDirectory

    # Отримання користувача за логіном
    $User = Get-ADUser -Filter "SamAccountName -eq '$SamAccountName'" -Properties DistinguishedName

    if (-not $User) {
        Write-Output "Error: Користувач не знайдений"
        exit 1
    }

    # Зміна пароля
    Set-ADAccountPassword -Identity $User.DistinguishedName -Reset -NewPassword (ConvertTo-SecureString $NewPassword -AsPlainText -Force)

    # Встановлення прапора "Користувач повинен змінити пароль при наступному вході"
    Set-ADUser -Identity $User.DistinguishedName -ChangePasswordAtLogon $true

    Write-Output "Success: Пароль для $SamAccountName змінено на $NewPassword. Користувач буде змушений змінити пароль при наступному вході."
    exit 0

} catch {
    Write-Output "Error: $_"
    exit 1
}
