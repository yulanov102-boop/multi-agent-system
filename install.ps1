# Установочный скрипт для PowerShell
# Запустите: powershell -ExecutionPolicy Bypass -File install.ps1

Write-Host "`n" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Установка Мультиагентной системы создания контента" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "`n" -ForegroundColor Cyan

# Проверяем, установлен ли Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue

if (-not $pythonCmd) {
    Write-Host "❌ Python не найден!" -ForegroundColor Red
    Write-Host "`nПожалуйста, установите Python:" -ForegroundColor Yellow
    Write-Host "  1. Посетите https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "  2. Загрузите Python 3.10 или новее" -ForegroundColor Yellow
    Write-Host "  3. При установке отметьте 'Add Python to PATH'" -ForegroundColor Yellow
    Write-Host "  4. Перезагрузите этот скрипт" -ForegroundColor Yellow
    Write-Host "`n"
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

# Выводим версию Python
Write-Host "✅ Python найден:" -ForegroundColor Green
python --version
Write-Host ""

# Проверяем pip
$pipCmd = Get-Command pip -ErrorAction SilentlyContinue

if (-not $pipCmd) {
    Write-Host "❌ pip не найден!" -ForegroundColor Red
    Write-Host "Пожалуйста, переустановите Python с опцией 'pip'" -ForegroundColor Yellow
    Write-Host ""
    Read-Host "Нажмите Enter для выхода"
    exit 1
}

Write-Host ""
Write-Host "📦 Установка зависимостей..." -ForegroundColor Cyan
Write-Host ""

# Обновляем pip
Write-Host "Обновляю pip..." -ForegroundColor Yellow
python -m pip install --upgrade pip --quiet

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Предупреждение при обновлении pip (это может быть нормально)" -ForegroundColor Yellow
}

# Устанавливаем зависимости
Write-Host ""
Write-Host "Устанавливаю зависимости из requirements.txt..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "✅ Установка успешно завершена!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Чтобы запустить мультиагент:" -ForegroundColor Green
    Write-Host "  python run.py" -ForegroundColor White
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "❌ Ошибка при установке зависимостей" -ForegroundColor Red
    Write-Host "Проверьте интернет соединение и попробуйте ещё раз" -ForegroundColor Red
}

Write-Host ""
Read-Host "Нажмите Enter для выхода"
