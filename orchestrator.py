"""
Оркестратор мультиагентной системы.
Координирует рабочий процесс агентов для создания и распространения контента.
"""

import json
import logging
from typing import Dict, Any, Optional
from pathlib import Path
import os
from dotenv import load_dotenv
from datetime import datetime
import uuid

load_dotenv()
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class Orchestrator:
    """Управляет рабочим процессом агентов и состоянием."""

    def __init__(self):
        self.state_dir = Path(os.getenv("STATE_DIR", "./state"))
        self.output_dir = Path(os.getenv("OUTPUT_DIR", "./outputs"))
        self.state_dir.mkdir(exist_ok=True)
        self.output_dir.mkdir(exist_ok=True)
        
        # Импортируем агентов
        from agents.researcher import Researcher
        from agents.copywriter import Copywriter
        from agents.designer import Designer
        from agents.telegram_agent import TelegramAgent
        from agents.editor import Editor
        
        self.agents = {
            "researcher": Researcher(),
            "copywriter": Copywriter(),
            "designer": Designer(),
            "telegram_agent": TelegramAgent(),
            "editor": Editor(),
        }

    def run_workflow(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Запускает полный рабочий процесс через всех агентов.

        Args:
            task: Задача для обработки

        Returns:
            Финальный результат после прохождения через всех агентов
        """
        task_id = task.get("id", str(uuid.uuid4()))
        task_title = task.get("topic", "Untitled")
        
        logger.info(f"╔════════════════════════════════════════╗")
        logger.info(f"║ Начинаю рабочий процесс                ║")
        logger.info(f"║ Задача: {task_title[:30]:<30} ║")
        logger.info(f"║ ID: {task_id[:34]:<34} ║")
        logger.info(f"╚════════════════════════════════════════╝")

        result = {
            "task_id": task_id,
            "task": task,
            "stages": {},
            "timestamps": {
                "start": datetime.now().isoformat()
            }
        }

        # Последовательность выполнения агентов
        workflow_order = ["researcher", "copywriter", "designer", "telegram_agent", "editor"]
        
        try:
            # Начинаем с исследователя
            logger.info(f"\n📊 СТАДИЯ 1: Исследование")
            logger.info("=" * 50)
            researcher_result = self.agents["researcher"].process(task)
            result["stages"]["research"] = researcher_result
            
            # Копирайтер пишет контент
            logger.info(f"\n✍️ СТАДИЯ 2: Создание контента")
            logger.info("=" * 50)
            copywriter_input = {
                "research": researcher_result,
                "topic": task.get("topic", "")
            }
            copywriter_result = self.agents["copywriter"].process(copywriter_input)
            result["stages"]["article"] = copywriter_result
            
            # Дизайнер создаёт визуальную концепцию
            logger.info(f"\n🎨 СТАДИЯ 3: Дизайн-концепция")
            logger.info("=" * 50)
            designer_input = {
                "article": copywriter_result,
                "topic": task.get("topic", "")
            }
            designer_result = self.agents["designer"].process(designer_input)
            result["stages"]["design"] = designer_result
            
            # Telegram-агент адаптирует контент
            logger.info(f"\n📱 СТАДИЯ 4: Telegram-адаптация")
            logger.info("=" * 50)
            telegram_input = {
                "article": copywriter_result,
                "topic": task.get("topic", "")
            }
            telegram_result = self.agents["telegram_agent"].process(telegram_input)
            result["stages"]["telegram"] = telegram_result
            
            # Финальный редактор проверяет всё
            logger.info(f"\n✅ СТАДИЯ 5: Финальная проверка")
            logger.info("=" * 50)
            editor_input = {
                "research": researcher_result,
                "article": copywriter_result,
                "design": designer_result,
                "telegram": telegram_result
            }
            editor_result = self.agents["editor"].process(editor_input)
            result["stages"]["editor"] = editor_result
            
            result["status"] = "completed"
            result["timestamps"]["end"] = datetime.now().isoformat()
            
            logger.info(f"\n✅ Рабочий процесс успешно завершён!")
            logger.info(f"╔════════════════════════════════════════╗")
            logger.info(f"║ РЕЗУЛЬТАТЫ:                            ║")
            logger.info(f"║ • Исследование: ✅                     ║")
            logger.info(f"║ • Статья: ✅                           ║")
            logger.info(f"║ • Дизайн: ✅                           ║")
            logger.info(f"║ • Telegram: ✅                         ║")
            logger.info(f"║ • Проверка: ✅                         ║")
            logger.info(f"╚════════════════════════════════════════╝")
            
        except Exception as e:
            logger.error(f"❌ Ошибка в рабочем процессе: {e}", exc_info=True)
            result["status"] = "failed"
            result["error"] = str(e)
            result["timestamps"]["error"] = datetime.now().isoformat()

        # Сохраняем результат
        self.save_state(result, task_id)
        
        return result

    def save_state(self, state: Dict[str, Any], task_id: str) -> None:
        """Сохраняет состояние в файл."""
        state_file = self.state_dir / f"{task_id}.json"
        with open(state_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)
        logger.info(f"💾 Состояние сохранено: {state_file}")
        
        # Также сохраняем в outputs для удобства
        output_file = self.output_dir / f"{task_id}_result.json"
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(state, f, ensure_ascii=False, indent=2)

    def load_state(self, task_id: str) -> Optional[Dict[str, Any]]:
        """Загружает состояние из файла."""
        state_file = self.state_dir / f"{task_id}.json"
        if state_file.exists():
            with open(state_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return None


if __name__ == "__main__":
    orchestrator = Orchestrator()
    print("✅ Оркестратор инициализирован и готов к работе")
