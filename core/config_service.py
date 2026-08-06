import json

from pathlib import Path

from models.app_config import AppConfig

from models.app_config import BackupTask


class ConfigService:

    CONFIG_FILE = Path("settings.json")


    @classmethod
    def load(cls) -> AppConfig:

        if not cls.CONFIG_FILE.exists():

            return AppConfig()

        with open(cls.CONFIG_FILE, "r", encoding="utf8") as f:

            data = json.load(f)

        tasks = []

        for task in data["tasks"]:

            tasks.append(

                BackupTask(

                    enabled=task["enabled"],

                    source_folder=task["source_folder"],

                    destination_folder=task["destination_folder"],

                    execution_time=task["execution_time"]

                )

            )

        config = AppConfig(

            version=data["version"],

            language=data["language"],

            theme=data["theme"],

            auto_run=data["auto_run"],

            tasks=tasks

        )

        return config


    @classmethod

    def save(cls, config: AppConfig):

        data = {

            "version": config.version,

            "language": config.language,

            "theme": config.theme,

            "auto_run": config.auto_run,

            "tasks": []

        }

        for task in config.tasks:

            data["tasks"].append({

                "enabled": task.enabled,

                "source_folder": task.source_folder,

                "destination_folder": task.destination_folder,

                "execution_time": task.execution_time

            })

        with open(cls.CONFIG_FILE, "w", encoding="utf8") as f:

            json.dump(data, f, indent=4, ensure_ascii=False)