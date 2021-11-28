from pathlib import Path
from datetime import datetime
import subprocess
from deep_translator import GoogleTranslator

sourceRootPath = r"C:\Users\Stephen\Documents\Church_Published"
webRootPath = Path.cwd().parent
languages = ('english','french')
mdRootFolder = r"content"
pdfRootFolder = r"static\pdf"
#outMDenglishPath = Join-Path -Path webRootPath -ChildPath "\content\English\Teaching Materials"
#outMDfrenchPath = Join-Path -Path webRootPath -ChildPath "\content\French\Teaching Materials"
#outPDFenglishPath = Join-Path -Path webRootPath -ChildPath "\static\pdf\English\Teaching Materials"
#outPDFfrenchPath = Join-Path -Path webRootPath -ChildPath "\static\pdf\French\Teaching Materials"
pandocCmd = "pandoc"
docxToPdfCmd = r"C:\Hugo\docto105\docto"

englishMDfolder = webRootPath / mdRootFolder /languages[0]
englishPDFfolder = webRootPath / pdfRootFolder / languages[0]
frenchMDfolder = webRootPath / mdRootFolder /languages[1]
frenchPDFfolder = webRootPath / pdfRootFolder / languages[1]
sourceRootStart = len(sourceRootPath)

def haveMadeNewFolder(folder) :
  if not folder.exists():
    folder.mkdir(parents=True)
    return True
  return False

def haveCreatedNewMDindex(mdDestinationPath, language):
  DirectoryName = mdDestinationPath.name
  if DirectoryName == "content" :
    needsIndex = False
  else:
    filePath = mdDestinationPath / "_index.md"
    needsIndex = not filePath.exists()
    if needsIndex:
      with filePath.open('w', encoding="utf-8") as writeFile:
        header = createHeader(DirectoryName, 'document-folder', language)  
        writeFile.write(header)
  return needsIndex

def createMDfolder(mdDestinationPath, language) :
  if haveMadeNewFolder(mdDestinationPath):
    outerFolder = mdDestinationPath
    while haveCreatedNewMDindex(outerFolder, language):
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
    subprocess.run([pandocCmd, *parms], shell=False)
  else:
    file = False
  return file

def prependToFile(originalfile, string):
    with originalfile.open('r', encoding="utf-8") as original:
      tempFile = originalfile.parent / 'tempFile.txt'
      with tempFile.open('w', encoding="utf-8") as temp: 
        temp.write(string)
        for line in original:
          temp.write(line)
      original.close()
      originalfile.unlink()
      temp.close()
      tempFile.replace(originalfile)

def createHeader (englishTitle, type, language):
  if language != 'en':
    translated = GoogleTranslator(source='en', target=language).translate(text=englishTitle)
  else:
    translated = englishTitle
  contents = "---"
  contents += "\ntype: " + type
  contents += "\ngeometry: margin=2cm"
  contents += "\npapersize: a4"
  contents += "\noutput: pdf_document"
  contents += "\npdf_document: null"
  contents += "\ntranslationKey: " + englishTitle  
  contents += "\ntitle: " + translated  
  contents += "\n---\n"
  return contents

def createPDF(sourcePath, destPath, name):
  file = destPath / (name + ".pdf")
  if fileNeedsUpdating(sourcePath, file):
    #tempName = sourcePath.replace('c:\\Hugo\\Temp.md')  
    tempPDF = Path('c:\\Hugo\\Temp.pdf')
    fromMD_Parms = ("-f", "markdown", sourcePath,"-t", "pdf", "-o", tempPDF, "--pdf-engine=xelatex" , "--toc", "-V geometry:margin=2cm")
    fromDocxParms = ("-f", sourcePath, "-O", file, "-T", "wdFormatPDF", "-OX", ".pdf")
    print("Created:", file)
    #subprocess.run([docxToPdfCmd, *fromDocxParms], shell=False)
    subprocess.run([pandocCmd, *fromMD_Parms], shell=False) # very slow, and big page boarders
    #tempName.replace(sourcePath)
    tempPDF.replace(file)

def createMDtranslation(sourceFile, destPath, name, language):
  destFile = destPath / (name + '.md')
  if fileNeedsUpdating(sourceFile, destFile):
    tempName = destFile.with_suffix('.temp')
    with sourceFile.open('r', encoding="utf-8") as original:
      with tempName.open('w', encoding="utf-8") as translation: 
        translationBlock = ''
        blockLength = 0;
        headerCompleted = False;
        for line in original:
          lineLen = len(line)
          if not headerCompleted:
            if line.startswith('title: '):
              headerCompleted = True               
              englishTitle = line[7:]
              translated = GoogleTranslator(source='en', target=language).translate(text=englishTitle)
              line = line[:7] + translated
              translationBlock += line
              translation.write(translationBlock)
              translationBlock = ''
            else:
              translationBlock += line
          elif blockLength + lineLen < 4000:
            translationBlock += line
            blockLength += lineLen
          else:
            translated = GoogleTranslator(source='en', target=language).translate(text=translationBlock)
            print(translated[:10])
            translationBlock = ''
            blockLength = 0;
            translation.write(translated)
        translated = GoogleTranslator(source='en', target=language).translate(text=translationBlock)
        translation.write(translated)
        translation.close()
        tempName.replace(destFile)

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
    createMDfolder(englishMDpath, 'en')
    mdFile = createMDfile(sourceDoc, englishMDpath, docName)
    if mdFile:
      header = createHeader(docName, 'document', 'en')    
      prependToFile(mdFile, header)

    
    # Create English .pdf files
    englishPDFpath = englishPDFfolder / docFolder
    haveMadeNewFolder(englishPDFpath)
    #createPDF(sourceDoc, englishPDFpath, docName)
    englishMDfile = englishMDpath / (docName + '.md')
    createPDF(englishMDfile, englishPDFpath, docName)

    frenchMDpath = frenchMDfolder / docFolder
    createMDfolder(frenchMDpath, 'fr')
    createMDtranslation(englishMDfile, frenchMDpath, docName,'fr')
    # Create French .pdf files
    frenchPDFpath = frenchPDFfolder / docFolder
    frenchMDfile = frenchMDpath / (docName + '.md')
    haveMadeNewFolder(frenchPDFpath)
    createPDF(frenchMDfile, frenchPDFpath, docName) 

  updateWebsite()

checkForUpdatedFiles()