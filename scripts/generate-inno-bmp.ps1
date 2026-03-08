Add-Type -AssemblyName System.Drawing

function Draw-LogoFromImage {
	param(
		[int]$Width,
		[int]$Height,
		[string]$OutputPath,
		[string]$ImagePath,
		[bool]$IsBig = $false
	)

	$bmp = New-Object System.Drawing.Bitmap($Width, $Height, [System.Drawing.Imaging.PixelFormat]::Format24bppRgb)
	$g = [System.Drawing.Graphics]::FromImage($bmp)

	# High quality scaling
	$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
	$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
	$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

	# Dark background color (a nice dark-gray/black that fits the transparent logo)
	$bgColor = [System.Drawing.Color]::FromArgb(30, 30, 30)
	$g.Clear($bgColor)

	$srcImg = [System.Drawing.Image]::FromFile($ImagePath)

	if ($IsBig) {
		# Logo in upper half for the sidebar
		$iconSize = [float]([Math]::Min($Width * 0.75, $Height * 0.40))
		$iconX = [float](($Width - $iconSize) / 2.0)
		$iconY = [float]($Height * 0.1)

		$g.DrawImage($srcImg, $iconX, $iconY, $iconSize, $iconSize)

		# Add SAgentai text underneath
		$nameFontSize = [float]($Width * 0.115)
		$nameFont = New-Object System.Drawing.Font("Segoe UI", $nameFontSize, [System.Drawing.FontStyle]::Bold)
		$nameBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(240, 240, 240))
		$nameStr = "SAgentai"
		$nameSize = $g.MeasureString($nameStr, $nameFont)
		$nameX = [float](($Width - $nameSize.Width) / 2.0)
		$nameY = [float]($iconY + $iconSize + $Height * 0.05)
		$g.DrawString($nameStr, $nameFont, $nameBrush, $nameX, $nameY)
		$nameFont.Dispose()
		$nameBrush.Dispose()

	}
 else {
		# Fill/Center for the small top-right square
		$iconSize = [float]([Math]::Min($Width, $Height) * 0.8)
		$iconX = [float](($Width - $iconSize) / 2.0)
		$iconY = [float](($Height - $iconSize) / 2.0)

		$g.DrawImage($srcImg, $iconX, $iconY, $iconSize, $iconSize)
	}

	$srcImg.Dispose()
	$g.Dispose()
	$bmp.Save($OutputPath, [System.Drawing.Imaging.ImageFormat]::Bmp)
	$bmp.Dispose()

	Write-Host "Saved: $OutputPath ($Width x$Height)"
}

$dir = "D:\SAgentai\resources\win32"
# Using the highest resolution one to ensure sharp scaling up
$sourceImage = "D:\SAgentai\resources\linux\code.png"
if (-Not (Test-Path $sourceImage)) {
	$sourceImage = "D:\SAgentai\resources\win32\code_150x150.png"
}

$bigFiles = @(
	@{n = "inno-big-100"; w = 164; h = 314 },
	@{n = "inno-big-125"; w = 205; h = 392 },
	@{n = "inno-big-150"; w = 246; h = 471 },
	@{n = "inno-big-175"; w = 287; h = 549 },
	@{n = "inno-big-200"; w = 328; h = 628 },
	@{n = "inno-big-225"; w = 369; h = 706 },
	@{n = "inno-big-250"; w = 410; h = 785 }
)

$smallFiles = @(
	@{n = "inno-small-100"; w = 55; h = 55 },
	@{n = "inno-small-125"; w = 68; h = 68 },
	@{n = "inno-small-150"; w = 83; h = 83 },
	@{n = "inno-small-175"; w = 97; h = 97 },
	@{n = "inno-small-200"; w = 110; h = 110 },
	@{n = "inno-small-225"; w = 124; h = 124 },
	@{n = "inno-small-250"; w = 138; h = 138 }
)

foreach ($f in $bigFiles) {
	Draw-LogoFromImage -Width $f.w -Height $f.h -OutputPath "$dir\$($f.n).bmp" -ImagePath $sourceImage -IsBig $true
}

foreach ($f in $smallFiles) {
	Draw-LogoFromImage -Width $f.w -Height $f.h -OutputPath "$dir\$($f.n).bmp" -ImagePath $sourceImage -IsBig $false
}

Write-Host "`nAll 14 BMP files generated successfully using the logo image."
