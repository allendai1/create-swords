$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root='C:/Users/Allen/Documents/Create Swords!'
$sourcePath=Join-Path $root 'output/thumbnails/Taru square - base.png'
$outputPath=Join-Path $root 'Art/Icons/Taru - Create Swords - Large Title - 512.png'
$source=[System.Drawing.Image]::FromFile($sourcePath)
$icon=New-Object System.Drawing.Bitmap(512,512)
$graphics=[System.Drawing.Graphics]::FromImage($icon)
$graphics.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.PixelOffsetMode=[System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$graphics.DrawImage($source,0,0,512,512)
$fonts=New-Object System.Drawing.Text.PrivateFontCollection
$fonts.AddFontFile((Join-Path $root 'Models/Thumbnail/Font/bloodcrow.ttf'))
$family=$fonts.Families[0]
function TitleLine($text,$left,$top,$width,$height,$fillColor) {
 $path=New-Object System.Drawing.Drawing2D.GraphicsPath
 $path.AddString($text,$family,0,200,[System.Drawing.PointF]::new(0,0),[System.Drawing.StringFormat]::GenericTypographic)
 $bounds=$path.GetBounds()
 $move=New-Object System.Drawing.Drawing2D.Matrix
 $move.Translate(-$bounds.X,-$bounds.Y)
 $path.Transform($move); $move.Dispose()
 $scale=New-Object System.Drawing.Drawing2D.Matrix
 $scale.Scale(($width/$bounds.Width),($height/$bounds.Height))
 $path.Transform($scale); $scale.Dispose()
 $place=New-Object System.Drawing.Drawing2D.Matrix
 $place.Translate($left,$top)
 $path.Transform($place); $place.Dispose()
 $outside=New-Object System.Drawing.Pen([System.Drawing.Color]::White,12)
 $outside.LineJoin=[System.Drawing.Drawing2D.LineJoin]::Round
 $outline=New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255,20,10,10),8)
 $outline.LineJoin=[System.Drawing.Drawing2D.LineJoin]::Round
 $brush=New-Object System.Drawing.SolidBrush($fillColor)
 $graphics.DrawPath($outside,$path)
 $graphics.DrawPath($outline,$path)
 $graphics.FillPath($brush,$path)
 $brush.Dispose(); $outside.Dispose(); $outline.Dispose(); $path.Dispose()
}
TitleLine 'Create' 79 349 354 57 ([System.Drawing.Color]::White)
TitleLine 'Swords!' 22 414 468 78 ([System.Drawing.Color]::FromArgb(255,235,32,25))
$icon.Save($outputPath,[System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose(); $icon.Dispose(); $source.Dispose(); $fonts.Dispose()
$check=[System.Drawing.Image]::FromFile($outputPath)
Write-Output "$outputPath : $($check.Width) x $($check.Height); font: Blood Crow"
$check.Dispose()
