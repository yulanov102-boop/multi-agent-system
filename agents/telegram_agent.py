"""Telegram-агент - подготавливает контент для Telegram."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class TelegramAgent(BaseAgent):
    """Telegram-агент. Адаптирует контент для Telegram."""

    def __init__(self):
        super().__init__("telegram_agent")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Адаптирует контент для Telegram.

        Args:
            input_data: Входные данные с контентом

        Returns:
            Результат с Telegram-форматированным сообщением
        """
        article = input_data.get("article", {})
        topic = article.get("topic", "")
        title = article.get("title", "")
        sections = article.get("sections", [])

        logger.info(f"Telegram-агент: адаптирую контент для Telegram")

        # Формируем запрос для Claude
        prompt = f"""Адаптируй следующий контент специально для Telegram:

Тема: "{topic}"
Заголовок: "{title}"

Основной контент:
{json.dumps(sections, ensure_ascii=False, indent=2)}

Требования:
1. Максимум 4096 символов (подели на части если нужно)
2. Используй Markdown разметку
3. Добавь emoji для выделения
4. Сделай текст сканируемым (используй * для выделения)
5. Добавь 5-7 релевантных хештегов
6. Если контент большой, раздели на 2-3 сообщения
7. Каждое сообщение должно быть самостоятельным

Верни результат в JSON:
{{
    "message_count": 1,
    "messages": [
        {{
            "part": 1,
            "content": "Текст сообщения с Markdown разметкой...",
            "hashtags": ["#тег1", "#тег2", ...]
        }}
    ],
    "post_type": "thread или single message",
    "recommended_time": "Рекомендуемое время публикации (если релевантно)"
}}"""

        # Получаем ответ от Claude
        response = self.call_claude(prompt)

        # Парсим результат
        result = self.parse_json_response(response)
        result["agent"] = "telegram_agent"
        result["status"] = "completed"
        result["topic"] = topic

        self.log_result(result)
        return result
