#Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope LocalMachine
#$sourceRootPath = $args[0]
$sourceRootPath = "C:\Users\Stephen\Documents\Church_Published"
$webRootPath = Get-Location
$webRootPath = (get-item $webRootPath).parent.FullName
$languages = @('English','French')
$mdRootFolder = "\content\"
$pdfRootFolder = "\static\pdf\"
#$outMDenglishPath = Join-Path -Path $webRootPath -ChildPath "\content\English\Teaching Materials"
#$outMDfrenchPath = Join-Path -Path $webRootPath -ChildPath "\content\French\Teaching Materials"
#$outPDFenglishPath = Join-Path -Path $webRootPath -ChildPath "\static\pdf\English\Teaching Materials"
#$outPDFfrenchPath = Join-Path -Path $webRootPath -ChildPath "\static\pdf\French\Teaching Materials"
$docxToMDcmd = "pandoc"
$docxToPdfCmd = "C:\Hugo\docto105\docto"
write-host "Inpath:" $sourceRootPath

$englishMDfolder = $webRootPath + $mdRootFolder + $languages[0]
$englishPDFfolder = $webRootPath + $pdfRootFolder + $languages[0]

$sourceRootStart = $sourceRootPath.Length

function New-Folder($folder) {
  if (!(Test-Path $folder)) {
    New-Item -ItemType directory -Path $folder 
    return $true
  }
  return $false
}
function New-mdIndex($mdDestinationPath){
  $DirectoryName = (get-item $mdDestinationPath).Name
  if ($DirectoryName -eq "content") {
    $needsIndex = $false
  } else {
    $needsIndex = !(Test-Path ($mdDestinationPath + "\_index.md"))
    if ($needsIndex) {
      $title = "title: " + $DirectoryName
      $contents = "---`n" + $title + "`ntype: document-folder`n---`n"
      New-Item -Path $mdDestinationPath -Name "_index.md" -ItemType "file" -Value $contents
    }
  }
  return $needsIndex
}

function New-mdFolder($mdDestinationPath) {
  if (New-Folder $mdDestinationPath) {
    $outerFolder = $mdDestinationPath
    while (New-mdIndex($outerFolder)) {
      $outerFolder = (get-item $outerFolder).parent.FullName
    } 
  }
}


function Test-FileNeedsUpdating($sourceFile, $convertedFile) {
  if (Test-Path ($convertedFile)) {
    $convertedFileDate = (get-item $convertedFile).LastWriteTime
    $sourceFileDate = (get-item $sourceFile.FullName).LastWriteTime
    $fileOutOfDate = ($sourceFileDate - $convertedFileDate).Minutes -gt 2
  } else {
    $fileOutOfDate = $true
  }
  return $fileOutOfDate
}
function New-mdFile($sourcePath, $destPath, $name){
  $file = $destPath + "\" + $name + ".md"
  if (Test-FileNeedsUpdating $sourcePath $file) {
    $sourcePath = $sourcePath.FullName
    $parms = @("-s", "-f", "docx", $sourcePath,"-t", "markdown", "-o", $file)
    write-host "Created:" ($name + ".md")
    & $docxToMDcmd $parms
  } else {
    $file = $false
  }
  return $file
}

function Add-Title ($docPath, $docName){
  $title = "title: " + $docName
  $contents = "---`n" + $title + "`ntype: document`n---`n"
  [System.Collections.ArrayList]$lines=Get-Content $docPath;
  $lines[0]=$lines[0].Insert(0,$contents) ;
  Set-Content $docPath -Value $lines
}

function New-PDF($sourcePath, $destPath, $name){
  $file = $destPath + "\" + $name + ".pdf"
  if (Test-FileNeedsUpdating $sourcePath $file) {
    $sourcePath = $sourcePath.FullName
    $parms = @("-f", $sourcePath, "-O", $file, "-T", "wdFormatPDF", "-OX", ".pdf")
    write-host "Created:" ($name + ".pdf")
    & $docxToPdfCmd $parms
  }
}

function Update-Website{
  $ParmsAdd = @("add", ".")
  $ParmsCommit = @("commit","-m", "Upload new content")
  $ParmsPush = @("push", "origin", "main")
  $Git = "git"
  & $Git $ParmsAdd
  & $Git $ParmsCommit
  & $Git $ParmsPush
}

foreach($sourceDoc in Get-ChildItem -Path $sourceRootPath -File -Recurse -Filter "*.docx") {
  $docName = $sourceDoc.BaseName
  #$docFolder = $sourceDoc.Directory.Name
  $docFolder = $sourceDoc.DirectoryName.Substring($sourceRootStart)
  # Create English .md files
  $englishMDpath = $englishMDfolder + $docFolder
  New-mdFolder $englishMDpath
  $mdFile = New-mdFile $sourceDoc $englishMDpath $docName
  if ($mdFile) {Add-Title $mdFile $docName}
  
  # Create English .pdf files
  $englishPDFpath = $englishPDFfolder + $docFolder
  $throwAway = New-Folder $englishPDFpath
  New-PDF $sourceDoc $englishPDFpath $docName    
}
Update-Website