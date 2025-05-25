#!/usr/bin/env python3
"""
Test script to verify the new logging configuration system works correctly.
"""
import json
import os
import sys
from pathlib import Path

# Add the app directory to the Python path so we can import our modules
sys.path.insert(0, str(Path(__file__).parent / "app"))

from app.logger.config import get_logger_config
from app.settings import RUN_ENV, RunEnv


def test_basic_config():
    """Test that basic configuration is generated correctly"""
    config = get_logger_config()
    
    # Check basic structure
    assert config["version"] == 1
    assert config["disable_existing_loggers"] is False
    assert "formatters" in config
    assert "handlers" in config
    assert "loggers" in config
    assert "root" in config
    
    # Check that console_handler exists
    assert "console_handler" in config["handlers"]
    assert config["handlers"]["console_handler"]["class"] == "logging.StreamHandler"
    
    print("✓ Basic configuration structure is correct")


def test_environment_specific_configs():
    """Test environment-specific configurations"""
    # Save original environment
    original_env_vars = {}
    env_vars_to_clear = ["GITHUB_ACTIONS", "K_SERVICE", "AWS_EXECUTION_ENV", "CONTAINER_APP_REPLICA_NAME", "CLOUD"]
    
    for var in env_vars_to_clear:
        if var in os.environ:
            original_env_vars[var] = os.environ[var]
            del os.environ[var]
    
    try:
        # Test LOCAL/Default environment
        from importlib import reload
        import app.settings
        reload(app.settings)
        config = get_logger_config()
        root_handlers = config["root"]["handlers"]
        assert root_handlers == ["console_handler"], f"Expected ['console_handler'], got {root_handlers}"
        print("✓ LOCAL environment configuration is correct")
        
        # Test AWS environment
        os.environ["AWS_EXECUTION_ENV"] = "test"
        reload(app.settings)
        config = get_logger_config()
        root_handlers = config["root"]["handlers"]
        assert "aws_handler" in root_handlers, f"AWS handler not found in {root_handlers}"
        assert "watchtower.CloudWatchLogHandler" in str(config["handlers"]["aws_handler"]["class"])
        print("✓ AWS environment configuration is correct")
        
        # Clean up AWS env var
        del os.environ["AWS_EXECUTION_ENV"]
        
        # Test GCP environment
        os.environ["K_SERVICE"] = "test-service"
        reload(app.settings)
        config = get_logger_config()
        assert "cloud_logging_formatter" in config["formatters"]
        console_handler = config["handlers"]["console_handler"]
        assert console_handler["formatter"] == "cloud_logging_formatter"
        print("✓ GCP environment configuration is correct")
        
        # Clean up GCP env var
        del os.environ["K_SERVICE"]
        
        # Test Azure environment
        os.environ["CONTAINER_APP_REPLICA_NAME"] = "test-replica"
        reload(app.settings)
        config = get_logger_config()
        root_handlers = config["root"]["handlers"]
        assert "azure_handler" in root_handlers, f"Azure handler not found in {root_handlers}"
        assert "opencensus.ext.azure.log_exporter.AzureLogHandler" in str(config["handlers"]["azure_handler"]["class"])
        print("✓ Azure environment configuration is correct")
        
    finally:
        # Restore original environment
        for var in env_vars_to_clear:
            if var in os.environ:
                del os.environ[var]
        for var, value in original_env_vars.items():
            os.environ[var] = value
        reload(app.settings)


def main():
    """Run all tests"""
    print("Testing new logging configuration system...")
    print(f"Current environment: {RUN_ENV}")
    print()
    
    test_basic_config()
    test_environment_specific_configs()
    
    print()
    print("All tests passed! ✓")
    print()
    print("Sample configuration for current environment:")
    config = get_logger_config()
    print(json.dumps(config, indent=2))


if __name__ == "__main__":
    main()