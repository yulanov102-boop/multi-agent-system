"""Дизайнер - создаёт визуальные концепции и генерирует изображения через DALL-E 3."""

import json
import os
import logging
from typing import Dict, Any
from pathlib import Path
from agents.base_agent import BaseAgent
from openai import OpenAI

logger = logging.getLogger(__name__)


class Designer(BaseAgent):
    """Дизайнер. Создаёт концепции и генерирует изображения через DALL-E 3."""

    def __init__(self):
        super().__init__("designer")
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.dalle_model = os.getenv("DALLE_MODEL", "dall-e-3")
        self.dalle_size = os.getenv("DALLE_SIZE", "1024x1024")
        self.dalle_quality = os.getenv("DALLE_QUALITY", "standard")

    def process(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Создаёт визуальную концепцию и генерирует изображение через DALL-E 3.

        Args:
            input_data: Входные данные с контентом

        Returns:
            Результат с описанием концепции и путём к сгенерированному изображению
        """
        article = input_data.get("article", {})
        topic = article.get("topic", "")
        title = article.get("title", "")

        logger.info(f"Дизайнер: создаю визуальную концепцию для '{title}'")

        # Шаг 1: Создаём концепцию через Claude
        concept = self._create_concept(topic, title)

        # Шаг 2: Генерируем изображение через DALL-E 3
        image_path = self._generate_image_dalle(concept, topic, title)

        result = {
            "agent": "designer",
            "status": "completed",
            "topic": topic,
            "title": title,
            "concept": concept,
            "image_path": image_path,
            "image_url": None,
        }

        self.log_result(result)
        return result

    def _create_concept(self, topic: str, title: str) -> Dict[str, Any]:
        """Создаёт концепцию изображения через Claude."""
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
    "key_visual": "Описание ключевого визуального элемента",
    "implementation_notes": "Рекомендации для дизайнера/художника"
}}"""

        response = self.call_claude(prompt)
        return self.parse_json_response(response)

    def _generate_image_dalle(self, concept: Dict[str, Any], topic: str, title: str) -> str:
        """Генерирует изображение через DALL-E 3 и сохраняет локально."""
        try:
            logger.info("Генерирую изображение через DALL-E 3...")

            # Создаём детальный промпт для DALL-E на основе концепции
            dalle_prompt = self._build_dalle_prompt(concept, topic, title)

            # Вызываем DALL-E 3
            response = self.openai_client.images.generate(
                model=self.dalle_model,
                prompt=dalle_prompt,
                size=self.dalle_size,
                quality=self.dalle_quality,
                n=1,
            )

            image_url = response.data[0].url

            # Скачиваем и сохраняем изображение локально
            image_path = self._download_and_save_image(image_url, topic)

            logger.info(f"Изображение успешно сгенерировано и сохранено: {image_path}")
            return image_path

        except Exception as e:
            logger.error(f"Ошибка при генерации изображения: {e}")
            raise

    def _build_dalle_prompt(self, concept: Dict[str, Any], topic: str, title: str) -> str:
        """Создаёт оптимальный промпт для DALL-E 3."""
        elements = ", ".join(concept.get("elements", []))
        key_visual = concept.get("key_visual", "")
        color_info = concept.get("color_palette", {})

        prompt = f"""Создай профессиональное и привлекательное изображение:

Название: {title}
Концепция: {concept.get('concept', '')}
Тема: {topic}

Ключевые элементы: {elements}
Главный визуальный элемент: {key_visual}

Цветовая палитра:
- Основной цвет: {color_info.get('primary', '#1F2937')}
- Вторичный: {color_info.get('secondary', '#3B82F6')}
- Акцент: {color_info.get('accent', '#10B981')}

Стиль: современный, профессиональный дизайн с высоким качеством
Разрешение: 1024x1024 пиксела
Формат: цифровой дизайн, готовый для интернета и соцсетей"""

        return prompt

    def _download_and_save_image(self, image_url: str, topic: str) -> str:
        """Скачивает изображение и сохраняет локально."""
        import requests
        from datetime import datetime

        try:
            # Создаём директорию для изображений
            images_dir = Path("outputs/images")
            images_dir.mkdir(parents=True, exist_ok=True)

            # Генерируем имя файла
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            safe_topic = topic.replace(" ", "_").replace("/", "_")[:30]
            filename = f"dalle_{safe_topic}_{timestamp}.png"
            filepath = images_dir / filename

            # Скачиваем изображение
            response = requests.get(image_url, timeout=30)
            response.raise_for_status()

            # Сохраняем файл
            with open(filepath, "wb") as f:
                f.write(response.content)

            logger.info(f"Изображение сохранено: {filepath}")
            return str(filepath)

        except Exception as e:
            logger.error(f"Ошибка при сохранении изображения: {e}")
            raise
