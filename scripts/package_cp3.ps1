$ErrorActionPreference = 'Stop'

$workspace = (Resolve-Path -LiteralPath (Join-Path $PSScriptRoot '..')).Path
$stage = Join-Path $workspace 'cp3_package_staging'
$zip = Join-Path $workspace 'CP3_FINCHAT_GRUPO_PROVISORIO.zip'

function Assert-InStage([string]$Path) {
    $full = [System.IO.Path]::GetFullPath($Path)
    if (-not $full.StartsWith($stage + [System.IO.Path]::DirectorySeparatorChar, [System.StringComparison]::OrdinalIgnoreCase) -and $full -ne $stage) {
        throw "Caminho fora da area temporaria: $full"
    }
}

if (Test-Path -LiteralPath $stage) {
    $resolvedStage = (Resolve-Path -LiteralPath $stage).Path
    Assert-InStage $resolvedStage
    Remove-Item -LiteralPath $resolvedStage -Recurse -Force
}
New-Item -ItemType Directory -Path $stage | Out-Null

$directories = @('alembic', 'app', 'docs', 'evidencias', 'scripts', 'tests', 'frontend')
foreach ($directory in $directories) {
    Copy-Item -LiteralPath (Join-Path $workspace $directory) -Destination $stage -Recurse
}

$rootFiles = @(
    '.dockerignore', '.env.example', '.gitattributes', '.gitignore',
    'alembic.ini', 'compose.yaml', 'Dockerfile', 'pytest.ini', 'README.md',
    'render.yaml', 'requirements-lock.txt', 'requirements.txt'
)
foreach ($file in $rootFiles) {
    Copy-Item -LiteralPath (Join-Path $workspace $file) -Destination $stage
}

$excludedDirectories = @('__pycache__', '.pytest_cache', 'node_modules', 'dist', '.vite', 'coverage', 'htmlcov')
$directoriesToRemove = Get-ChildItem -LiteralPath $stage -Directory -Recurse -Force |
    Where-Object { $_.Name -in $excludedDirectories } |
    Sort-Object FullName -Descending
foreach ($item in $directoriesToRemove) {
    Assert-InStage $item.FullName
    Remove-Item -LiteralPath $item.FullName -Recurse -Force
}

$filesToRemove = Get-ChildItem -LiteralPath $stage -File -Recurse -Force |
    Where-Object { $_.Name -match '\.py[co]$|\.tsbuildinfo$|\.log$|\.db($|\.)|\.sqlite[3]?$' -or $_.Name -eq '.env' }
foreach ($item in $filesToRemove) {
    Assert-InStage $item.FullName
    Remove-Item -LiteralPath $item.FullName -Force
}

Compress-Archive -Path (Join-Path $stage '*') -DestinationPath $zip -CompressionLevel Optimal -Force

$resolvedStage = (Resolve-Path -LiteralPath $stage).Path
Assert-InStage $resolvedStage
Remove-Item -LiteralPath $resolvedStage -Recurse -Force

Get-Item -LiteralPath $zip | Select-Object FullName, Length, LastWriteTime
