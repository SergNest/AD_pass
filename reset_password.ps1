
param (
    [string]$SamAccountName,
    [string]$NewPassword
)

# Перевіряємо, чи вказаний SamAccountName
if (-not $SamAccountName) {
    Write-Output "Error: Not enter SamAccountName"
    exit 1
}

try {
    # Імпорт модуля Active Directory (вимагає встановлений RSAT)
    Import-Module ActiveDirectory

    # Отримання користувача за логіном
    $User = Get-ADUser -Filter "SamAccountName -eq '$SamAccountName'" -Properties DistinguishedName

    if (-not $User) {
        Write-Output "Error: User not found"
        exit 1
    }

    # Зміна пароля
    Set-ADAccountPassword -Identity $User.DistinguishedName -Reset -NewPassword (ConvertTo-SecureString $NewPassword -AsPlainText -Force)

    # Встановлення прапора "Користувач повинен змінити пароль при наступному вході"
    Set-ADUser -Identity $User.DistinguishedName -ChangePasswordAtLogon $true

    Write-Output "Success: Password for $SamAccountName changed on $NewPassword. The user will be required to change their password at the next logon."
    exit 0

} catch {
    Write-Output "Error: $_"
    exit 1
}
