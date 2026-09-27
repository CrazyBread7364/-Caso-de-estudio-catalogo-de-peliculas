<#
.SYNOPSIS
    Script automatizado para crear y restaurar la base de datos PostgreSQL 'caescapel'.
.DESCRIPTION
    Detecta automáticamente la instalación de psql (incluso si no está en el PATH),
    crea la base de datos si no existe y restaura el volcado completo con los datos iniciales.
#>

param(
    [string]$DbName = "caescapel",
    [string]$DbUser = "postgres",
    [string]$DbPassword = "root",
    [string]$DbHost = "localhost",
    [string]$DbPort = "5432",
    [string]$BackupFile = "backup_completo_caescapel.sql"
)

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "  Inicializador y Restaurador de Base de Datos PostgreSQL" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Localizar el ejecutable psql
$psqlPath = $null
$command = Get-Command psql -ErrorAction SilentlyContinue
if ($command) {
    $psqlPath = $command.Source
} else {
    $possiblePaths = Get-ChildItem -Path "C:\Program Files\PostgreSQL\*\bin\psql.exe" -ErrorAction SilentlyContinue | Sort-Object FullName -Descending
    if ($possiblePaths) {
        $psqlPath = $possiblePaths[0].FullName
    }
}

if (-not $psqlPath -or -not (Test-Path $psqlPath)) {
    Write-Host "[ERROR] No se encontró el ejecutable 'psql.exe'." -ForegroundColor Red
    Write-Host "Verifica que PostgreSQL esté instalado o especifica la ruta de instalación." -ForegroundColor Yellow
    exit 1
}

Write-Host "[+] Usando psql: $psqlPath" -ForegroundColor Green

# 2. Localizar el archivo de respaldo
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
if (-not $scriptDir) { $scriptDir = (Get-Location).Path }
$backupFullPath = Join-Path $scriptDir $BackupFile

if (-not (Test-Path $backupFullPath)) {
    if (Test-Path $BackupFile) {
        $backupFullPath = (Resolve-Path $BackupFile).Path
    } else {
        Write-Host "[ERROR] No se encontró el archivo de respaldo: $BackupFile" -ForegroundColor Red
        exit 1
    }
}

Write-Host "[+] Archivo de respaldo: $backupFullPath" -ForegroundColor Green

# 3. Configurar entorno con contraseña
$env:PGPASSWORD = $DbPassword

# 4. Crear la base de datos si no existe
Write-Host "`n[1/3] Verificando base de datos '$DbName'..." -ForegroundColor Cyan
$checkQuery = "SELECT 1 FROM pg_database WHERE datname='$DbName';"
$dbExists = & $psqlPath -h $DbHost -p $DbPort -U $DbUser -d postgres -tAc $checkQuery 2>$null

if ($dbExists -and $dbExists.Trim() -eq "1") {
    Write-Host "[OK] La base de datos '$DbName' ya existe." -ForegroundColor Yellow
} else {
    Write-Host "[+] Creando base de datos '$DbName'..." -ForegroundColor Cyan
    & $psqlPath -h $DbHost -p $DbPort -U $DbUser -d postgres -c "CREATE DATABASE $DbName;"
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Falló la creación de la base de datos." -ForegroundColor Red
        exit $LASTEXITCODE
    }
    Write-Host "[OK] Base de datos '$DbName' creada exitosamente." -ForegroundColor Green
}

# 5. Restaurar el volcado SQL
Write-Host "`n[2/3] Restaurando tablas y datos desde '$BackupFile'..." -ForegroundColor Cyan
& $psqlPath -h $DbHost -p $DbPort -U $DbUser -d $DbName -f $backupFullPath

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ALERTA] psql finalizó con código: $LASTEXITCODE. Revisa los mensajes anteriores." -ForegroundColor Yellow
} else {
    Write-Host "[OK] Restauración completada sin errores." -ForegroundColor Green
}

# 6. Comprobar datos cargados
Write-Host "`n[3/3] Validando datos en la tabla MovieService_movie..." -ForegroundColor Cyan
$countQuery = 'SELECT count(*) FROM "MovieService_movie";'
$movieCount = (& $psqlPath -h $DbHost -p $DbPort -U $DbUser -d $DbName -tAc $countQuery 2>$null)

if ($movieCount) {
    $trimmedCount = $movieCount.Trim()
    Write-Host "[ÉXITO] Total de películas registradas en la base de datos: $trimmedCount" -ForegroundColor Green
} else {
    Write-Host "[INFO] No se pudo verificar el conteo automático de películas." -ForegroundColor Gray
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host "  ¡Base de datos lista para usarse con el backend!" -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Green
