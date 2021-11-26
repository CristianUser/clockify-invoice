from invoicify.src.clockify import ClockifyAPI
from invoicify.src.template import TemplateProcessor
from invoicify.common.constants import CLOCKIFY_API_KEY

import logging

from datetime import datetime
from dateutil.relativedelta import relativedelta

LOG = logging.getLogger(__name__)


def parse_date(date_string):
    return datetime.strptime(date_string, "%d-%m-%Y")


def add_n_months_to_date(date, n):
    return date + relativedelta(months=n)


def format_date(date):
    return date.strftime("%d/%m/%Y")


def seconds_to_hours(seconds):
    return seconds / 3600


def make_report(args, config):
    start_date = parse_date(args.start_date)
    end_date = parse_date(args.end_date)
    clockify_api_key = args.clockify_api_key or CLOCKIFY_API_KEY
    dev_rate = config.get("variables").get("rates").get("dev")
    coaching_rate = config.get("variables").get("rates").get("coaching")

    if not clockify_api_key:
        raise Exception("Missing Clockify API Key")

    clockify = ClockifyAPI(clockify_api_key)

    user = clockify.get_user()
    LOG.debug("Got user data", extra={"user": user})
    default_workspace = user["defaultWorkspace"]

    report = clockify.summary_report(default_workspace, start_date, end_date)
    LOG.debug("Got report data", extra={"report": report})
    report_group = report.get("groupOne")[0]

    coaching_duration = [
        child
        for child in report_group.get("children")
        if child.get("nameLowerCase") == "coaching"
    ][0].get("duration")
    duration_total = report_group.get("duration")
    development_duration = duration_total - coaching_duration

    LOG.debug(
        "Calculated duration",
        extra={
            "coaching_duration": seconds_to_hours(coaching_duration),
            "development_duration": seconds_to_hours(development_duration),
        }
    )

    development_cost = dev_rate * seconds_to_hours(development_duration)
    coaching_cost = coaching_rate * seconds_to_hours(coaching_duration)

    invoice_range = f"{format_date(start_date)} - {format_date(end_date)}"
    invoice_number = args.invoice_number or end_date.strftime("%Y%m%d")

    bank = config.get("variables").get("bank")
    client = config.get("variables").get("client")
    company = config.get("variables").get("company")

    template = TemplateProcessor(
        "invoice.html",
        {
            "invoice_number": invoice_number,
            "date_issue": datetime.today().strftime("%d/%m/%Y"),
            "date_expire": add_n_months_to_date(end_date, 1).strftime(
                "%d/%m/%Y"
            ),
            "currency": config.get("variables").get("currency"),
            "total_time": round(seconds_to_hours(duration_total), 2),
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
            "work": [
                {
                    "desc": f"Development {invoice_range}",
                    "time": round(seconds_to_hours(development_duration), 2),
                    "rate": dev_rate,
                    "cost": round(development_cost, 2),
                },
                {
                    "desc": f"Coaching {invoice_range}",
                    "time": round(seconds_to_hours(coaching_duration), 2),
                    "rate": coaching_rate,
                    "cost": round(coaching_cost, 2),
                },
            ],
            "total_cost": round(development_cost + coaching_cost, 2),
            "bank": {
                "name": bank.get("name"),
                "account_number": bank.get("account_number"),
                "account_owner": bank.get("account_owner"),
                "account_type": bank.get("account_type"),
                "account_currency": bank.get("account_currency"),
                "account_owner_id": bank.get("account_owner_id"),
            },
        },
    )

    if args.export_type == "pdf":
        output_file = f"invoice-{invoice_number}.pdf"
        template.render_to_pdf(output_file)
        LOG.info(f"Generated {output_file}")
    elif args.export_type == "html":
        output_file = f"invoice-{invoice_number}.html"
        print(template.render(output_file))
