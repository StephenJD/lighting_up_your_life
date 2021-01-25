#$inPath = $args[0]
$inPath = "C:\Users\Stephen\Documents\Church_Teaching"
$outPath = Get-Location
$outPath = Join-Path -Path $outPath -ChildPath "\content\Teaching Materials"
$Command = "pandoc"
write-host "Inpath:" $inPath
write-host "OutPath:" $outPath
$pathStart = $inPath.Length

$outDirectory = $outPath + "\" + (get-item $inPath).Name
if (!(Test-Path $outDirectory)) { 
  New-Item -ItemType directory -Path $outDirectory
  $DirectoryName = (get-item $outDirectory).Name
  $title = "title: " + $DirectoryName
  $contents = "---`n" + $title + "`ntype: document-folder`n---`n"
  New-Item -Path $outDirectory -Name "_index.md" -ItemType "file" -Value $contents
}

foreach($file in Get-ChildItem -Path $inPath -File -Recurse -Filter "*.docx") {
    $wordDoc = $file.BaseName
    $path = $file.DirectoryName.Substring($pathStart)
    $outDirectory = $outPath + $path
    if (!(Test-Path $outDirectory)) { 
      New-Item -ItemType directory -Path $outDirectory
      $DirectoryName = (get-item $outDirectory).Name
      $title = "title: " + $DirectoryName
      $contents = "---`n" + $title + "`ntype: document-folder`n---`n"
      New-Item -Path $outDirectory -Name "_index.md" -ItemType "file" -Value $contents
    }
    $outFile = $outDirectory + "\" + $wordDoc + ".md"
    $Parms = @("-s", "-f", "docx", $file.FullName,"-t", "markdown", "-o", $outFile)
    #write-host $outFile
    & $Command $Parms

    $title = "title: " + $wordDoc
    $contents = "---`n" + $title + "`ntype: document`n---`n"
    [System.Collections.ArrayList]$lines=Get-Content $outFile;
    $lines[0]=$lines[0].Insert(0,$contents) ;
    Set-Content $outFile -Value $lines
}

$ParmsAdd = @("add", ".")
$ParmsCommit = @("commit","-m", "Upload new content")
$ParmsPush = @("push", "origin", "master")
$Git = "git"
& $Git $ParmsAdd
& $Git $ParmsCommit
& $Git $ParmsPush