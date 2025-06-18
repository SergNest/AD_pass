param (
    [string]$SamAccountName,
    [string]$NewPassword
)

# Перевірка параметрів
if (-not $SamAccountName) {
    Write-Error "Error: Parameter 'SamAccountName' is required"
    exit 1
}
if (-not $NewPassword) {
    Write-Error "Error: Parameter 'NewPassword' is required"
    exit 1
}

try {
    Import-Module ActiveDirectory -ErrorAction Stop

    # Отримання користувача
    $User = Get-ADUser -Filter { SamAccountName -eq $SamAccountName } -Properties DistinguishedName, PasswordNeverExpires

    if (-not $User) {
        Write-Error "Error: User '$SamAccountName' not found"
        exit 1
    }

    # Якщо пароль не закінчується — знімаємо прапор
    if ($User.PasswordNeverExpires) {
        Set-ADUser -Identity $User.DistinguishedName -PasswordNeverExpires $false -ErrorAction Stop
        Write-Output "Info: 'PasswordNeverExpires' unset for $SamAccountName"
    }

    # Зміна пароля
    Set-ADAccountPassword -Identity $User.DistinguishedName -Reset -NewPassword (ConvertTo-SecureString $NewPassword -AsPlainText -Force) -ErrorAction Stop

    # Вимога змінити пароль при наступному вході
    Set-ADUser -Identity $User.DistinguishedName -ChangePasswordAtLogon $true -ErrorAction Stop

    Write-Output "Success: Password for '$SamAccountName' changed to '$NewPassword'. The user will be required to change it at next logon."
    exit 0

} catch {
    Write-Error "Unhandled error: $($_.Exception.Message)"
    exit 1
}
