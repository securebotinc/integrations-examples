# GitHub PR Review System

A system for automated GitHub Pull Request reviews using CrewAI and direct GitHub REST API integration. This system provides a comprehensive automated review process using a team of specialized AI agents.

## Prerequisites
- Python 3.9 or higher
- GitHub Personal Access Token with appropriate permissions
- Agent Auth credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/securebotinc/integrations-examples
cd integrations-examples/crewai_github_review_auth
```

2. Create and activate a virtual environment:
```bash
uv venv
source .venv/bin/activate
```

3. Install dependencies:
```bash
uv pip install -e .
```

4. Configure environment variables:
Create a `.env` by renaming `.env.example` file in the project root with the following variables:
```env
# GitHub Configuration
GITHUB_REPO=mx11212/frontend-stuff
GITHUB_API_BASE_URL=https://github.eastus.dev.securebot.io # Github API Passthrough Proxy URL
OPENAI_API_KEY=""

# Securebot Configuration
X_USER_ID=<user_id> Onboard a user to git integration and use its userid to fetch data
X_RESOURCE_URN=<resource_urn> # Create a github integration, and use its resource urn

# Agent Auth Configuration
AGENT_AUTH_PROJECT_ID=<project_id>
AGENT_AUTH_CLIENT_ID=<client_id>
AGENT_AUTH_CLIENT_SECRET=<client_secret>
```

## Usage

### Running the Automated Review Process

#### 1. Identities
There are 3 agents in this project, agent ids needs to be created for each using the ui console
- "pr-analyzer-agent"
- "code-reviewer-agent"
- "pr-reviewer-agent"

#### 2. Github Integration
Configure the github integration and onboard a user, update the user id in the .env file as required

#### 3 Assign Permissions
Create appropriate task and tool resources in the ui and assign permissions to the agents

#### 4 Running Example
Run the automated review process using CrewAI:

```bash
python main.py
```

The system will:
1. Analyze all open PRs in the repository
2. Review code changes in each PR
3. Create comprehensive reviews for each PR

## Configuration

### Agent Configuration

Agent behavior can be customized through YAML configuration files:
- `config/agents.yaml`: Configure agent roles, goals, and backstories
- `config/tasks.yaml`: Define task descriptions and expected outputs
