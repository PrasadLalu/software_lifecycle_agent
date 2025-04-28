import os
from atlassian import Jira

class JiraTool:
    def __init__(self):
        self.jira = Jira(
            url=os.getenv("JIRA_INSTANCE_URL"),
            username=os.getenv("JIRA_USERNAME"),
            password=os.getenv("JIRA_API_TOKEN"),
        )

    def create_user_story(self, title, description, acceptance_criteria):
        acceptance_criteria_text = "\n- ".join([""] + acceptance_criteria)

        # Create new user story
        user_story = {
            "project": {"key": "LI"},
            "summary": title,
            "description": f"""{description}
            Acceptance Criteria:
            {acceptance_criteria_text}""",
            "issuetype": {"name": "Story"},
            "priority": {"name": "Medium"},
        }

        try:
            issue = self.jira.issue_create(fields=user_story)
            print(f"Jira issue created successfully! Issue Key: {issue['key']}")
        except Exception as e:
            print(f"Jira issue creation failed: {e}")

        # print("user_story: ", user_story)


class Tool:
    def __init__(self):
        self.jira_tool = JiraTool()

    def get_jira_tool(self):
        """Returns the Jira tool object."""
        return self.jira_tool
