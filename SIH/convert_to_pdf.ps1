$pptxPath = "d:\Testing\Research\SIH\SETU_SIH2026_Idea_Presentation.pptx"
$pdfPath = "d:\Testing\Research\SIH\SETU_SIH2026_Idea_Presentation.pdf"

$ppt = New-Object -ComObject PowerPoint.Application
$ppt.Visible = 1

$presentation = $ppt.Presentations.Open($pptxPath)
$presentation.SaveAs($pdfPath, 32)  # 32 = ppSaveAsPDF
$presentation.Close()
$ppt.Quit()

[System.Runtime.InteropServices.Marshal]::ReleaseComObject($ppt) | Out-Null
Write-Host "PDF created successfully!"
