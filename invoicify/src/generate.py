from invoicify.src.clockify import ClockifyAPI
from invoicify.src.template import TemplateProcessor
from invoicify.common.constants import CLOCKIFY_API_KEY, DEV_RATE, COACHING_RATE

from datetime import datetime


clockify = ClockifyAPI(CLOCKIFY_API_KEY)


# replace - with /
def format_date(date):
    return date.replace("-", "/")


def seconds_to_hours(seconds):
    return seconds / 3600


def make_report(args):
    start_date = f"{args.start_date}T00:00:00.000Z"
    end_date = f"{args.end_date}T00:00:00.000Z"
    # end_date = f"{args.end_date}T23:59:59.999Z"

    user = clockify.get_user()
    default_workspace = user["defaultWorkspace"]

    report = clockify.summary_report(default_workspace, start_date, end_date)
    report_group = report.get("groupOne")[0]
    duration_total = report_group.get("duration")

    # find children with nameLowerCase
    coaching_duration = [
        child
        for child in report_group.get("children")
        if child.get("nameLowerCase") == "coaching"
    ][0].get("duration")

    development_duration = duration_total - coaching_duration
    development_cost = DEV_RATE * seconds_to_hours(development_duration)
    coaching_cost = COACHING_RATE * seconds_to_hours(coaching_duration)

    invoice_range = f"{format_date(args.start_date)} - {format_date(args.end_date)}"
    invoice_number = args.invoice_number or datetime.now().strftime("%Y%m%d")

    template = TemplateProcessor(
        "invoice.html",
        {
            "invoice_number": invoice_number,
            "date_issue": datetime.today().strftime("%d/%m/%Y"),
            "currency": "USD",
            "total_time": round(seconds_to_hours(duration_total), 2),
            "client": {
                "name": "Intellisys",
            },
            "company": {
                "name": user.get("name"),
                "mail": user.get("email"),
            },
            "work": [
                {
                    "desc": f"Development {invoice_range}",
                    "time": round(seconds_to_hours(development_duration), 2),
                    "rate": DEV_RATE,
                    "cost": round(development_cost, 2),
                },
                {
                    "desc": f"Coaching {invoice_range}",
                    "time": round(seconds_to_hours(coaching_duration), 2),
                    "rate": COACHING_RATE,
                    "cost": round(coaching_cost, 2),
                },
            ],
            "total_cost": round(development_cost + coaching_cost, 2),
            "bank": {
                "name": "Banreservas",
                "account_number": "9604078331",
                "account_name": "Cristian Mejia",
                "account_type": "Ahorro en dólares",
                "account_holder_id": "40228165102"
            },
        },
    )

    template.render_to_pdf(f"invoice-{invoice_number}.pdf")
