from flask import Flask
import requests
from requests.auth import HTTPBasicAuth
import json
import os
# Load environment variables from .env file
from dotenv import load_dotenv

# create a Flask application instance
app = Flask(__name__)


""""
This script creates a JIRA ticket using the JIRA REST API.
It uses Flask to define a route for creating tickets and the requests library to make HTTP requests.
/createJIRATicket is the endpoint that accepts POST requests to create a JIRA ticket.
"""""
@app.route('/createJIRATicket', methods=['POST'])
def create_jira_ticket(summary, description, project_key, issue_type):
    """
    Create a JIRA ticket using the JIRA REST API.

    :param summary: Summary of the JIRA ticket.
    :param description: Description of the JIRA ticket.
    :param project_key: Key of the project where the ticket will be created.
    :param issue_type: Type of the issue (e.g., 'Task', 'Bug').    
    """

    load_dotenv()  # Load environment variables from .env file
    url = os.getenv("JIRA_URL") # Replace with your JIRA instance URL
    if not url:
        raise ValueError("JIRA_URL environment variable is not set.")
    
    auth = HTTPBasicAuth(os.getenv("JIRA_EMAIL"), os.getenv("JIRA_API_TOKEN"))
    # Ensure that the JIRA_EMAIL and JIRA_API_TOKEN are set
    if not auth.username or not auth.password:
        raise ValueError("JIRA_EMAIL and JIRA_API_TOKEN environment variables must be set.")

    headers = {
    "Accept": "application/json",
    "Content-Type": "application/json"
    }

    payload = json.dumps( {
    "fields": {
    "description": {
      "content": [
        {
          "content": [
            {
              "text": description,
              "type": "text"
            }
          ],
          "type": "paragraph"
        }
      ],
      "type": "doc",
      "version": 1
    },
    "issuetype": {
      "id": issue_type
    },
    "project": {
      "key": project_key
    },
    "summary": summary,
    },
    } )

    response = requests.request(
    "POST",
    url,
    data=payload,
    headers=headers,
    auth=auth
    )

    return json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": "))

"""
Example usage of the create_jira_ticket function
Reused in the main block to demonstrate how to create a JIRA ticket.
Can run this script directly to create a ticket on local environment.
"""""
if __name__ == "__main__":
    # Example usage
    summary = "Example JIRA Ticket"
    description = "This is an example description for the JIRA ticket."
    project_key = "CPG" # Replace with your actual project key
    issue_type = "10001"  # Replace with the actual issue type ID

    ticket = create_jira_ticket(summary, description, project_key, issue_type)
    print(ticket)