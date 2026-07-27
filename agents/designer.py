"""Дизайнер - создаёт визуальные концепции."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class Designer(BaseAgent):
    """Дизайнер. Создаёт концепции визуальных активов."""

    def __init__(self):
        super().__init__("designer")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создаёт концепцию изображения.

        Args:
            input_data: Входные данные с контентом

        Returns:
            Результат с описанием визуальной концепции
        """
        article = input_data.get("article", {})
        topic = article.get("topic", "")
        title = article.get("title", "")

        logger.info(f"Дизайнер: создаю визуальную концепцию")

        # Формируем запрос для Claude
        prompt = f"""Создай концепцию привлекательного изображения для публикации:

Тема: "{topic}"
Заголовок: "{title}"

Требования к изображению:
1. Современный, привлекательный дизайн
2. Соответствие теме про ИИ и бизнес
3. Визуальная иерархия информации
4. Цветовая палитра (профессиональная)
5. Читаемость и контрастность

Верни детальное описание визуальной концепции в JSON:
{{
    "concept": "Название/описание концепции",
    "theme": "Основная тема визуала",
    "color_palette": {{
        "primary": "#XXXXXX",
        "secondary": "#XXXXXX",
        "accent": "#XXXXXX",
        "background": "#XXXXXX",
        "text": "#XXXXXX"
    }},
    "composition": "Описание композиции...",
    "elements": [
        "...",
        "...",
        "..."
    ],
    "typography": {{
        "title_style": "...",
        "body_style": "..."
    }},
    "key_visual": "Описание ключевого визуального элемента",
    "implementation_notes": "Рекомендации для дизайнера/художника",
    "file_format": "PNG или JPG",
    "recommended_size": "1200x630px (для соцсетей)"
}}"""

        # Получаем ответ от Claude
        response = self.call_claude(prompt)

        # Парсим результат
        result = self.parse_json_response(response)
        result["agent"] = "designer"
        result["status"] = "completed"
        result["topic"] = topic

        self.log_result(result)
        return result
