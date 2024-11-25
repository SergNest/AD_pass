[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

param (
    [string]$SamAccountName,
    [string]$Action  # "enable" або "disable"
)

if (-not $SamAccountName -or (-not $Action -or ($Action -ne "enable" -and $Action -ne "disable"))) {
    Write-Output "Error: Invalid parameters. Provide SamAccountName and Action (enable/disable)."
    exit 1
}

try {
    Import-Module ActiveDirectory

    $User = Get-ADUser -Filter "SamAccountName -eq '$SamAccountName'" -Properties DistinguishedName,Enabled

    if (-not $User) {
        Write-Output "Error: User not found."
        exit 1
    }

    if ($Action -eq "disable") {
        Disable-ADAccount -Identity $User.DistinguishedName
        Write-Output "Success: User $SamAccountName has been disabled."
    } elseif ($Action -eq "enable") {
        Enable-ADAccount -Identity $User.DistinguishedName
        Write-Output "Success: User $SamAccountName has been enabled."
    }
    exit 0

} catch {
    Write-Output "Error: $_"
    exit 1
}
