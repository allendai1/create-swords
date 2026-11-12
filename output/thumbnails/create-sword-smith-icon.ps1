param(
 [string]$BaseFile='Taru Shard - square base.png',
 [string]$IconFile='Sword Smith - Taru Shard - 512.png'
)
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Drawing
$root='C:/Users/Allen/Documents/Create Swords!'
$source=[System.Drawing.Image]::FromFile((Join-Path (Join-Path $root 'output/thumbnails') $BaseFile))
$logo=[System.Drawing.Bitmap]::FromFile((Join-Path $root 'output/thumbnails/Sword Smith - supplied logo.png'))
$minX=$logo.Width; $minY=$logo.Height; $maxX=0; $maxY=0
for($y=0;$y -lt $logo.Height;$y+=2) {
 for($x=0;$x -lt $logo.Width;$x+=2) {
  if($logo.GetPixel($x,$y).A -gt 32) { $minX=[Math]::Min($minX,$x);$minY=[Math]::Min($minY,$y);$maxX=[Math]::Max($maxX,$x);$maxY=[Math]::Max($maxY,$y) }
 }
}
$cropX=[Math]::Max(0,$minX-2);$cropY=[Math]::Max(0,$minY-2)
$cropW=[Math]::Min($logo.Width-$cropX,$maxX-$cropX+4)
$cropH=[Math]::Min($logo.Height-$cropY,$maxY-$cropY+4)
$icon=New-Object System.Drawing.Bitmap(512,512)
$g=[System.Drawing.Graphics]::FromImage($icon)
$g.InterpolationMode=[System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.CompositingQuality=[System.Drawing.Drawing2D.CompositingQuality]::HighQuality
$g.PixelOffsetMode=[System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$g.DrawImage($source,0,0,512,512)
$logoWidth=242
$logoHeight=[int][Math]::Round($logoWidth*$cropH/$cropW)
$destination=[System.Drawing.Rectangle]::new(8,(504-$logoHeight),$logoWidth,$logoHeight)
$g.DrawImage($logo,$destination,$cropX,$cropY,$cropW,$cropH,[System.Drawing.GraphicsUnit]::Pixel)
$output=Join-Path (Join-Path $root 'Art/Icons') $IconFile
$icon.Save($output,[System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose();$icon.Dispose();$source.Dispose();$logo.Dispose()
$check=[System.Drawing.Image]::FromFile($output)
Write-Output "$output : $($check.Width) x $($check.Height), PNG; supplied logo preserved"
$check.Dispose()
