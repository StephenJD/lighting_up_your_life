# To enable powershell scripts to run when double-clicked:
# Open cmd in admin-mode and execute the following two commands:
# assoc .ps1=Microsoft.PowerShellScript.1
# ftype Microsoft.PowerShellScript.1=%windir%\System32\WindowsPowerShell\v1.0\powershell.exe -File "%1"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
$ParmsAdd = @("add", ".")
$ParmsCommit = @("commit","-m", "Upload new content")
$ParmsPush = @("push", "origin", "main")
$Git = "git"
& $Git $ParmsAdd
& $Git $ParmsCommit
& $Git $ParmsPush