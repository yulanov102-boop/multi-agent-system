"""Финальный редактор - проверяет качество контента."""

import json
from typing import Dict, Any
from agents.base_agent import BaseAgent
import logging

logger = logging.getLogger(__name__)


class Editor(BaseAgent):
    """Финальный редактор. Проверяет качество и консистентность."""

    def __init__(self):
        super().__init__("editor")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Проверяет и одобряет весь контент.

        Args:
            input_data: Входные данные со всеми компонентами

        Returns:
            Финальный одобренный результат
        """
        research = input_data.get("research", {})
        article = input_data.get("article", {})
        design = input_data.get("design", {})
        telegram = input_data.get("telegram", {})

        logger.info(f"Финальный редактор: проверяю весь контент")

        # Формируем запрос для Claude
        prompt = f"""Ты главный редактор. Проверь весь контент на качество:

Исследование:
{json.dumps(research, ensure_ascii=False, indent=2)}

Статья:
{json.dumps(article, ensure_ascii=False, indent=2)}

Дизайн-концепция:
{json.dumps(design, ensure_ascii=False, indent=2)}

Telegram контент:
{json.dumps(telegram, ensure_ascii=False, indent=2)}

Проверь:
1. ✅ Грамотность и стилистика
2. ✅ Консистентность информации
3. ✅ Соответствие теме
4. ✅ Качество и глубина контента
5. ✅ Актуальность и полезность
6. ✅ Единство стиля
7. ✅ Отсутствие ошибок и опечаток

Верни результат в JSON:
{{
    "status": "approved или needs_revision",
    "quality_score": "1-10",
    "checklist": {{
        "grammar": true/false,
        "consistency": true/false,
        "relevance": true/false,
        "quality": true/false,
        "completeness": true/false
    }},
    "notes": "Замечания редактора",
    "recommendations": ["...", "..."],
    "final_approval": true/false,
    "summary": "Краткое резюме качества контента"
}}"""

        # Получаем ответ от Claude
        response = self.call_claude(prompt)

        # Парсим результат
        result = self.parse_json_response(response)
        result["agent"] = "editor"
        result["status"] = "completed"

        self.log_result(result)
        return result
