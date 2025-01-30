# config.py

# Webhook URLs for various services
WEBHOOK_URLS = {
    "notion": "https://api.notion.com/v1/pages",
    "github": "https://api.github.com/repos/{owner}/{repo}/issues",
    "zapier": "https://hooks.zapier.com/hooks/catch/123456/",
    "slack": "https://hooks.slack.com/services/T00000000/B00000000/XXXXXXXXXXXXXXXXXXXXXXXX"
}

# API Credentials
NOTION_API_KEY = "your_notion_secret"
NOTION_DATABASE_ID = "your_database_id"

GITHUB_ACCESS_TOKEN = "your_github_token"
GITHUB_REPO_OWNER = "your_github_username"
GITHUB_REPO_NAME = "your_repository_name"

SLACK_CHANNEL = "#workflow-updates"