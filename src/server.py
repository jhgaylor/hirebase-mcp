import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from mcp.server.fastmcp import FastMCP

# Create a FastMCP server instance named "Hirebase"
mcp = FastMCP("Hirebase")

# HireBase API configuration
HIREBASE_API_BASE = "https://data.hirebase.org/v0"
HIREBASE_API_KEY = os.getenv("HIREBASE_API_KEY")


def get_hirebase_headers():
    """Get headers for HireBase API requests"""
    headers = {"Content-Type": "application/json"}
    if HIREBASE_API_KEY:
        headers["x-api-key"] = HIREBASE_API_KEY
    return headers


@dataclass
class JobSearchParams:
    """Parameters for job search"""

    q: Optional[str] = None
    and_keywords: Optional[List[str]] = None
    or_keywords: Optional[List[str]] = None
    not_keywords: Optional[List[str]] = None
    title: Optional[List[str]] = None
    category: Optional[List[str]] = None
    country: Optional[List[str]] = None
    region: Optional[List[str]] = None
    city: Optional[List[str]] = None
    location_type: Optional[List[str]] = None
    company: Optional[List[str]] = None
    industry: Optional[List[str]] = None
    company_size_from: Optional[int] = None
    company_size_to: Optional[int] = None
    years_from: Optional[int] = None
    years_to: Optional[int] = None
    salary_from: Optional[float] = None
    salary_to: Optional[float] = None
    salary_currency: Optional[str] = None
    salary_period: Optional[str] = None
    visa: Optional[bool] = None
    days: Optional[int] = None
    expired: Optional[bool] = None
    limit: Optional[int] = None
    offset: Optional[int] = None

    def to_params(self) -> Dict[str, Any]:
        """Convert to API parameters"""
        params = {}
        if self.q:
            params["q"] = self.q
        if self.and_keywords:
            params["and"] = self.and_keywords
        if self.or_keywords:
            params["or"] = self.or_keywords
        if self.not_keywords:
            params["not"] = self.not_keywords
        if self.title:
            params["title"] = self.title
        if self.category:
            params["category"] = self.category
        if self.country:
            params["country"] = self.country
        if self.region:
            params["region"] = self.region
        if self.city:
            params["city"] = self.city
        if self.location_type:
            params["locationType"] = self.location_type
        if self.company:
            params["company"] = self.company
        if self.industry:
            params["industry"] = self.industry
        if self.company_size_from is not None:
            params["companySizeFrom"] = self.company_size_from
        if self.company_size_to is not None:
            params["companySizeTo"] = self.company_size_to
        if self.years_from is not None:
            params["yearsFrom"] = self.years_from
        if self.years_to is not None:
            params["yearsTo"] = self.years_to
        if self.salary_from is not None:
            params["salaryFrom"] = self.salary_from
        if self.salary_to is not None:
            params["salaryTo"] = self.salary_to
        if self.salary_currency:
            params["salaryCurrency"] = self.salary_currency
        if self.salary_period:
            params["salaryPeriod"] = self.salary_period
        if self.visa is not None:
            params["visa"] = self.visa
        if self.days is not None:
            params["days"] = self.days
        if self.expired is not None:
            params["expired"] = self.expired
        if self.limit is not None:
            params["limit"] = self.limit
        if self.offset is not None:
            params["offset"] = self.offset
        return params


def _search_jobs_logic(**kwargs) -> Dict[str, Any]:
    """Internal logic for searching jobs via HireBase API."""
    print("--- DEBUG: Entering _search_jobs_logic ---")
    try:
        # Create JobSearchParams from kwargs
        kwargs_copy = kwargs.copy()
        if "query" in kwargs_copy:
            kwargs_copy["q"] = kwargs_copy.pop("query")

        search_params_obj = JobSearchParams(**kwargs_copy)

        response = requests.get(
            f"{HIREBASE_API_BASE}/jobs",
            headers=get_hirebase_headers(),
            params=search_params_obj.to_params(),
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        # Log the error or handle it as needed
        # print(f"HireBase API Error: {e}") # Example logging
        return {"error": str(e)}
    except TypeError as e:
        # Handle cases where kwargs don't match JobSearchParams
        return {"error": f"Invalid search parameter: {e}"}


@mcp.tool()
def search_jobs(
    query: Optional[str] = None,
    and_keywords: Optional[List[str]] = None,
    or_keywords: Optional[List[str]] = None,
    not_keywords: Optional[List[str]] = None,
    title: Optional[List[str]] = None,
    category: Optional[List[str]] = None,
    country: Optional[List[str]] = None,
    city: Optional[List[str]] = None,
    location_type: Optional[List[str]] = None,
    company: Optional[List[str]] = None,
    salary_from: Optional[float] = None,
    salary_to: Optional[float] = None,
    salary_currency: Optional[str] = None,
    years_from: Optional[int] = None,
    years_to: Optional[int] = None,
    visa: Optional[bool] = None,
    limit: Optional[int] = 10,
) -> Dict[str, Any]:
    """Search for jobs using the HireBase API

    Args:
        query: Full text search query
        and_keywords: Keywords that must all appear in results
        or_keywords: Keywords where at least one must appear
        not_keywords: Keywords that must not appear
        title: Job titles to search for
        category: Job categories to filter by
        country: Countries to filter by
        city: Cities to filter by
        location_type: Location types (Remote, In-Person, Hybrid)
        company: Companies to filter by
        salary_from: Minimum salary
        salary_to: Maximum salary
        salary_currency: Salary currency (e.g. USD)
        years_from: Minimum years of experience
        years_to: Maximum years of experience
        visa: Whether job offers visa sponsorship
        limit: Maximum number of results to return
    """
    # Pass all arguments to the internal logic function
    # Use locals() to capture all passed arguments
    args = locals()
    return _search_jobs_logic(**args)


def _get_job_logic(job_id: str) -> Dict[str, Any]:
    """Internal logic for retrieving a specific job via HireBase API."""
    try:
        response = requests.get(
            f"{HIREBASE_API_BASE}/jobs/{job_id}", headers=get_hirebase_headers()
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        # Log the error or handle it as needed
        # print(f"HireBase API Error: {e}") # Example logging
        return {"error": str(e)}


@mcp.tool()
def get_job(job_id: str) -> Dict[str, Any]:
    """Get detailed information about a specific job

    Args:
        job_id: The unique identifier of the job
    """
    return _get_job_logic(job_id=job_id)


@mcp.prompt()
def create_candidate_profile(
    name: str,
    linkedin_url: Optional[str] = None,
    personal_website: Optional[str] = None,
    resume_text: Optional[str] = None,
) -> str:
    """Create a prompt to help search for jobs based on candidate profile

    Args:
        name: The candidate's name
        linkedin_url: URL to candidate's LinkedIn profile
        personal_website: URL to candidate's personal website/portfolio
        resume_text: Text content from candidate's resume
    """
    prompt_parts = [
        f"I am {name}, a job seeker looking for relevant opportunities.",
    ]

    if linkedin_url:
        prompt_parts.append(f"My LinkedIn profile is available at: {linkedin_url}")

    if personal_website:
        prompt_parts.append(f"My personal website/portfolio is: {personal_website}")

    if resume_text:
        prompt_parts.append("\nHere is my resume content:")
        prompt_parts.append(resume_text)

    prompt_parts.append("\nBased on my profile above, please:")
    prompt_parts.extend(
        [
            "1. Identify key skills, experience level, and job preferences",
            "2. Suggest relevant job categories and keywords for searching",
            "3. Recommend search parameters (location, salary range, etc.)",
            "4. Create targeted search queries using the HireBase API tools",
        ]
    )

    return "\n".join(prompt_parts)


def main():
    mcp.run()


if __name__ == "__main__":
    main()
