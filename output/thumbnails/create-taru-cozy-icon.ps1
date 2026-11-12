$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root='C:/Users/Allen/Documents/Create Swords!'
$outputPath=Join-Path $root 'Art/Icons/Taru - Create Swords - Cozy Title - 512.png'
$source=[System.Drawing.Image]::FromFile((Join-Path $root 'output/thumbnails/Taru square - base.png'))
$icon=New-Object System.Drawing.Bitmap(512,512)
$graphics=[System.Drawing.Graphics]::FromImage($icon)
$graphics.SmoothingMode=[System.Drawing.Drawing2D.SmoothingMode]::AntiAlias
$graphics.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.PixelOffsetMode=[System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$graphics.DrawImage($source,0,0,512,512)
$fonts=New-Object System.Drawing.Text.PrivateFontCollection
$fonts.AddFontFile('C:/Windows/Fonts/segoeprb.ttf')
$family=$fonts.Families[0]
function CozyLine($text,$left,$top,$width,$height) {
 $path=New-Object System.Drawing.Drawing2D.GraphicsPath
 $path.AddString($text,$family,[int][System.Drawing.FontStyle]::Bold,200,[System.Drawing.PointF]::new(0,0),[System.Drawing.StringFormat]::GenericTypographic)
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
 $shadow=$path.Clone()
 $drop=New-Object System.Drawing.Drawing2D.Matrix
 $drop.Translate(0,4)
 $shadow.Transform($drop); $drop.Dispose()
 foreach($layer in @(@{Width=16;Alpha=22},@{Width=12;Alpha=40},@{Width=8;Alpha=90})) {
  $pen=New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb($layer.Alpha,76,42,22),$layer.Width)
  $pen.LineJoin=[System.Drawing.Drawing2D.LineJoin]::Round
  $graphics.DrawPath($pen,$shadow); $pen.Dispose()
 }
 $outline=New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(255,115,67,35),8)
 $outline.LineJoin=[System.Drawing.Drawing2D.LineJoin]::Round
 $rect=[System.Drawing.RectangleF]::new($left,($top-2),$width,($height+4))
 $fill=New-Object System.Drawing.Drawing2D.LinearGradientBrush($rect,[System.Drawing.Color]::FromArgb(255,255,249,224),[System.Drawing.Color]::FromArgb(255,245,203,125),[System.Drawing.Drawing2D.LinearGradientMode]::Vertical)
 $graphics.DrawPath($outline,$path)
 $graphics.FillPath($fill,$path)
 $fill.Dispose(); $outline.Dispose(); $shadow.Dispose(); $path.Dispose()
}
CozyLine 'Create' 105 344 302 58
CozyLine 'Swords!' 35 412 442 76
$icon.Save($outputPath,[System.Drawing.Imaging.ImageFormat]::Png)
$graphics.Dispose(); $icon.Dispose(); $source.Dispose(); $fonts.Dispose()
$check=[System.Drawing.Image]::FromFile($outputPath)
Write-Output "$outputPath : $($check.Width) x $($check.Height); font: Segoe Print Bold"
$check.Dispose()
