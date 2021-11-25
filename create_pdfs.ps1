# Best option is to invoke print-to-pdf. This allows styles to determine what gets printed.
# Alternatives are: convert .md to .pdf - this omits the "see also" and TOC sections.
# Convert from the live-page html to .pdf. This includes stuff you don't want such as the nav-bar!
# install LaTeX from here: https://miktex.org/download
#& "hugo" "server"
$Command = "pandoc"
$outPath = "C:\Hugo\Sites\Life For Liberia\static\pdf"
$fileName = "Growth Groups - Introduction for Leaders"
$inPath =  "http://localhost:1313/teaching-materials/organic-church/growth-groups//"
$inPage = $inPath + $fileName
$md_page = "`"C:\Hugo\Sites\Life For Liberia\content\Teaching Materials\Organic Church\Growth Groups\"
$mdFile = $md_page + $fileName + ".md`""
$outFile = $outPath + "\" + $fileName + ".pdf"
$FromHTML_Parms = @("-f", "html", $inPage,"-t", "pdf", "-o", $outFile, "--pdf-engine=xelatex")
$FromMD_Parms = @("-f", "markdown", $mdFile,"-t", "pdf", "-o", $outFile, "--pdf-engine=xelatex" , "--toc")
$FromDOCX_Parms = @("-f", "markdown", $mdFile,"-t", "pdf", "-o", $outFile, "--pdf-engine=xelatex" , "--toc")
$docxPath = "C:\Users\Stephen\Documents\Church_Published\Discipleship Groups\Growth Groups"
$docxToPdf = @("-f", $docxPath, "-O", $outPath, "-T", "wdFormatPDF", "-OX", ".pdf")
$docxToPdfCmd = "C:\Hugo\docto105\docto"
#& $Command $FromMD_Parms
& $docxToPdfCmd $docxToPdf