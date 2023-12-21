from invoicify.src.clockify import ClockifyAPI
from invoicify.src.template import TemplateProcessor
from invoicify.common.constants import CLOCKIFY_API_KEY

import logging

from datetime import datetime, time
from dateutil.relativedelta import relativedelta

LOG = logging.getLogger(__name__)


def parse_date(date_string):
    return datetime.strptime(date_string, "%d-%m-%Y")


def parse_end_date(date_string):
    return datetime.combine(parse_date(date_string), time.max)


def add_n_months_to_date(date, n):
    return date + relativedelta(months=n)


def format_date(date):
    return date.strftime("%d-%m-%Y")


def seconds_to_hours(seconds):
    return seconds / 3600


def get_child_duration(task):
    return task["timeInterval"]["duration"]


def get_clockify_report(clockify, workspace_id, start_date, end_date):
    report_data = {
        "dateRangeEnd": end_date.isoformat(),
        "dateRangeStart": start_date.isoformat(),
        "sortOrder": "ASCENDING",
        "description": "",
        "rounding": False,
        "withoutDescription": False,
        "amounts": [],
        "amountShown": "HIDE_AMOUNT",
        "zoomLevel": "WEEK",
        "userLocale": "en-US",
        "customFields": None,
        "userCustomFields": None,
        "kioskIds": [],
        "summaryFilter": {
            "sortColumn": "GROUP",
            "groups": ["DATE", "TASK", "TIMEENTRY"],
            "summaryChartType": "BILLABILITY",
        },
        "exportType": "JSON",
    }
    return clockify.summary_report(workspace_id, report_data)


def build_report_data(args, config):
    start_date = parse_date(args.start_date)
    end_date = parse_end_date(args.end_date)
    clockify_api_key = args.clockify_api_key or config.get("api_key") or CLOCKIFY_API_KEY

    if not clockify_api_key:
        raise Exception("Missing Clockify API Key")

    clockify = ClockifyAPI(clockify_api_key)

    user = clockify.get_user()
    LOG.debug("Got user data", extra={"user": user})
    default_workspace = user["defaultWorkspace"]

    report = get_clockify_report(clockify, default_workspace, start_date, end_date)
    LOG.debug("Got report data", extra={"report": report})

    parsed_entries = []

    for group_a in report.get("groupOne"):
        for group_b in group_a["children"]:
            for entry in group_b["children"]:
                parsed_entry = {
                    "date": group_a["name"],
                    "task": group_b["name"],
                    "description": entry["name"],
                    "duration": round(seconds_to_hours(entry["duration"]), 2),
                }
                parsed_entries.append(parsed_entry)
                LOG.debug(
                    "Got task duration",
                    extra={"task": entry, "parsed_entry": parsed_entry},
                )

    report_number = args.invoice_number or end_date.strftime("%Y%m%d")

    client = config.get("variables").get("client")
    company = config.get("variables").get("company")
    report_range = f"{format_date(start_date)} - {format_date(end_date)}"

    return {
        "report_number": report_number,
        "report_range": report_range,
        "date_issue": datetime.today().strftime("%d/%m/%Y"),
        "date_expire": add_n_months_to_date(end_date, 1).strftime("%d/%m/%Y"),
        "client": {
            "name": client.get("name"),
            "address": client.get("address"),
            "phone": client.get("phone"),
            "email": client.get("email"),
        },
        "company": {
            "name": user.get("name"),
            "email": company.get("email") or user.get("email"),
            "address": company.get("address"),
            "phone": company.get("phone"),
        },
        "work": parsed_entries,
    }


def make_report(args, config):
    data = build_report_data(args, config)

    template = TemplateProcessor("report.html", data)

    report_range = data["report_range"]
    if args.export_type == "pdf":
        output_file = f"report-{report_range}.pdf"
        template.render_to_pdf(output_file)
        LOG.info(f"Generated {output_file}")
    elif args.export_type == "html":
        output_file = f"invoice-{report_range}.html"
        print(template.render(output_file))
