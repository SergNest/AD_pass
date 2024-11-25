[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

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
    Write-Output "Success: Пароль для $SamAccountName змінено на $NewPassword"
    exit 0

} catch {
    Write-Output "Error: $_"
    exit 1
}
