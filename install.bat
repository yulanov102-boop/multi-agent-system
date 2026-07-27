@echo off
REM Установочный скрипт для мультиагента
REM Этот скрипт установит Python (если нужно) и все зависимости

echo.
echo ============================================================
echo  Установка Мультиагентной системы создания контента
echo ============================================================
echo.

REM Проверяем, установлен ли Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python не найден!
    echo.
    echo Пожалуйста, установите Python:
    echo 1. Посетите https://www.python.org/downloads/
    echo 2. Загрузите Python 3.10 или новее
    echo 3. При установке отметьте "Add Python to PATH"
    echo 4. Перезагрузите этот скрипт
    echo.
    pause
    exit /b 1
)

REM Выводим версию Python
echo ✅ Python найден:
python --version
echo.

REM Проверяем pip
pip --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ pip не найден!
    echo Пожалуйста, переустановите Python с опцией "pip"
    pause
    exit /b 1
)

echo.
echo 📦 Установка зависимостей...
echo.

REM Обновляем pip
echo Обновляю pip...
python -m pip install --upgrade pip

REM Устанавливаем зависимости
echo.
echo Устанавливаю зависимости из requirements.txt...
pip install -r requirements.txt

if %errorlevel% equ 0 (
    echo.
    echo ============================================================
    echo ✅ Установка успешно завершена!
    echo.
    echo Чтобы запустить мультиагент:
    echo   python run.py
    echo.
    echo ============================================================
) else (
    echo.
    echo ❌ Ошибка при установке зависимостей
    echo Проверьте интернет соединение и попробуйте ещё раз
)

pause
