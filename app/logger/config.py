from typing import Any, Dict

from app.settings import RUN_ENV, RunEnv


def get_base_config() -> Dict[str, Any]:
    """共通のログ設定を返す"""
    return {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s"
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "simple"
            }
        },
        "loggers": {
            "app": {
                "level": "DEBUG"
            },
            "__main__": {
                "level": "DEBUG"
            }
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console_handler"]
        }
    }


def get_aws_config_overrides() -> Dict[str, Any]:
    """AWS環境固有のログ設定オーバーライド"""
    return {
        "handlers": {
            "aws_handler": {
                "class": "watchtower.CloudWatchLogHandler",
                "level": "DEBUG",
                "log_group_name": "/application",
                "log_stream_name": "python",
                "send_interval": 10,
                "formatter": "simple",
                "create_log_group": False
            }
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console_handler", "aws_handler"]
        }
    }


def get_azure_config_overrides() -> Dict[str, Any]:
    """Azure環境固有のログ設定オーバーライド"""
    return {
        "handlers": {
            "azure_handler": {
                "class": "opencensus.ext.azure.log_exporter.AzureLogHandler",
                "level": "DEBUG",
                "formatter": "simple"
            }
        },
        "root": {
            "level": "WARNING",
            "handlers": ["console_handler", "azure_handler"]
        }
    }


def get_gcp_config_overrides() -> Dict[str, Any]:
    """GCP環境固有のログ設定オーバーライド"""
    return {
        "formatters": {
            "cloud_logging_formatter": {
                "class": "app.logger.formatter.CloudLoggingFormatter"
            }
        },
        "handlers": {
            "console_handler": {
                "class": "logging.StreamHandler",
                "level": "DEBUG",
                "formatter": "cloud_logging_formatter"
            }
        }
    }


def merge_config(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """設定辞書を再帰的にマージする"""
    result = base.copy()
    
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = merge_config(result[key], value)
        else:
            result[key] = value
    
    return result


def get_logger_config() -> Dict[str, Any]:
    """実行環境に応じたログ設定を生成する"""
    base_config = get_base_config()
    
    match RUN_ENV:
        case RunEnv.AWS:
            overrides = get_aws_config_overrides()
        case RunEnv.AZURE:
            overrides = get_azure_config_overrides()
        case RunEnv.GCP:
            overrides = get_gcp_config_overrides()
        case _:  # LOCAL, GITHUB_ACTIONS, or any other environment
            overrides = {}
    
    return merge_config(base_config, overrides)