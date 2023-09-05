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
    return datetime.combine(
        parse_date(date_string), time.max
    )


def add_n_months_to_date(date, n):
    return date + relativedelta(months=n)


def format_date(date):
    return date.strftime("%d/%m/%Y")


def seconds_to_hours(seconds):
    return seconds / 3600


def get_child_duration(task, report_group):
    task_report = [
        child
        for child in report_group.get("children")
        if child.get("nameLowerCase") == task
    ]
    return task_report[0].get("duration") if len(task_report) > 0 else 0


def build_report_data(args, config):
    start_date = parse_date(args.start_date)
    end_date = parse_end_date(args.end_date)
    clockify_api_key = args.clockify_api_key or CLOCKIFY_API_KEY

    if not clockify_api_key:
        raise Exception("Missing Clockify API Key")

    clockify = ClockifyAPI(clockify_api_key)

    user = clockify.get_user()
    LOG.debug("Got user data", extra={"user": user})
    default_workspace = user["defaultWorkspace"]

    report = clockify.summary_report(default_workspace, start_date, end_date)
    LOG.debug("Got report data", extra={"report": report})
    report_group = report.get("groupOne")[0]

    report_tasks = list(config.get("tasks").keys())
    tasks_duration = {}
    tasks_cost = {}

    for task in report_tasks:
        task_rate = config.get("tasks").get(task).get("rate")
        tasks_duration[task] = seconds_to_hours(get_child_duration(task, report_group))
        tasks_cost[task] = task_rate * tasks_duration[task]
        LOG.debug(
            "Got task duration", extra={"task": task, "duration": tasks_duration[task]}
        )
        LOG.debug("Got task cost", extra={"task": task, "cost": tasks_cost[task]})

    duration_total = sum(tasks_duration.values())
    total_cost = sum(tasks_cost.values())

    work_details = []

    invoice_range = f"{format_date(start_date)} - {format_date(end_date)}"
    for task in report_tasks:
        task_info = config.get("tasks").get(task)
        task_name = task_info.get("description")
        work_details.append(
            {
                "desc": f"{task_name} {invoice_range}",
                "time": round(tasks_duration[task], 2),
                "cost": round(tasks_cost[task], 2),
                "rate": task_info.get("rate"),
            }
        )

    invoice_number = args.invoice_number or end_date.strftime("%Y%m%d")

    bank = config.get("variables").get("bank")
    client = config.get("variables").get("client")
    company = config.get("variables").get("company")

    return {
        "invoice_number": invoice_number,
        "date_issue": datetime.today().strftime("%d/%m/%Y"),
        "date_expire": add_n_months_to_date(end_date, 1).strftime("%d/%m/%Y"),
        "currency": config.get("variables").get("currency"),
        "total_time": round(duration_total, 2),
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
        "work": work_details,
        "total_cost": round(total_cost, 2),
        "bank": {
            "name": bank.get("name"),
            "account_number": bank.get("account_number"),
            "account_owner": bank.get("account_owner"),
            "account_type": bank.get("account_type"),
            "account_currency": bank.get("account_currency"),
            "account_owner_id": bank.get("account_owner_id"),
        },
    }


def make_report(args, config):
    data = build_report_data(args, config)
    template = TemplateProcessor(
        "invoice.html",
        data
    )

    invoice_number = data["invoice_number"]
    if args.export_type == "pdf":
        output_file = f"invoice-{invoice_number}.pdf"
        template.render_to_pdf(output_file)
        LOG.info(f"Generated {output_file}")
    elif args.export_type == "html":
        output_file = f"invoice-{invoice_number}.html"
        print(template.render(output_file))
