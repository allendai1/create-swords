$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root = 'C:/Users/Allen/Documents/Create Swords!'
$folder = Join-Path $root 'Art/Thumbnail/Concept 3 - Taru'
$backplatePath = Join-Path $root 'output/thumbnails/Create Swords - brush backplate.png'
$fontPath = Join-Path $root 'Models/Thumbnail/Font/bloodcrow.ttf'
$logoPath = Join-Path $folder 'Create Swords - Blood Crow Logo.png'
$finalPath = Join-Path $folder 'Taru Hero - Create Swords Logo.png'
$previewPath = Join-Path $folder 'Taru Hero - Create Swords Logo - phone preview.png'
function Quality($graphics) {
 $graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
 $graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
 $graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
 $graphics.CompositingQuality = [System.Drawing.Drawing2D.CompositingQuality]::HighQuality
}
$fontCollection = New-Object System.Drawing.Text.PrivateFontCollection
$fontCollection.AddFontFile($fontPath)
$family = $fontCollection.Families[0]
Write-Output "Loaded font: $($family.Name) from $fontPath"
$backplate = [System.Drawing.Bitmap]::FromFile($backplatePath)
$minX=$backplate.Width; $minY=$backplate.Height; $maxX=0; $maxY=0
for ($y=0; $y -lt $backplate.Height; $y+=3) {
 for ($x=0; $x -lt $backplate.Width; $x+=3) {
  if ($backplate.GetPixel($x,$y).A -gt 160) { $minX=[Math]::Min($minX,$x); $minY=[Math]::Min($minY,$y); $maxX=[Math]::Max($maxX,$x); $maxY=[Math]::Max($maxY,$y) }
 }
}
$logo = New-Object System.Drawing.Bitmap(1100,1000)
$g = [System.Drawing.Graphics]::FromImage($logo)
Quality $g
$g.Clear([System.Drawing.Color]::Transparent)
$g.FillEllipse([System.Drawing.Brushes]::White,90,65,930,860)
$dest = New-Object System.Drawing.Rectangle(10,10,1080,980)
$g.DrawImage($backplate,$dest,$minX,$minY,($maxX-$minX+1),($maxY-$minY+1),[System.Drawing.GraphicsUnit]::Pixel)
$g.FillEllipse([System.Drawing.Brushes]::White,130,110,850,780)
function Lettering($text,$left,$top,$width,$height) {
 $glyphs = New-Object System.Drawing.Drawing2D.GraphicsPath
 $glyphs.AddString($text,$family,[int][System.Drawing.FontStyle]::Regular,250,[System.Drawing.PointF]::new(0,0),[System.Drawing.StringFormat]::GenericTypographic)
 $bounds=$glyphs.GetBounds()
 $matrix=New-Object System.Drawing.Drawing2D.Matrix
 $matrix.Translate(-$bounds.X,-$bounds.Y)
 $glyphs.Transform($matrix); $matrix.Dispose()
 $matrix=New-Object System.Drawing.Drawing2D.Matrix
 $matrix.Scale(($width/$bounds.Width),($height/$bounds.Height))
 $glyphs.Transform($matrix); $matrix.Dispose()
 $matrix=New-Object System.Drawing.Drawing2D.Matrix
 $matrix.Translate($left,$top)
 $glyphs.Transform($matrix); $matrix.Dispose()
 $outline=New-Object System.Drawing.Pen([System.Drawing.Color]::White,12)
 $outline.LineJoin=[System.Drawing.Drawing2D.LineJoin]::Round
 $g.DrawPath($outline,$glyphs)
 $g.FillPath([System.Drawing.Brushes]::Black,$glyphs)
 $outline.Dispose(); $glyphs.Dispose()
}
Lettering 'Create' 80 210 940 290
Lettering 'Swords!' 20 515 1060 300
$logo.Save($logoPath,[System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose(); $backplate.Dispose()
$base=[System.Drawing.Image]::FromFile((Join-Path $folder 'Taru Hero.png'))
$final=New-Object System.Drawing.Bitmap($base.Width,$base.Height)
$fg=[System.Drawing.Graphics]::FromImage($final)
Quality $fg
$fg.DrawImage($base,0,0,$base.Width,$base.Height)
$fg.DrawImage($logo,22,645,455,414)
$fg.Dispose(); $base.Dispose(); $logo.Dispose()
$final.Save($finalPath,[System.Drawing.Imaging.ImageFormat]::Png)
$preview=New-Object System.Drawing.Bitmap(400,225)
$pg=[System.Drawing.Graphics]::FromImage($preview)
Quality $pg
$pg.DrawImage($final,0,0,400,225)
$preview.Save($previewPath,[System.Drawing.Imaging.ImageFormat]::Png)
$pg.Dispose(); $preview.Dispose(); $final.Dispose(); $fontCollection.Dispose()
foreach ($path in @($logoPath,$finalPath,$previewPath)) {
 $check=[System.Drawing.Image]::FromFile($path)
 Write-Output "$path : $($check.Width) x $($check.Height)"
 $check.Dispose()
}
