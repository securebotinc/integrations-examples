import os
from typing import Any, Dict, List, Optional

import requests
from crewai.tools import BaseTool
from pydantic import Field
from securebot_sdk.identity.crewai import requires_tool_scope

GITHUB_API_BASE_URL = "https://github.eastus.dev.securebot.io"


def get_headers(token: str):
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json",
        "X-USER-ID": os.getenv("X_USER_ID"),
        "X-RESOURCE-URN": os.getenv("X_RESOURCE_URN"),
    }


@requires_tool_scope(scope="app:tool:GitHubPRListTool", pass_token=True)
class GitHubPRListTool(BaseTool):
    """Tool for listing GitHub pull requests."""

    name: str = "github_pr_list"
    description: str = "List all open pull requests in a repository"
    return_direct: bool = False
    repo_name: str = Field(..., description="Repository name in format 'owner/repo'")
    token: Optional[str] = None

    def __init__(self, repo_name: str, token: Optional[str] = None, **kwargs):
        super().__init__(repo_name=repo_name, token=token, **kwargs)

    def _run(self, *args, **kwargs) -> List[Dict[str, Any]]:
        """List all open pull requests in the repository."""
        owner, repo = self.model_dump()["repo_name"].split("/")
        url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls"

        try:
            response = requests.get(
                url,
                headers=get_headers(self.token),
                timeout=10,
            )
            response.raise_for_status()
            prs = response.json()

            return [
                {
                    "number": pr["number"],
                    "title": pr["title"],
                    "state": pr["state"],
                    "created_at": pr["created_at"],
                    "updated_at": pr["updated_at"],
                    "user": pr["user"]["login"],
                    "url": pr["html_url"],
                }
                for pr in prs
            ]
        except requests.exceptions.RequestException as e:
            return [{"error": str(e)}]


@requires_tool_scope(scope="app:tool:GitHubPRDetailsTool", pass_token=True)
class GitHubPRDetailsTool(BaseTool):
    """Tool for getting detailed information about a GitHub pull request."""

    name: str = "github_pr_details"
    description: str = "Get detailed information about a specific pull request"
    return_direct: bool = False
    repo_name: str = Field(..., description="Repository name in format 'owner/repo'")
    token: Optional[str] = None

    def __init__(self, repo_name: str, token: Optional[str] = None, **kwargs):
        super().__init__(repo_name=repo_name, token=token, **kwargs)

    def _run(self, pr_number: str, **kwargs) -> Dict[str, Any]:
        """Get detailed information about a specific pull request."""
        owner, repo = self.model_dump()["repo_name"].split("/")
        url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}"

        try:
            # Get PR details
            response = requests.get(
                url,
                headers=get_headers(self.token),
                timeout=10,
            )
            response.raise_for_status()
            pr_details = response.json()

            # Get changed files
            files_url = f"{url}/files"
            response = requests.get(
                files_url,
                headers=get_headers(self.token),
                timeout=10,
            )
            response.raise_for_status()
            changed_files = response.json()

            # Get commits
            commits_url = f"{url}/commits"
            response = requests.get(
                commits_url,
                headers=get_headers(self.token),
                timeout=10,
            )
            response.raise_for_status()
            commits = response.json()

            # Get comments
            comments_url = f"{url}/comments"
            response = requests.get(
                comments_url,
                headers=get_headers(self.token),
                timeout=10,
            )
            response.raise_for_status()
            comments = response.json()

            return {
                "number": pr_details["number"],
                "title": pr_details["title"],
                "state": pr_details["state"],
                "created_at": pr_details["created_at"],
                "updated_at": pr_details["updated_at"],
                "user": pr_details["user"]["login"],
                "url": pr_details["html_url"],
                "body": pr_details["body"],
                "changed_files": [
                    {
                        "filename": f["filename"],
                        "status": f["status"],
                        "additions": f["additions"],
                        "deletions": f["deletions"],
                        "changes": f["changes"],
                    }
                    for f in changed_files
                ],
                "commits": [
                    {
                        "sha": c["sha"],
                        "message": c["commit"]["message"],
                        "author": c["commit"]["author"]["name"],
                        "date": c["commit"]["author"]["date"],
                    }
                    for c in commits
                ],
                "comments": [
                    {
                        "id": c["id"],
                        "user": c["user"]["login"],
                        "body": c["body"],
                        "created_at": c["created_at"],
                    }
                    for c in comments
                ],
            }
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}


@requires_tool_scope(scope="app:tool:GitHubPRReviewTool", pass_token=True)
class GitHubPRReviewTool(BaseTool):
    """Tool for creating GitHub pull request reviews."""

    name: str = "github_pr_review"
    description: str = "Create a review for a pull request"
    return_direct: bool = False
    token: Optional[str] = None
    repo_name: str = Field(..., description="Repository name in format 'owner/repo'")

    def __init__(self, repo_name: str, token: Optional[str] = None, **kwargs):
        super().__init__(repo_name=repo_name, token=token, **kwargs)

    def _run(self, pr_number: str, event: str, body: str, **kwargs) -> Dict[str, Any]:
        """Create a review for a pull request."""
        owner, repo = self.model_dump()["repo_name"].split("/")
        url = f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
        print(f"Reviewing PR {pr_number} with event {event} and body {body}")

        try:
            # Format the review body
            review_data = {
                "event": "COMMENT",
                "body": body,
                "comments": [],  # Required field for GitHub API
            }

            response = requests.post(
                timeout=10,
                url=url,
                headers=get_headers(self.token),
                json=review_data,
            )

            # Print response for debugging
            print(f"Review request: {review_data}")
            print(f"Response status: {response.status_code}")
            print(f"Response body: {response.text}")
            print("Response: ", response.json())
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            return {"error": str(e)}
