import json
import requests


class ClockifyAPI:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": api_key, "Content-Type": "application/json"})
        self.api_url = "https://api.clockify.me/api/v1"

    def get_time_entries(self, start_date, end_date):
        url = f"{self.api_url}/time-entries"
        params = {"startDate": start_date, "endDate": end_date}
        r = self.session.request(method="GET", url=url, params=params)
        return r.json()

    def get_workspaces(self):
        url = f"{self.api_url}/workspaces"
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_projects(self, workspace_id):
        url = f"{self.api_url}/workspaces/{workspace_id}/projects"
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_tasks(self, project_id):
        url = f"{self.api_url}/projects/{project_id}/tasks"
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_time_entry(self, time_entry_id):
        url = f"{self.api_url}/time-entries/{time_entry_id}"
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_user(self):
        url = f"{self.api_url}/user"
        r = self.session.request(method="GET", url=url)
        r.raise_for_status()
        return r.json()

    def summary_report(self, workspace_id, data):
        url = (
            f"https://reports.api.clockify.me/workspaces/{workspace_id}/reports/summary"
        )

        r = self.session.request(method="POST", url=url, data=json.dumps(data))
        return r.json()

    def detailed_report(self, workspace_id, data):
        url = (
            f"https://reports.api.clockify.me/workspaces/{workspace_id}/reports/detailed"
        )

        r = self.session.request(method="POST", url=url, data=json.dumps(data))
        return r.json()
