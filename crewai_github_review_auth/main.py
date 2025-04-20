import os

from crew import GitHubPRReviewCrew
from dotenv import load_dotenv

load_dotenv()


def run_crew():
    """Run the PR review crew."""
    crew = GitHubPRReviewCrew(
        repo_name=os.getenv("GITHUB_REPO", "securebotinc/ai-gateway"),
    )
    return crew.crew().kickoff()


if __name__ == "__main__":
    print("## Welcome to GitHub PR Review System")
    print("----------------------------------")

    print("\nRunning with crew...")
    result = run_crew()
    print("\n\n########################")
    print("## PR Review Results")
    print("########################\n")
    print(result)
