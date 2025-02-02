# core/webhooks.py
import requests
import logging
from config import WEBHOOK_URLS, NOTION_API_KEY, NOTION_DATABASE_ID, GITHUB_ACCESS_TOKEN, GITHUB_REPO_OWNER, GITHUB_REPO_NAME, SLACK_CHANNEL
import os
import json
from typing import Dict, List, Any

logging.basicConfig(level=logging.INFO)

def send_webhook(event: str, payload: dict):
    """Send webhook notifications based on the event type."""
    url = WEBHOOK_URLS.get(event)
    if not url:
        logging.warning(f"No webhook URL configured for event: {event}")
        return
    
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        logging.info(f"Webhook {event} sent successfully: {response.status_code}")
    except Exception as e:
        logging.error(f"Error sending {event} webhook: {e}")

def send_notion_update(state_id: str, messages: List[str], data_store: Dict[str, Any]) -> bool:
    """
    Update Notion database with workflow state information.
    Returns True if successful, False otherwise.
    """
    if not NOTION_API_KEY or not NOTION_DATABASE_ID:
        print("Notion credentials not configured")
        return False

    try:
        headers = {
            "Authorization": f"Bearer {NOTION_API_KEY}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"
        }

        data = {
            "parent": {"database_id": NOTION_DATABASE_ID},
            "properties": {
                "State ID": {"title": [{"text": {"content": str(state_id)}}]},
                "Status": {"select": {"name": "Completed"}},
                "Messages": {"rich_text": [{"text": {"content": "\n".join(messages)}}]},
                "Data Store": {"rich_text": [{"text": {"content": json.dumps(data_store, indent=2)}}]}
            }
        }

        response = requests.post(
            "https://api.notion.com/v1/pages",
            headers=headers,
            json=data
        )
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Error updating Notion: {str(e)}")
        return False

def create_github_issue(error_message: str) -> bool:
    """
    Create a GitHub issue for workflow errors.
    Returns True if successful, False otherwise.
    """
    if not GITHUB_ACCESS_TOKEN or not GITHUB_REPO_OWNER or not GITHUB_REPO_NAME:
        print("GitHub credentials not configured")
        return False

    try:
        url = WEBHOOK_URLS["github"].format(owner=GITHUB_REPO_OWNER, repo=GITHUB_REPO_NAME)
        headers = {
            "Authorization": f"Bearer {GITHUB_ACCESS_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }
        
        data = {
            "title": "Workflow Error Detected",
            "body": f"An error occurred in the workflow:\n\n```\n{error_message}\n```\n\nPlease investigate and resolve.",
            "labels": ["bug", "workflow-error"]
        }
        
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Error creating GitHub issue: {str(e)}")
        return False

def trigger_zapier_workflow(payload: Dict[str, Any]) -> bool:
    """
    Trigger a Zapier workflow with the provided payload.
    Returns True if successful, False otherwise.
    """
    if not WEBHOOK_URLS["zapier"]:
        print("Zapier webhook URL not configured")
        return False

    try:
        response = requests.post(WEBHOOK_URLS["zapier"], json=payload)
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Error triggering Zapier workflow: {str(e)}")
        return False

def send_slack_notification(message: str) -> bool:
    """
    Send a notification to Slack.
    Returns True if successful, False otherwise.
    """
    if not SLACK_CHANNEL:
        print("Slack channel not configured")
        return False

    try:
        payload = {"text": message, "channel": SLACK_CHANNEL}
        response = requests.post(WEBHOOK_URLS["slack"], json=payload)
        response.raise_for_status()
        return True

    except Exception as e:
        print(f"Error sending Slack notification: {str(e)}")
        return False