"""Копирайтер - создаёт контент."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class Copywriter(BaseAgent):
    """Копирайтер. Создаёт привлекательный контент."""

    def __init__(self):
        super().__init__("copywriter")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создаёт пост на основе исследований.

        Args:
            input_data: Входные данные с исследованиями

        Returns:
            Результат с текстом поста
        """
        research = input_data.get("research", {})
        topic = research.get("topic", "")

        logger.info(f"Копирайтер: создаю контент на основе исследования")

        # Подготавливаем информацию для копирайтера
        key_points = research.get("key_points", [])
        statistics = research.get("statistics", [])

        # Формируем запрос для Claude
        prompt = f"""На основе следующей информации создай привлекательный блог-пост:

Тема: "{topic}"

Ключевые пункты:
{json.dumps(key_points, ensure_ascii=False, indent=2)}

Статистика:
{json.dumps(statistics, ensure_ascii=False, indent=2)}

Требования к посту:
1. Привлекательный, цепляющий заголовок
2. Интригующее вступление (2-3 предложения)
3. Основной контент с разбором каждого пункта (в стиле блог-поста)
4. Практические рекомендации
5. Выводы
6. Призыв к действию

Стиль: профессиональный, но доступный. Используй данные и примеры.

Верни результат в виде JSON:
{{
    "title": "Привлекательный заголовок",
    "intro": "Вступление...",
    "sections": [
        {{"title": "...", "content": "..."}},
        ...
    ],
    "recommendations": ["...", "..."],
    "conclusion": "...",
    "cta": "Призыв к действию..."
}}"""

        # Получаем ответ от Claude
        response = self.call_claude(prompt)

        # Парсим результат
        result = self.parse_json_response(response)
        result["agent"] = "copywriter"
        result["status"] = "completed"
        result["topic"] = topic

        self.log_result(result)
        return result
