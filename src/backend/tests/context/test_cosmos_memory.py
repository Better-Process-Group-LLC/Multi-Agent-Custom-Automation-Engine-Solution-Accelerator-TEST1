import os
import sys
import pytest
from unittest.mock import AsyncMock, patch
from azure.cosmos.partition_key import PartitionKey

# Provide minimal environment variables required during import
os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://mock-openai-endpoint")
os.environ.setdefault("AZURE_OPENAI_API_VERSION", "2023-01-01")
os.environ.setdefault("AZURE_OPENAI_DEPLOYMENT_NAME", "mock-deployment-name")
os.environ.setdefault("COSMOSDB_ENDPOINT", "https://mock-endpoint")
os.environ.setdefault("COSMOSDB_KEY", "mock-key")
os.environ.setdefault("COSMOSDB_DATABASE", "mock-database")
os.environ.setdefault("COSMOSDB_CONTAINER", "mock-container")
os.environ.setdefault("AZURE_AI_SUBSCRIPTION_ID", "dummy-subscription")
os.environ.setdefault("AZURE_AI_RESOURCE_GROUP", "dummy-rg")
os.environ.setdefault("AZURE_AI_PROJECT_NAME", "dummy-project")
os.environ.setdefault("AZURE_AI_AGENT_ENDPOINT", "https://dummy-endpoint")

# Ensure src/backend is on the Python path for imports
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from src.backend.context.cosmos_memory_kernel import CosmosMemoryContext


# Helper to create async iterable
async def async_iterable(mock_items):
    """Helper to create an async iterable."""
    for item in mock_items:
        yield item


@pytest.fixture
def mock_env_variables(monkeypatch):
    """Mock all required environment variables."""
    env_vars = {
        "COSMOSDB_ENDPOINT": "https://mock-endpoint",
        "COSMOSDB_KEY": "mock-key",
        "COSMOSDB_DATABASE": "mock-database",
        "COSMOSDB_CONTAINER": "mock-container",
        "AZURE_OPENAI_DEPLOYMENT_NAME": "mock-deployment-name",
        "AZURE_OPENAI_API_VERSION": "2023-01-01",
        "AZURE_OPENAI_ENDPOINT": "https://mock-openai-endpoint",
    }
    for key, value in env_vars.items():
        monkeypatch.setenv(key, value)


@pytest.fixture
def mock_cosmos_client():
    """Fixture for mocking Cosmos DB client and container."""
    mock_client = AsyncMock()
    mock_container = AsyncMock()
    mock_client.create_container_if_not_exists.return_value = mock_container

    # Mocking context methods
    mock_context = AsyncMock()
    mock_context.store_message = AsyncMock()
    mock_context.retrieve_messages = AsyncMock(
        return_value=async_iterable([{"id": "test_id", "content": "test_content"}])
    )

    return mock_client, mock_container, mock_context


@pytest.fixture
def mock_config(mock_cosmos_client):
    """Fixture to patch Config with mock Cosmos DB client."""
    mock_client, _, _ = mock_cosmos_client
    with patch(
        "src.backend.config_kernel.Config.COSMOSDB_CONTAINER", "mock-container"
    ), patch(
        "src.backend.context.cosmos_memory_kernel.CosmosClient"
    ) as MockCosmosClient, patch(
        "src.backend.context.cosmos_memory_kernel.DefaultAzureCredential"
    ):
        MockCosmosClient.return_value.get_database_client.return_value = mock_client
        yield


@pytest.mark.asyncio
async def test_initialize(mock_config, mock_cosmos_client):
    """Test if the Cosmos DB container is initialized correctly."""
    mock_client, mock_container, _ = mock_cosmos_client
    context = CosmosMemoryContext(
        session_id="test_session", user_id="test_user"
    )
    await context.initialize()
    mock_client.create_container_if_not_exists.assert_called_once_with(
        id="mock-container", partition_key=PartitionKey(path="/session_id")
    )
    assert context._container == mock_container
