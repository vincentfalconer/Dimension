import os
import requests
from dotenv import load_dotenv

# Load GitHub token from .env file
load_dotenv()
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# GitHub repository and project details
OWNER = 'vincentfalconer'
REPO = 'Dimension'
PROJECT_NAME = 'Project Dimension'

# GitHub API headers
headers = {
    'Authorization': f'token {GITHUB_TOKEN}',
    'Accept': 'application/vnd.github.inertia-preview+json'
}

# Step 1: Get all projects in the repository
projects_url = f'https://api.github.com/repos/{OWNER}/{REPO}/projects'
projects_response = requests.get(projects_url, headers=headers)

try:
    projects = projects_response.json()
except Exception as e:
    print("❌ Failed to parse JSON response:", e)
    print("Raw response:", projects_response.text)
    exit()

# Ensure the response is a list
if not isinstance(projects, list):
    print("❌ Unexpected response format. Expected a list of projects.")
    print("Raw response:", projects_response.text)
    exit()

# Find the project ID for 'Project Dimension'
project_id = None
for project in projects:
    if project.get('name') == PROJECT_NAME:
        project_id = project.get('id')
        break

if not project_id:
    print(f"❌ Project '{PROJECT_NAME}' not found in repository '{REPO}'.")
    exit()

# Step 2: Get columns in the project
columns_url = f'https://api.github.com/projects/{project_id}/columns'
columns_response = requests.get(columns_url, headers=headers)

try:
    columns = columns_response.json()
except Exception as e:
    print("❌ Failed to parse columns JSON response:", e)
    print("Raw response:", columns_response.text)
    exit()

if not isinstance(columns, list):
    print("❌ Unexpected columns response format. Expected a list.")
    print("Raw response:", columns_response.text)
    exit()

# Map column names to their IDs
column_ids = {}
for column in columns:
    column_ids[column.get('name')] = column.get('id')

# Step 3: Define tasks for each column
tasks = {
    'Todo': [
        'Initialize GitHub repo',
        'Set up project in VS Code',
        'Create GitHub Actions workflow',
        'Get Azure publish profile',
        'Add GitHub secret for Azure deployment'
    ],
    'In Progress': [
        'Write and test application code',
        'Push code to GitHub',
        'Configure workflow file'
    ],
    'Done': [
        'Azure secret added',
        'Workflow committed',
        'GitHub Actions ran successfully',
        'Website deployed and verified'
    ]
}

# Step 4: Add tasks to each column
for column_name, cards in tasks.items():
    column_id = column_ids.get(column_name)
    if not column_id:
        print(f"⚠️ Column '{column_name}' not found in project.")
        continue

    for card in cards:
        create_card_url = f'https://api.github.com/projects/columns/{column_id}/cards'
        card_data = {'note': card}
        response = requests.post(create_card_url, headers=headers, json=card_data)
        if response.status_code == 201:
            print(f"✅ Added card '{card}' to column '{column_name}'.")
        else:
            print(f"❌ Failed to add card '{card}' to column '{column_name}': {response.text}")

