# Мультиагентная система создания контента

## 🚀 Быстрый старт

### 1. Установка Python

Если у вас ещё не установлен Python:

**Windows:**
- Загрузите Python с [python.org](https://www.python.org/downloads/)
- При установке отметьте ✅ "Add Python to PATH"

**После установки Python:**

```powershell
# Проверьте версию
python --version
```

### 2. Установка зависимостей

```powershell
# Перейдите в папку проекта
cd "c:\Users\user\Desktop\Мой мультигагент"

# Установите зависимости
pip install -r requirements.txt
```

### 3. Настройка переменных окружения

Отредактируйте файл `.env`:

```env
# Добавьте ваш API ключ Anthropic
ANTHROPIC_API_KEY=sk-ant-v1-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Получить API ключ: https://console.anthropic.com/

### 4. Запуск мультиагента

```powershell
python run.py
```

## 📋 Архитектура

### Агенты системы:

1. **🔍 Исследователь** - Собирает информацию, проверяет факты
2. **✍️ Копирайтер** - Создаёт привлекательный контент
3. **🎨 Дизайнер** - Разрабатывает концепции визуалов
4. **📱 Telegram-агент** - Адаптирует контент для Telegram
5. **✅ Финальный редактор** - Проверяет качество

### Рабочий процесс:

```
Задача
  ↓
🔍 Исследователь → Собранная информация
  ↓
✍️ Копирайтер → Готовая статья
  ↓
🎨 Дизайнер → Концепция визуала
  ↓
📱 Telegram-агент → Telegram-пост
  ↓
✅ Финальный редактор → Одобренный контент
  ↓
📂 Результаты в outputs/
```

## 📁 Структура проекта

```
├── agents/              # Модули агентов
│   ├── researcher.py    # Исследователь
│   ├── copywriter.py    # Копирайтер
│   ├── designer.py      # Дизайнер
│   ├── telegram_agent.py # Telegram-агент
│   └── editor.py        # Финальный редактор
├── utils/               # Утилиты
│   ├── claude_client.py # Клиент Claude API
│   └── config_loader.py # Загрузчик конфигов
├── config/              # Конфигурация
│   ├── settings.yaml    # Глобальные настройки
│   └── agents.yaml      # Конфиги агентов
├── orchestrator.py      # Оркестратор рабочего процесса
├── run.py              # Главный скрипт запуска
├── outputs/            # Результаты работы
├── state/              # Состояние процессов
└── requirements.txt    # Зависимости
```

## 🎯 Использование

### Запуск с темой "5 ошибок малого бизнеса при внедрении ИИ":

```powershell
python run.py
```

### Создание собственной задачи:

Отредактируйте файл `run.py`:

```python
task = {
    "topic": "Ваша тема здесь",
    "requirements": {
        "research": "Описание требований",
        # ...
    }
}
```

## 📊 Результаты

После запуска система создаст:

- `outputs/TASK_ID_result.json` - Полный результат работы
- `state/TASK_ID.json` - Состояние для восстановления

## 🔧 Команды

```powershell
# Запуск
python run.py

# Запуск с отладкой
python -u run.py

# Проверка конфига
python -c "from utils.config_loader import ConfigLoader; c = ConfigLoader(); print(c.agents)"
```

## 📝 Пример результата

Система вернёт JSON с всеми стадиями обработки:

```json
{
  "task_id": "uuid-123",
  "stages": {
    "research": { /* исследование */ },
    "article": { /* статья */ },
    "design": { /* дизайн */ },
    "telegram": { /* telegram пост */ },
    "editor": { /* финальная проверка */ }
  },
  "status": "completed"
}
```

## 🐛 Решение проблем

### "Имя ANTHROPIC_API_KEY не определено"
- Проверьте файл `.env`
- Убедитесь, что ключ скопирован правильно
- Перезагрузите терминал

### "ModuleNotFoundError"
- Переустановите зависимости: `pip install -r requirements.txt`
- Убедитесь, что используется правильный Python: `python --version`

### Claude не отвечает
- Проверьте интернет соединение
- Проверьте лимиты API на Anthropic Console
- Убедитесь, что API ключ актуален

## 📚 Документация

- [Anthropic API](https://docs.anthropic.com/)
- [Claude Models](https://docs.anthropic.com/claude/reference/models-overview)

## 👤 Автор

Мультиагентная система контента

## 📄 Лицензия

MIT
