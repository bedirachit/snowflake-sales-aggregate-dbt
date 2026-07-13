"""Shared configuration for pipeline scripts."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
load_dotenv(PROJECT_ROOT / ".env")


def env(key: str, default: str = "") -> str:
    return os.getenv(key, default)


def snowflake_connect_kwargs() -> dict:
    account = env("SNOWFLAKE_ACCOUNT")
    if not account:
        raise ValueError("SNOWFLAKE_ACCOUNT is required in .env")
    return {
        "account": account,
        "user": env("SNOWFLAKE_USER"),
        "password": env("SNOWFLAKE_PASSWORD"),
        "warehouse": env("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH"),
        "role": env("SNOWFLAKE_ROLE", "ACCOUNTADMIN"),
        "database": env("SNOWFLAKE_DATABASE", "DEMO_DB"),
        "schema": env("SNOWFLAKE_SCHEMA", "DEMO_SCHEMA"),
    }


def sql_path(*parts: str) -> Path:
    return PROJECT_ROOT / "pipeline" / "sql" / Path(*parts)


def data_path(*parts: str) -> Path:
    return PROJECT_ROOT / "pipeline" / "data" / Path(*parts)


DBT_PROJECT_DIR = PROJECT_ROOT / "pipeline" / "dbt"
DBT_MODEL = DBT_PROJECT_DIR / "models" / "marts" / "sales_summary.sql"
DBT_MODEL_SELECT = "sales_summary"


def dbt_env() -> dict[str, str]:
    """Environment for dbt CLI with Snowflake creds from .env."""
    merged = os.environ.copy()
    load_dotenv(PROJECT_ROOT / ".env", override=True)
    merged.update(
        {
            k: v
            for k, v in os.environ.items()
            if k.startswith("SNOWFLAKE_")
        }
    )
    merged["DBT_PROFILES_DIR"] = str(DBT_PROJECT_DIR)
    return merged

