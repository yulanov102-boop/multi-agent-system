#!/usr/bin/env python
"""
Главный скрипт для запуска мультиагента.
"""

import logging
import json
import argparse
import sys
from orchestrator import Orchestrator

# Настраиваем логирование
logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def print_banner():
    """Выводит заголовок приложения."""
    print("\n" + "="*60)
    print("🤖 МУЛЬТИАГЕНТНАЯ СИСТЕМА СОЗДАНИЯ КОНТЕНТА")
    print("="*60)


def list_results(orchestrator):
    """Выводит список доступных результатов."""
    print_banner()
    print("\n📋 ДОСТУПНЫЕ РЕЗУЛЬТАТЫ:\n")

    results = orchestrator.list_results()
    if not results:
        print("   Результатов не найдено")
        return

    for i, result in enumerate(results, 1):
        status_emoji = "✅" if result["status"] == "completed" else "⚠️"
        posted_emoji = "📤" if result.get("posted") else "⏳"
        print(f"{i}. {status_emoji} {result['topic'][:40]}")
        print(f"   ID: {result['task_id']}")
        print(f"   Статус: {result['status']} {posted_emoji}")
        if result.get("posted"):
            print(f"   Отправлено: {result['posted']}")
        print()


def post_to_telegram_cmd(orchestrator, task_id):
    """Отправляет результат в Telegram."""
    print_banner()
    print(f"\n📱 Отправляю в Telegram...\n")

    result = orchestrator.post_to_telegram(task_id)

    if result.get("status") == "completed":
        messages_sent = result.get("messages_sent", 0)
        print(f"✅ Успешно отправлено {messages_sent} сообщение(й)!")
        for msg in result.get("sent_messages", []):
            if msg.get("status") == "sent":
                print(f"   • Сообщение {msg.get('part')} (ID: {msg.get('message_id')})")
    else:
        print(f"❌ Ошибка: {result.get('error', 'Неизвестная ошибка')}")

    print()


def post_last(orchestrator):
    """Отправляет последний результат в Telegram."""
    results = orchestrator.list_results()
    if not results:
        print("❌ Результатов не найдено")
        return

    # Берём первый (последний по времени) результат, который ещё не отправлен
    for result in results:
        if not result.get("posted"):
            post_to_telegram_cmd(orchestrator, result["task_id"])
            return

    # Если все отправлены, берём самый свежий
    post_to_telegram_cmd(orchestrator, results[0]["task_id"])


def run_workflow():
    """Запускает полный рабочий процесс."""

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

    print_banner()
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


def main():
    """Основная функция с обработкой аргументов."""
    parser = argparse.ArgumentParser(
        description="Мультиагентная система создания контента",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:
  python run.py                           # Запустить полный цикл обработки
  python run.py --list                    # Показать доступные результаты
  python run.py --post <task_id>          # Отправить результат в Telegram
  python run.py --post-last               # Отправить последний результат
        """
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="Показать список доступных результатов для постинга"
    )
    parser.add_argument(
        "--post",
        metavar="TASK_ID",
        help="Отправить результат в Telegram по ID задачи"
    )
    parser.add_argument(
        "--post-last",
        action="store_true",
        help="Отправить последний результат в Telegram"
    )

    args = parser.parse_args()

    orchestrator = Orchestrator()

    # Обработка команд
    if args.list:
        list_results(orchestrator)
    elif args.post:
        post_to_telegram_cmd(orchestrator, args.post)
    elif args.post_last:
        post_last(orchestrator)
    else:
        # По умолчанию - запустить полный рабочий процесс
        run_workflow()


if __name__ == "__main__":
    main()
