"""
Shared pytest fixtures and configuration for the test suite.
"""
import os
import tempfile
import pytest
from unittest.mock import Mock, MagicMock


@pytest.fixture
def temp_dir():
    """Provide a temporary directory for tests."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def temp_file():
    """Provide a temporary file for tests."""
    with tempfile.NamedTemporaryFile(mode='w+', delete=False) as tmpfile:
        yield tmpfile.name
    # Clean up
    try:
        os.unlink(tmpfile.name)
    except FileNotFoundError:
        pass


@pytest.fixture
def mock_config():
    """Provide a mock configuration object."""
    config = Mock()
    config.host = "localhost"
    config.port = 8888
    config.debug = True
    return config


@pytest.fixture
def mock_database():
    """Provide a mock database connection."""
    db = MagicMock()
    db.connect.return_value = True
    db.execute.return_value = []
    db.fetchall.return_value = []
    db.fetchone.return_value = None
    return db


@pytest.fixture
def mock_request():
    """Provide a mock HTTP request object."""
    request = Mock()
    request.method = "GET"
    request.path = "/"
    request.headers = {}
    request.body = b""
    request.arguments = {}
    return request


@pytest.fixture
def mock_response():
    """Provide a mock HTTP response object."""
    response = Mock()
    response.status_code = 200
    response.headers = {}
    response.body = ""
    return response


@pytest.fixture(autouse=True)
def clean_environment():
    """Clean environment variables before and after each test."""
    # Store original environment
    original_env = os.environ.copy()
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)


@pytest.fixture
def sample_data():
    """Provide sample data for tests."""
    return {
        "users": [
            {"id": 1, "name": "Alice", "email": "alice@example.com"},
            {"id": 2, "name": "Bob", "email": "bob@example.com"},
        ],
        "products": [
            {"id": 1, "name": "Widget", "price": 10.99},
            {"id": 2, "name": "Gadget", "price": 25.50},
        ]
    }


@pytest.fixture
def mock_tornado_application():
    """Provide a mock Tornado application for testing."""
    from unittest.mock import Mock
    app = Mock()
    app.listen = Mock()
    app.handlers = []
    return app


@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    import asyncio
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()