"""Tests for application configuration."""

import os
from unittest.mock import patch

from src.backend.app_config import AppConfig
from src.backend.config_kernel import Config

MOCK_ENV_VARS = {
    "COSMOSDB_ENDPOINT": "https://mock-cosmosdb.documents.azure.com:443/",
    "COSMOSDB_DATABASE": "mock_database",
    "COSMOSDB_CONTAINER": "mock_container",
    "AZURE_OPENAI_DEPLOYMENT_NAME": "mock-deployment",
    "AZURE_OPENAI_API_VERSION": "2024-05-01-preview",
    "AZURE_OPENAI_ENDPOINT": "https://mock-openai-endpoint.azure.com/",
    "AZURE_OPENAI_API_KEY": "mock-api-key",
    "AZURE_TENANT_ID": "mock-tenant-id",
    "AZURE_CLIENT_ID": "mock-client-id",
    "AZURE_CLIENT_SECRET": "mock-client-secret",
}

@patch.dict(os.environ, MOCK_ENV_VARS)
def test_get_required_config():
    cfg = AppConfig()
    assert cfg._get_required("COSMOSDB_ENDPOINT") == MOCK_ENV_VARS["COSMOSDB_ENDPOINT"]

@patch.dict(os.environ, MOCK_ENV_VARS)
def test_get_optional_config():
    cfg = AppConfig()
    assert cfg._get_optional("NON_EXISTENT_VAR", "default_value") == "default_value"
    assert cfg._get_optional("COSMOSDB_DATABASE", "default_db") == MOCK_ENV_VARS["COSMOSDB_DATABASE"]

@patch.dict(os.environ, MOCK_ENV_VARS)
def test_get_bool_config():
    cfg = AppConfig()
    with patch.dict(os.environ, {"FEATURE_ENABLED": "true"}):
        assert cfg._get_bool("FEATURE_ENABLED") is True
    with patch.dict(os.environ, {"FEATURE_ENABLED": "false"}):
        assert cfg._get_bool("FEATURE_ENABLED") is False
    with patch.dict(os.environ, {"FEATURE_ENABLED": "1"}):
        assert cfg._get_bool("FEATURE_ENABLED") is True
    with patch.dict(os.environ, {"FEATURE_ENABLED": "0"}):
        assert cfg._get_bool("FEATURE_ENABLED") is False

@patch("src.backend.app_config.DefaultAzureCredential")
@patch.dict(os.environ, MOCK_ENV_VARS)
def test_get_azure_credentials_with_env_vars(mock_default_cred):
    cfg = AppConfig()
    creds = cfg.get_azure_credentials()
    assert creds is not None
    mock_default_cred.assert_called()
