"""Custom tools for agents."""
from typing import Dict, Any, List
from langchain_core.tools import BaseTool, tool
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.utilities.serpapi import SerpAPIWrapper
from langchain_community.tools.github.tool import GitHubAction
from langchain_community.tools.file_management import (
    ReadFileTool,
    WriteFileTool,
    ListDirectoryTool
)
import requests
import json
import logging
from config import settings

# Initialize logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL.upper()),
    format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)

# Search Tools
search = DuckDuckGoSearchRun()

@tool
def web_search(query: str) -> str:
    """Search the web for information."""
    try:
        return search.run(query)
    except Exception as e:
        logger.error(f"Web search error: {e}")
        return f"Error performing web search: {str(e)}"

serpapi = SerpAPIWrapper()

@tool
def serpapi_search(query: str) -> str:
    """Search using SerpAPI for more detailed results."""
    try:
        return serpapi.run(query)
    except Exception as e:
        logger.error(f"SerpAPI search error: {e}")
        return f"Error performing SerpAPI search: {str(e)}"

# File Management Tools
read_file = ReadFileTool()
write_file = WriteFileTool()
list_directory = ListDirectoryTool()

@tool
def save_to_file(file_path: str, content: str) -> str:
    """Save content to a file."""
    try:
        write_file.run({"file_path": file_path, "text": content})
        return f"Content saved to {file_path}"
    except Exception as e:
        logger.error(f"File write error: {e}")
        return f"Error saving to file: {str(e)}"

@tool
def read_from_file(file_path: str) -> str:
    """Read content from a file."""
    try:
        return read_file.run(file_path)
    except Exception as e:
        logger.error(f"File read error: {e}")
        return f"Error reading file: {str(e)}"

@tool
def list_files(directory_path: str) -> str:
    """List files in a directory."""
    try:
        return list_directory.run(directory_path)
    except Exception as e:
        logger.error(f"Directory listing error: {e}")
        return f"Error listing directory: {str(e)}"

# GitHub Tools
github = GitHubAction(
    repository=settings.GITHUB_REPO,
    access_token=settings.GITHUB_TOKEN
)

@tool
def create_github_issue(title: str, body: str) -> str:
    """Create a GitHub issue."""
    try:
        return github.run({
            "action": "create_issue",
            "title": title,
            "body": body
        })
    except Exception as e:
        logger.error(f"GitHub issue creation error: {e}")
        return f"Error creating GitHub issue: {str(e)}"

# Integration Tools
@tool
def send_to_notion(content: Dict[str, Any]) -> str:
    """Send content to Notion database."""
    try:
        headers = {
            "Authorization": f"Bearer {settings.NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }
        
        data = {
            "parent": {"database_id": settings.NOTION_DATABASE_ID},
            "properties": content
        }
        
        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        
        return "Content sent to Notion successfully"
    except Exception as e:
        logger.error(f"Notion integration error: {e}")
        return f"Error sending to Notion: {str(e)}"

@tool
def send_to_slack(message: str) -> str:
    """Send a message to Slack."""
    try:
        response = requests.post(
            settings.SLACK_WEBHOOK_URL,
            json={"text": message}
        )
        response.raise_for_status()
        
        return "Message sent to Slack successfully"
    except Exception as e:
        logger.error(f"Slack integration error: {e}")
        return f"Error sending to Slack: {str(e)}"

# Tool Groups
RESEARCH_TOOLS = [
    web_search,
    serpapi_search
]

FILE_TOOLS = [
    read_from_file,
    save_to_file,
    list_files
]

INTEGRATION_TOOLS = [
    create_github_issue,
    send_to_notion,
    send_to_slack
]

# Tool Registry
TOOL_REGISTRY = {
    "professor_athena": RESEARCH_TOOLS + FILE_TOOLS,
    "dr_milgrim": RESEARCH_TOOLS + INTEGRATION_TOOLS,
    "yaat": FILE_TOOLS + INTEGRATION_TOOLS
} 