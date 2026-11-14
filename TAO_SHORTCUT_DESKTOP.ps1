param([string]$Source = (Join-Path (Split-Path $PSScriptRoot) 'ZaloRec.exe'))
$ErrorActionPreference = 'Stop'
if (-not (Test-Path -LiteralPath $Source)) { throw 'Chưa có EXE đã cài. Hãy chạy bộ cài trước.' }
$exePath = (Resolve-Path -LiteralPath $Source).Path
$link = (New-Object -ComObject WScript.Shell).CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'ZaloRec.lnk'))
$link.TargetPath = $exePath
$link.WorkingDirectory = Split-Path $exePath
$link.IconLocation = "$exePath,0"
$link.Save()
