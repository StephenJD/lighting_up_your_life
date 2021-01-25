$ParmsAdd = @("add", ".")
$ParmsCommit = @("commit","-m", "Upload new content")
$ParmsPush = @("push", "origin", "main")
$Git = "git"
& $Git $ParmsAdd
& $Git $ParmsCommit
& $Git $ParmsPush