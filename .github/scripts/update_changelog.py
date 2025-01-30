#!/usr/bin/env python3

import os
import re
from datetime import datetime
from git import Repo
from dateutil import parser

CHANGELOG_PATH = "CHANGELOG.md"
UNRELEASED_PATTERN = r"## \[v\d+\.\d+\.\d+\] - \d{4}-\d{2}-XX"

def get_latest_release():
    """Get the latest release tag and date from GitHub."""
    repo = Repo(".")
    tags = sorted(repo.tags, key=lambda t: t.commit.committed_datetime)
    if not tags:
        return None, None
    latest_tag = tags[-1]
    return str(latest_tag), latest_tag.commit.committed_datetime

def update_changelog():
    """Update the CHANGELOG.md with the latest release information."""
    with open(CHANGELOG_PATH, "r") as f:
        content = f.read()

    # Get latest release info
    tag, date = get_latest_release()
    if not tag or not date:
        print("No releases found")
        return

    # Format the date
    formatted_date = date.strftime("%Y-%m-%d")

    # Replace the unreleased date with the actual release date
    updated_content = re.sub(
        UNRELEASED_PATTERN,
        f"## [{tag}] - {formatted_date}",
        content,
        count=1
    )

    # Add new unreleased section if this is a new release
    if updated_content != content:
        new_version = increment_version(tag)
        unreleased_section = f"""# Changelog

All notable changes to the Langchain-Agents project will be documented in this file.

## [v{new_version}] - 2024-03-XX

### Added
- No changes yet

### Changed
- No changes yet

### Fixed
- No changes yet

"""
        updated_content = unreleased_section + updated_content.split("# Changelog")[1]

    # Write the updated content back
    with open(CHANGELOG_PATH, "w") as f:
        f.write(updated_content)

def increment_version(version):
    """Increment the patch version number."""
    match = re.match(r"v(\d+)\.(\d+)\.(\d+)", version)
    if not match:
        return "0.1.0"
    major, minor, patch = map(int, match.groups())
    return f"{major}.{minor}.{int(patch) + 1}"

if __name__ == "__main__":
    update_changelog() 