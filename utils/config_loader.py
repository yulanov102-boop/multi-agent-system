"""Загрузчик конфигурации."""

import yaml
import logging
from typing import Dict, Any
from pathlib import Path

logger = logging.getLogger(__name__)


class ConfigLoader:
    """Загружает и управляет конфигурацией системы."""

    def __init__(self, config_dir: str = "./config"):
        self.config_dir = Path(config_dir)
        self.settings = {}
        self.agents = {}
        self._load_configs()

    def _load_configs(self):
        """Загружает все конфиги."""
        self._load_settings()
        self._load_agents()

    def _load_settings(self):
        """Загружает settings.yaml."""
        settings_file = self.config_dir / "settings.yaml"
        if settings_file.exists():
            with open(settings_file, "r", encoding="utf-8") as f:
                self.settings = yaml.safe_load(f) or {}
            logger.info(f"Конфиг settings загружен из {settings_file}")
        else:
            logger.warning(f"Файл settings не найден: {settings_file}")

    def _load_agents(self):
        """Загружает agents.yaml."""
        agents_file = self.config_dir / "agents.yaml"
        if agents_file.exists():
            with open(agents_file, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f) or {}
            self.agents = config.get("agents", {})
            self.workflow_order = config.get("workflow_order", [])
            logger.info(f"Конфиг agents загружен из {agents_file}")
        else:
            logger.warning(f"Файл agents не найден: {agents_file}")

    def get_agent_config(self, agent_name: str) -> Dict[str, Any]:
        """
        Получает конфиг агента.

        Args:
            agent_name: Имя агента

        Returns:
            Конфиг агента
        """
        return self.agents.get(agent_name, {})

    def get_setting(self, key: str, default: Any = None) -> Any:
        """
        Получает значение настройки.

        Args:
            key: Ключ настройки (поддерживает точечную нотацию: 'anthropic.model')
            default: Значение по умолчанию

        Returns:
            Значение настройки
        """
        keys = key.split(".")
        value = self.settings

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    def get_workflow_order(self) -> list:
        """Получает порядок выполнения агентов."""
        return getattr(self, "workflow_order", [])
