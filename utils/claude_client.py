"""Клиент для взаимодействия с Claude API."""

import json
import logging
from typing import Dict, Any, Optional
from anthropic import Anthropic

logger = logging.getLogger(__name__)


class ClaudeClient:
    """Клиент для взаимодействия с Claude API."""

    def __init__(self, model: str = "claude-3-5-sonnet-20241022"):
        self.client = Anthropic()
        self.model = model
        self.conversation_history = []

    def send_message(
        self,
        message: str,
        system_prompt: str,
        temperature: float = 0.7,
        max_tokens: int = 2000,
        json_mode: bool = True,
    ) -> str:
        """
        Отправляет сообщение Claude и получает ответ.

        Args:
            message: Сообщение для отправки
            system_prompt: Системный промпт
            temperature: Температура ответа
            max_tokens: Максимальное количество токенов
            json_mode: Должен ли ответ быть в JSON формате

        Returns:
            Ответ от Claude
        """
        try:
            # Добавляем сообщение пользователя в историю
            self.conversation_history.append(
                {"role": "user", "content": message}
            )

            # Создаём сообщение с историей
            response = self.client.messages.create(
                model=self.model,
                max_tokens=max_tokens,
                temperature=temperature,
                system=system_prompt,
                messages=self.conversation_history,
            )

            # Извлекаем текст ответа
            assistant_message = response.content[0].text

            # Добавляем ответ в историю
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )

            logger.info(f"Получен ответ от Claude ({len(assistant_message)} символов)")
            return assistant_message

        except Exception as e:
            logger.error(f"Ошибка при обращении к Claude API: {e}")
            raise

    def parse_json_response(self, response: str) -> Dict[str, Any]:
        """
        Парсит JSON ответ из строки.

        Args:
            response: Строка с JSON ответом

        Returns:
            Распарсенный JSON
        """
        try:
            # Пытаемся найти JSON в ответе
            json_start = response.find("{")
            json_end = response.rfind("}") + 1

            if json_start != -1 and json_end > json_start:
                json_str = response[json_start:json_end]
                return json.loads(json_str)

            # Если JSON не найден, пытаемся распарсить весь ответ
            return json.loads(response)

        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            # Возвращаем ответ как есть
            return {"raw_response": response}

    def clear_history(self):
        """Очищает историю разговора."""
        self.conversation_history = []
