# import respx # No longer needed
# from httpx import Response # No longer needed
from unittest.mock import MagicMock, patch  # Use unittest.mock

import pytest

# Import the internal logic functions and constants to be tested
# We also import the prompt function directly as before
from src.server import (
    HIREBASE_API_BASE,
    _get_job_logic,
    _search_jobs_logic,
    create_candidate_profile,
)

# Mock API base URL
BASE_URL = HIREBASE_API_BASE


@pytest.mark.asyncio
@patch("src.server.requests.get")  # Patch requests.get in the server module
async def test_search_jobs_success(mock_get, monkeypatch):
    """Test successful job search using unittest.mock."""
    monkeypatch.delenv("HIREBASE_API_KEY", raising=False)

    # Configure the mock response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"jobs": [{"id": "123", "title": "Test Job"}], "total": 1}
    # Make raise_for_status do nothing for success case
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Call the internal logic function
    result = _search_jobs_logic(q="test", limit=1)

    # Assertions
    mock_get.assert_called_once()  # Check if requests.get was called
    # Check call arguments (optional but good)
    call_args, call_kwargs = mock_get.call_args
    assert call_args[0] == f"{BASE_URL}/jobs"
    assert call_kwargs["params"] == {"q": "test", "limit": 1}

    assert "error" not in result
    assert result["total"] == 1
    assert len(result["jobs"]) == 1
    assert result["jobs"][0]["title"] == "Test Job"
    # assert search_route.calls.last.request.url.query == b'q=test&limit=1' # Respx specific


@pytest.mark.asyncio
@patch("src.server.requests.get")  # Patch requests.get
async def test_search_jobs_api_error(mock_get, monkeypatch):
    """Test job search API error using unittest.mock."""
    monkeypatch.delenv("HIREBASE_API_KEY", raising=False)

    # Configure mock response for error
    mock_response = MagicMock()
    mock_response.status_code = 500
    # Simulate requests.exceptions.HTTPError on raise_for_status()
    from requests.exceptions import HTTPError

    mock_response.raise_for_status.side_effect = HTTPError(
        "Internal Server Error", response=mock_response
    )
    mock_get.return_value = mock_response

    # Call the internal logic function
    result = _search_jobs_logic(q="test")

    mock_get.assert_called_once()
    assert "error" in result
    # The error message now comes from the caught RequestException
    assert "Internal Server Error" in result["error"]


@pytest.mark.asyncio
@patch("src.server.requests.get")  # Patch requests.get
async def test_get_job_success(mock_get, monkeypatch):
    """Test successful job retrieval using unittest.mock."""
    monkeypatch.delenv("HIREBASE_API_KEY", raising=False)
    job_id = "job123"
    mock_job_data = {"id": job_id, "title": "Specific Job", "description": "Details..."}

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = mock_job_data
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    # Call the internal logic function
    result = _get_job_logic(job_id=job_id)

    mock_get.assert_called_once()
    call_args, _ = mock_get.call_args
    assert call_args[0] == f"{BASE_URL}/jobs/{job_id}"

    assert "error" not in result
    assert result["id"] == job_id
    assert result["title"] == "Specific Job"


@pytest.mark.asyncio
@patch("src.server.requests.get")  # Patch requests.get
async def test_get_job_not_found(mock_get, monkeypatch):
    """Test job not found (404) using unittest.mock."""
    monkeypatch.delenv("HIREBASE_API_KEY", raising=False)
    job_id = "invalid_job"

    mock_response = MagicMock()
    mock_response.status_code = 404
    from requests.exceptions import HTTPError

    mock_response.raise_for_status.side_effect = HTTPError("Not Found", response=mock_response)
    mock_get.return_value = mock_response

    # Call the internal logic function
    result = _get_job_logic(job_id=job_id)

    mock_get.assert_called_once()
    assert "error" in result
    assert "Not Found" in result["error"]


# Test the prompt function (doesn't need async or mocking)
def test_create_candidate_profile():
    """Test the create_candidate_profile prompt generation."""
    # from src.server import create_candidate_profile # Already imported above

    name = "Test Candidate"
    linkedin = "linkedin.com/test"
    website = "test.com"
    resume = "Experienced professional..."

    prompt = create_candidate_profile(
        name=name, linkedin_url=linkedin, personal_website=website, resume_text=resume
    )

    assert name in prompt
    assert linkedin in prompt
    assert website in prompt
    assert resume in prompt
    assert "Based on my profile above, please:" in prompt
    assert "1. Identify key skills" in prompt
