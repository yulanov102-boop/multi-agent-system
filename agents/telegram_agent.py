"""Telegram-агент - подготавливает и отправляет контент в Telegram."""

import json
import os
from typing import Dict, Any, List
from agents.base_agent import BaseAgent
import logging
from telegram import Bot
from telegram.error import TelegramError

logger = logging.getLogger(__name__)


class TelegramAgent(BaseAgent):
    """Telegram-агент. Адаптирует контент для Telegram и отправляет его."""

    def __init__(self):
        super().__init__("telegram_agent")
        self.bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        if self.bot_token:
            self.bot = Bot(token=self.bot_token)
        else:
            self.bot = None
            logger.warning("TELEGRAM_BOT_TOKEN не установлен")

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

    def send_to_telegram(self, telegram_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Отправляет подготовленные сообщения в Telegram.

        Args:
            telegram_data: Данные с сообщениями от process()

        Returns:
            Результат отправки
        """
        if not self.bot:
            logger.error("Telegram бот не инициализирован")
            return {"status": "failed", "error": "Telegram bot token not set"}

        if not self.chat_id:
            logger.error("TELEGRAM_CHAT_ID не установлен")
            return {"status": "failed", "error": "TELEGRAM_CHAT_ID not set"}

        try:
            messages = telegram_data.get("messages", [])
            sent_messages = []

            logger.info(f"Отправляю {len(messages)} сообщение(я) в Telegram...")

            for i, msg in enumerate(messages, 1):
                content = msg.get("content", "")
                if not content:
                    logger.warning(f"Сообщение {i} пусто, пропускаю")
                    continue

                try:
                    # Отправляем сообщение с Markdown разметкой
                    sent_msg = self.bot.send_message(
                        chat_id=self.chat_id,
                        text=content,
                        parse_mode="Markdown",
                        disable_web_page_preview=False
                    )

                    sent_messages.append({
                        "part": i,
                        "message_id": sent_msg.message_id,
                        "status": "sent",
                        "timestamp": sent_msg.date.isoformat() if sent_msg.date else None
                    })

                    logger.info(f"✅ Сообщение {i} отправлено (ID: {sent_msg.message_id})")

                except TelegramError as e:
                    logger.error(f"❌ Ошибка при отправке сообщения {i}: {e}")
                    sent_messages.append({
                        "part": i,
                        "status": "failed",
                        "error": str(e)
                    })

            result = {
                "agent": "telegram_agent",
                "action": "send_to_telegram",
                "status": "completed" if sent_messages else "failed",
                "messages_sent": len([m for m in sent_messages if m.get("status") == "sent"]),
                "total_messages": len(messages),
                "sent_messages": sent_messages
            }

            self.log_result(result)
            return result

        except Exception as e:
            logger.error(f"❌ Критическая ошибка при отправке в Telegram: {e}")
            return {
                "status": "failed",
                "error": str(e),
                "agent": "telegram_agent"
            }
