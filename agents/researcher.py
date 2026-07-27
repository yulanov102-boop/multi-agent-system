"""Исследователь - собирает информацию."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class Researcher(BaseAgent):
    """Исследователь. Собирает и проверяет информацию по теме."""

    def __init__(self):
        super().__init__("researcher")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Исследует тему и собирает информацию.

        Args:
            input_data: Входные данные с темой

        Returns:
            Результат исследования с информацией
        """
        topic = input_data.get("topic", "")
        logger.info(f"Исследователь: начинаю исследование темы '{topic}'")

        # Формируем запрос для Claude
        prompt = f"""Проведи глубокое исследование по теме: "{topic}"

Найди и структурируй следующую информацию:
1. Основные пункты/ошибки (5-7 ключевых моментов)
2. Статистика и факты (если есть)
3. Примеры из практики
4. Последствия и влияние
5. Рекомендации и решения

Верни результат в виде JSON с структурой:
{{
    "topic": "{topic}",
    "key_points": [
        {{"title": "...", "description": "...", "impact": "..."}},
        ...
    ],
    "statistics": [...],
    "case_studies": [...],
    "recommendations": [...],
    "sources": [...],
    "summary": "..."
}}"""

        # Получаем ответ от Claude
        response = self.call_claude(prompt)

        # Парсим результат
        result = self.parse_json_response(response)

        result["agent"] = "researcher"
        result["status"] = "completed"

        self.log_result(result)
        return result
