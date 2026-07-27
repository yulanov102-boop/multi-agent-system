#!/usr/bin/env python
"""
Главный скрипт для запуска мультиагента.
"""

import logging
import json
from orchestrator import Orchestrator

# Настраиваем логирование
logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def main():
    """Основная функция."""
    
    # Задача для мультиагента
    task = {
        "topic": "5 ошибок малого бизнеса при внедрении ИИ",
        "requirements": {
            "research": "Найти актуальную информацию об ошибках",
            "article": "Написать привлекательный пост",
            "design": "Подготовить концепцию картинки",
            "telegram": "Адаптировать для Telegram публикации"
        }
    }
    
    print("\n" + "="*60)
    print("🤖 МУЛЬТИАГЕНТНАЯ СИСТЕМА СОЗДАНИЯ КОНТЕНТА")
    print("="*60)
    print(f"\n📝 Тема: {task['topic']}")
    print("\n⏳ Начинаю обработку...\n")
    
    # Создаём оркестратор
    orchestrator = Orchestrator()
    
    # Запускаем рабочий процесс
    result = orchestrator.run_workflow(task)
    
    # Выводим результат
    print("\n" + "="*60)
    print("✅ РАБОЧИЙ ПРОЦЕСС ЗАВЕРШЁН")
    print("="*60)
    
    if result.get("status") == "completed":
        print("\n📊 РЕЗУЛЬТАТЫ ПО СТАДИЯМ:\n")
        
        # Исследование
        if "research" in result["stages"]:
            research = result["stages"]["research"]
            print("1️⃣ ИССЛЕДОВАНИЕ:")
            print(f"   Статус: ✅")
            if "topic" in research:
                print(f"   Тема: {research['topic']}")
            if "key_points" in research:
                print(f"   Ключевых пунктов найдено: {len(research['key_points'])}")
            print()
        
        # Статья
        if "article" in result["stages"]:
            article = result["stages"]["article"]
            print("2️⃣ СТАТЬЯ:")
            print(f"   Статус: ✅")
            if "title" in article:
                print(f"   Заголовок: {article['title'][:60]}...")
            if "sections" in article:
                print(f"   Разделов: {len(article['sections'])}")
            print()
        
        # Дизайн
        if "design" in result["stages"]:
            design = result["stages"]["design"]
            print("3️⃣ ДИЗАЙН:")
            print(f"   Статус: ✅")
            if "concept" in design:
                print(f"   Концепция: {design['concept'][:50]}...")
            if "color_palette" in design:
                print(f"   Цветовая палитра: готова")
            print()
        
        # Telegram
        if "telegram" in result["stages"]:
            telegram = result["stages"]["telegram"]
            print("4️⃣ TELEGRAM:")
            print(f"   Статус: ✅")
            if "message_count" in telegram:
                print(f"   Сообщений для публикации: {telegram['message_count']}")
            if "messages" in telegram:
                for i, msg in enumerate(telegram["messages"], 1):
                    if "hashtags" in msg:
                        print(f"   Хештеги: {len(msg['hashtags'])} найдено")
            print()
        
        # Финальная проверка
        if "editor" in result["stages"]:
            editor = result["stages"]["editor"]
            print("5️⃣ ФИНАЛЬНАЯ ПРОВЕРКА:")
            print(f"   Статус: ✅")
            if "quality_score" in editor:
                print(f"   Оценка качества: {editor['quality_score']}/10")
            if "final_approval" in editor:
                approval = "✅ Одобрено" if editor["final_approval"] else "⚠️ Требует доработки"
                print(f"   Результат: {approval}")
            print()
    else:
        print(f"\n❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")
    
    print("\n" + "="*60)
    print(f"📂 Результаты сохранены в: outputs/")
    print(f"💾 Состояние сохранено в: state/")
    print("="*60 + "\n")


if __name__ == "__main__":
    main()
