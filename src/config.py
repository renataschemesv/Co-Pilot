import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    @staticmethod
    def mysql_config() -> dict[str, str]:
        return {
            "host": os.getenv("MYSQL_HOST", "localhost"),
            "port": os.getenv("MYSQL_PORT", "3306"),
            "user": os.getenv("MYSQL_USER", "root"),
            "password": os.getenv("MYSQL_PASSWORD", ""),
            "database": os.getenv("MYSQL_DB", "ifc_achados_perdidos"),
        }

    @staticmethod
    def database_url() -> str:
        if os.getenv("APP_ENV", "development").lower() == "production":
            cfg = Settings.mysql_config()
            password = quote_plus(cfg["password"])
            return (
                f"mysql+pymysql://{cfg['user']}:{password}@{cfg['host']}:{cfg['port']}/"
                f"{cfg['database']}"
            )

        return f"sqlite:///{BASE_DIR / 'ifc_achados_perdidos.db'}"
