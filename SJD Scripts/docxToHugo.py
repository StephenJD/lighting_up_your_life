from pathlib import Path
from datetime import datetime
import subprocess

sourceRootPath = r"C:\Users\Stephen\Documents\Church_Published"
webRootPath = Path.cwd().parent
languages = ('english','french')
mdRootFolder = r"content"
pdfRootFolder = r"static\pdf"
#outMDenglishPath = Join-Path -Path webRootPath -ChildPath "\content\English\Teaching Materials"
#outMDfrenchPath = Join-Path -Path webRootPath -ChildPath "\content\French\Teaching Materials"
#outPDFenglishPath = Join-Path -Path webRootPath -ChildPath "\static\pdf\English\Teaching Materials"
#outPDFfrenchPath = Join-Path -Path webRootPath -ChildPath "\static\pdf\French\Teaching Materials"
docxToMDcmd = "pandoc"
docxToPdfCmd = r"C:\Hugo\docto105\docto"

englishMDfolder = webRootPath / mdRootFolder /languages[0]
englishPDFfolder = webRootPath / pdfRootFolder / languages[0]

sourceRootStart = len(sourceRootPath)

def haveMadeNewFolder(folder) :
  if not folder.exists():
    folder.mkdir(parents=True)
    return True
  return False

def haveCreatedNewMDindex(mdDestinationPath):
  DirectoryName = mdDestinationPath.name
  if DirectoryName == "content" :
    needsIndex = False
  else:
    filePath = mdDestinationPath / "_index.md"
    needsIndex = not filePath.exists()
    if needsIndex:
      with filePath.open('w') as writeFile:
        title = "title: " + DirectoryName
        writeFile.write("---\n" + title + "\ntype: document-folder\n---\n")
  return needsIndex

def createMDfolder(mdDestinationPath) :
  if haveMadeNewFolder(mdDestinationPath):
    outerFolder = mdDestinationPath
    while haveCreatedNewMDindex(outerFolder):
      outerFolder = outerFolder.parent

def fileNeedsUpdating(sourceFile, convertedFile):
  if convertedFile.exists():
    convertedFileDate = datetime.fromtimestamp(convertedFile.stat().st_mtime)
    sourceFileDate = datetime.fromtimestamp(sourceFile.stat().st_mtime)
    fileOutOfDate = (sourceFileDate - convertedFileDate).total_seconds() > 120
  else:
    fileOutOfDate = True
  return fileOutOfDate

def createMDfile(sourcePath, destPath, name):
  #print(sourcePath)
  #print(destPath)
  #print(name + ".md")
  file = destPath / (name + ".md")
  if fileNeedsUpdating(sourcePath, file):
    parms = ("-s", "-f", "docx", sourcePath,"-t", "markdown", "-o", file)
    print("Created:", name + ".md")
    subprocess.run([docxToMDcmd, *parms], shell=False)
  else:
    file = False
  return file

def prependToFile(originalfile, string):
    with originalfile.open('r') as original:
      tempFile = originalfile.parent / 'tempFile.txt'
      with tempFile.open('w') as temp: 
        temp.write(string)
        for line in original:
          temp.write(line)
      original.close()
      originalfile.unlink()
      temp.close()
      tempFile.rename(originalfile)

def insertHeader (docPath, docName, englishTitle):
  contents = "---\ntitle: " + docName
  contents += "\ntranslationKey: " + englishTitle
  contents += "\ntype: document"
  contents += "\n---\n"
  prependToFile(docPath, contents)

def createPDF(sourcePath, destPath, name):
  file = destPath / (name + ".pdf")
  if fileNeedsUpdating(sourcePath, file):
    parms = ("-f", sourcePath, "-O", file, "-T", "wdFormatPDF", "-OX", ".pdf")
    print("Created:", name + ".pdf")
    subprocess.run([docxToPdfCmd, *parms], shell=False)

def createMDtranslation(sourcePath, destPath, name):
  file = destPath / name + ".pdf"
  if fileNeedsUpdating(sourcePath, file):
    parms = ("-f", sourcePath, "-O", file, "-T", "wdFormatPDF", "-OX", ".pdf")
    #print("Created:", name + ".pdf")

def updateWebsite():
  ParmsAdd = ("add", "..")
  ParmsCommit = ("commit","-m", "Upload new content")
  ParmsPush = ("push", "origin", "main")
  Git = "git"
  subprocess.run([Git, *ParmsAdd], shell=False)
  subprocess.run([Git, *ParmsCommit], shell=False)
  subprocess.run([Git, *ParmsPush], shell=False)

def checkForUpdatedFiles():
  #foreach(sourceDoc in Get-ChildItem -Path sourceRootPath -File -Recurse -Filter "*.docx") 
  for sourceDoc in Path(sourceRootPath).rglob('*.docx'):
    docName = sourceDoc.stem
    #docFolder = sourceDoc.Directory.Name
    docFolder = str(sourceDoc.parent)[sourceRootStart:].strip('\\')
    # Create English .md files
    englishMDpath = englishMDfolder / docFolder
    createMDfolder(englishMDpath)
    mdFile = createMDfile(sourceDoc, englishMDpath, docName)
    if mdFile: insertHeader(mdFile, docName, docName)
    
    # Create English .pdf files
    englishPDFpath = englishPDFfolder / docFolder
    haveMadeNewFolder(englishPDFpath)
    createPDF(sourceDoc, englishPDFpath, docName)    

  updateWebsite()

checkForUpdatedFiles()