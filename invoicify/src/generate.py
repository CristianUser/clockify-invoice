from invoicify.src.clockify import ClockifyAPI
from invoicify.src.template import TemplateProcessor
from invoicify.common.constants import CLOCKIFY_API_KEY

from datetime import datetime


def format_date(date):
    return date.replace("-", "/")


def seconds_to_hours(seconds):
    return seconds / 3600


def make_report(args, config):
    start_date = f"{args.start_date}T00:00:00.000Z"
    end_date = f"{args.end_date}T00:00:00.000Z"
    clockify_api_key = args.clockify_api_key or CLOCKIFY_API_KEY
    dev_rate = config.get("variables").get("rates").get("dev")
    coaching_rate = config.get("variables").get("rates").get("coaching")

    clockify = ClockifyAPI(clockify_api_key)

    user = clockify.get_user()
    default_workspace = user["defaultWorkspace"]

    report = clockify.summary_report(default_workspace, start_date, end_date)
    report_group = report.get("groupOne")[0]
    duration_total = report_group.get("duration")

    coaching_duration = [
        child
        for child in report_group.get("children")
        if child.get("nameLowerCase") == "coaching"
    ][0].get("duration")

    development_duration = duration_total - coaching_duration
    development_cost = dev_rate * seconds_to_hours(development_duration)
    coaching_cost = coaching_rate * seconds_to_hours(coaching_duration)

    invoice_range = f"{format_date(args.start_date)} - {format_date(args.end_date)}"
    invoice_number = args.invoice_number or datetime.now().strftime("%Y%m%d")

    bank = config.get("variables").get("bank")
    client = config.get("variables").get("client")
    company = config.get("variables").get("company")

    template = TemplateProcessor(
        "invoice.html",
        {
            "invoice_number": invoice_number,
            "date_issue": datetime.today().strftime("%d/%m/%Y"),
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

    template.render_to_pdf(f"invoice-{invoice_number}.pdf")
