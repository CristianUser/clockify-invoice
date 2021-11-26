import json
import requests


class ClockifyAPI:
    def __init__(self, api_key):
        self.session = requests.Session()
        self.session.headers.update({"X-Api-Key": api_key, "Content-Type": "application/json"})

    def get_time_entries(self, start_date, end_date):
        url = "https://api.clockify.me/api/v1/time-entries"
        params = {"startDate": start_date, "endDate": end_date}
        r = self.session.request(method="GET", url=url, params=params)
        return r.json()

    def get_workspaces(self):
        url = "https://api.clockify.me/api/v1/workspaces"
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_projects(self, workspace_id):
        url = "https://api.clockify.me/api/v1/workspaces/{}/projects".format(
            workspace_id
        )
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_tasks(self, project_id):
        url = "https://api.clockify.me/api/v1/projects/{}/tasks".format(project_id)
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_time_entry(self, time_entry_id):
        url = "https://api.clockify.me/api/v1/time-entries/{}".format(time_entry_id)
        r = self.session.request(method="GET", url=url)
        return r.json()

    def get_user(self):
        url = "https://api.clockify.me/api/v1/user"
        r = self.session.request(method="GET", url=url)
        return r.json()

    def summary_report(self, workspace_id, start_date, end_date):
        url = (
            f"https://reports.api.clockify.me/workspaces/{workspace_id}/reports/summary"
        )
        data = {
            "amountShown": "HIDE_AMOUNT",
            "customFields": None,
            "dateRangeEnd": end_date.isoformat(),
            "dateRangeStart": start_date.isoformat(),
            "description": "",
            "rounding": False,
            "sortOrder": "ASCENDING",
            "groups": ["PROJECT", "TAG"],
            "sortColumn": "GROUP",
            "userLocale": "en_US",
            "withoutDescription": False,
            "zoomLevel": "WEEK",
            "summaryFilter": {"groups": ["PROJECT", "TAG"], "sortColumn": "GROUP"},
            "exportType": "JSON",
        }

        r = self.session.request(method="POST", url=url, data=json.dumps(data))
        return r.json()
