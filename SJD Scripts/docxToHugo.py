from pathlib import Path
from datetime import datetime
import subprocess
from deep_translator import GoogleTranslator
import ctypes

pandocCmd = "pandoc"
docxToPdfCmd = r"C:\Hugo\docto105\docto"

def Msgbox(title, text, style):
    return ctypes.windll.user32.MessageBoxW(0, str(text), str(title), style)

def readINI() :
  webRootPath = Path.cwd()
  iniPath = webRootPath / "docxToHugo_ini.toml"
  docxRoot = webRootPath.parent / 'docx';
  sourceLanguage = 'en'
  languages = ['en']
  if iniPath.exists() :
      with iniPath.open('r', encoding="utf-8") as iniFile:
        for line in iniFile:
          line = line.strip()
          if line == "[Docx Root]":
            docxRoot = iniFile.readline().strip('\t\n "\'')
          if line == "[Docx Language]":
            sourceLanguage = iniFile.readline().strip('\t\n "\'')
          if line == "[Languages]":
            languages = iniFile.readline().strip('[] \t\n').split(',')
  return docxRoot, sourceLanguage, languages

def haveMadeNewFolder(folder) :
  if not folder.exists():
    folder.mkdir(parents=True)
    return True
  return False

def haveCreatedNewMDindex(mdDestinationPath, language):
  DirectoryName = mdDestinationPath.name
  if DirectoryName == "content" or DirectoryName == language:
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
  if not sourceFile.exists(): fileOutOfDate = False
  elif convertedFile.exists():
    convertedFileDate = datetime.fromtimestamp(convertedFile.stat().st_mtime)
    sourceFileDate = datetime.fromtimestamp(sourceFile.stat().st_mtime)
    fileOutOfDate = (sourceFileDate - convertedFileDate).total_seconds() > 120
  else:
    fileOutOfDate = True
  return fileOutOfDate

def createMDfile(sourcePath, destPath, name):
  file = destPath / (name + ".md")
  if fileNeedsUpdating(sourcePath, file):
    parms = ("-s", "-f", "docx", sourcePath,"-t", "markdown", "-o", file)
    print("Created:", name + ".md")
    subprocess.run([pandocCmd, *parms], shell=False)
    if not file.exists(): file = False
  else:
    file = False
  return file

def getDocTitle(mdFile):
  with mdFile.open('r', encoding="utf-8") as file:
    line = file.readline()
    if line.startswith('# '):
        return line[2:]
    else:
      return '¬' + line

def prependToFile(originalfile, string):
    with originalfile.open('r', encoding="utf-8") as original:
      tempFile = originalfile.parent / 'tempFile.txt'
      line = original.readline()
      if not line.startswith('# '):
        original.seek(0)
        string += '\n'

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
  contents += "\ntitle: " + translated.strip()  
  contents += "\ntype: " + type
  contents += "\ntranslationKey: " + englishTitle.strip() 
  contents += "\ngeometry: margin=2cm"
  contents += "\ngeometry: a4paper"
  #contents += "\noutput: pdf_document"
  #contents += "\npdf_document: null"
  contents += "\n---\n"
  return contents

def createPDF(sourcePath, destPath, name):
  file = destPath / (name + ".pdf")
  if fileNeedsUpdating(sourcePath, file):
    #tempName = sourcePath.replace('c:\\Hugo\\Temp.md')  
    tempPDF = Path('c:\\Hugo\\Temp.pdf')
    fromMD_Parms = ("-f", "markdown", sourcePath,"-t", "pdf", "-o", tempPDF, "--pdf-engine=xelatex" , "--toc", "-V geometry:a4paper", "-V geometry:margin=2cm")
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
              englishTitle = line[7:]
              translated = GoogleTranslator(source='en', target=language).translate(text=englishTitle)
              line = line[:7] + translated + '\n'
              translationBlock += line
            else:
              if blockLength > 5 and line == '---\n' :
                headerCompleted = True
                translation.write(translationBlock)
                translationBlock = ''
                blockLength = 0
              translationBlock += line
              blockLength += lineLen
          elif blockLength + lineLen < 4000:
            translationBlock += line
            blockLength += lineLen
          else:
            translated = GoogleTranslator(source='en', target=language).translate(text=translationBlock)
            print(translated[:10])
            translation.write(translated)
            translationBlock = ''
            blockLength = 0;
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

def deleteRemovedFiles(sourceRootPath, languages):
  mdRootPath = Path.cwd().parent / "content"

  for lang in languages:
    mdLangPath = mdRootPath / lang
    langRootStart = len(str(mdLangPath)) + 1   
    for dirItem in mdLangPath.rglob('*'):
      if 'home' in dirItem.parts: continue
      sourceItem = dirItem
      if dirItem.is_file():
        if dirItem.stem.strip('_') == 'index' : continue
        sourceItem = dirItem.parent / (dirItem.stem + '.docx')
      sourcePath = sourceRootPath / str(sourceItem)[langRootStart:]     
      if (sourcePath).exists(): 
        continue
      else:
        msg = f'Item "{dirItem.name}" is missing from {sourceRootPath}\n'
        msg += f'Do you want to delete it from {lang} folder?'
        response = Msgbox("Deleted File", msg, 4)
        if response == 6 :
          try:
            dirItem.unlink()
          except:
            Msgbox("Delete File", f"Unable to delete {dirItem.name}", 0)

def checkForUpdatedFiles():
  sourceRootPath, sourceLanguage, languages = readINI()
  msg = "Docx root is :" + sourceRootPath + '\n'
  msg += "Source Language is: " + sourceLanguage + '\n'
  msg += "Languages are: " + str(languages)
  response = Msgbox("docxToHugo_ini.toml", msg, 1)
  
  webRootPath = Path.cwd().parent
  mdRootPath = webRootPath / "content"
  #pdfRootPath = webRootPath / "static/pdf"

  sourceLanguageMDfolder = mdRootPath / sourceLanguage
  #sourceLanguagePDFfolder = pdfRootPath / sourceLanguage
  sourceRootStart = len(sourceRootPath) + 1
  sourceRootPath = Path(sourceRootPath)
  deleteRemovedFiles(sourceRootPath, languages)
  for sourceDoc in sourceRootPath.rglob('*.docx'):
    docName = sourceDoc.stem
    if docName.startswith('~'): continue
    docFolder = str(sourceDoc.parent)[sourceRootStart:]
    # Create sourceLanguage .md files
    sourceLanguageMDpath = sourceLanguageMDfolder / docFolder
    createMDfolder(sourceLanguageMDpath, sourceLanguage)
    mdFile = createMDfile(sourceDoc, sourceLanguageMDpath, docName)
    if mdFile:
      title = getDocTitle(mdFile)
      if title[0] == '¬':
        msg = f'First line of "{docName}" is not Heading 1. It is\n'
        msg += '"' + title[1:] + f'"\n Do you want to use {docName}?'
        response = Msgbox(docFolder, msg, 1)
        if (response == 2):
          mdFile.unlink()
          return
        else: title = docName
      header = createHeader(title, 'document', 'en')    
      prependToFile(mdFile, header)
    sourceLanguageMDfile = sourceLanguageMDpath / (docName + '.md')
    
    # Create English .pdf files
    #englishPDFpath = englishPDFfolder / docFolder
    #haveMadeNewFolder(englishPDFpath)
    #createPDF(sourceLanguageMDfile, englishPDFpath, docName)

    for lang in languages:
      if lang == sourceLanguage: continue
      langMDpath = mdRootPath / lang / docFolder
      createMDfolder(langMDpath, lang)
      createMDtranslation(sourceLanguageMDfile, langMDpath, docName, lang)
 
  updateWebsite()

checkForUpdatedFiles()