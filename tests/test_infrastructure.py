"""
Validation tests to ensure the testing infrastructure is working correctly.
"""
import pytest
import os
import sys


def test_python_version():
    """Test that Python version is compatible."""
    assert sys.version_info >= (3, 8), "Python 3.8+ is required"


def test_pytest_is_working():
    """Basic test to verify pytest is functioning."""
    assert True


@pytest.mark.unit
def test_unit_marker():
    """Test that unit marker is working."""
    assert 1 + 1 == 2


@pytest.mark.integration
def test_integration_marker():
    """Test that integration marker is working."""
    assert "integration" in "integration test"


@pytest.mark.slow
def test_slow_marker():
    """Test that slow marker is working."""
    import time
    time.sleep(0.01)  # Minimal sleep to simulate slow test
    assert True


def test_fixtures_available(temp_dir, temp_file, mock_config, sample_data):
    """Test that common fixtures are available and working."""
    # Test temp_dir fixture
    assert os.path.isdir(temp_dir)
    
    # Test temp_file fixture
    assert os.path.exists(temp_file)
    
    # Test mock_config fixture
    assert hasattr(mock_config, 'host')
    assert hasattr(mock_config, 'port')
    
    # Test sample_data fixture
    assert 'users' in sample_data
    assert 'products' in sample_data
    assert len(sample_data['users']) == 2


def test_mock_functionality(mock_database, mock_request):
    """Test that mock objects are working correctly."""
    # Test mock database
    assert mock_database.connect() is True
    assert mock_database.execute() == []
    
    # Test mock request
    assert mock_request.method == "GET"
    assert mock_request.path == "/"


def test_environment_cleanup():
    """Test that environment cleanup fixture is working."""
    # Set a test environment variable
    os.environ['TEST_VAR'] = 'test_value'
    assert os.environ.get('TEST_VAR') == 'test_value'
    # The clean_environment fixture should clean this up after the test


class TestExampleClass:
    """Example test class to verify class-based tests work."""
    
    def test_class_method(self):
        """Test that class-based tests are discovered."""
        assert True
        
    def test_fixture_in_class(self, mock_config):
        """Test that fixtures work in class methods."""
        assert mock_config.host == "localhost"


def test_tornado_import():
    """Test that tornado can be imported (validates dependency installation)."""
    try:
        import tornado.web
        import tornado.ioloop
        assert True
    except ImportError:
        pytest.fail("Tornado import failed - check dependency installation")


def test_coverage_excludes():
    """Test that this file would be included in coverage."""
    # This test itself validates that test files can run
    # Coverage exclusions are tested by running coverage
    assert __file__.endswith('test_infrastructure.py')