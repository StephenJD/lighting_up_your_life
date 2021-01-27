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
$FromMD_Parms = @("-f", "markdown", $mdFile,"-t", "pdf", "-o", $outFile, "--pdf-engine=xelatex")
& $Command $FromMD_Parms