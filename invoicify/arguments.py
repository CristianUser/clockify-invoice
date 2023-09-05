import argparse


def add_generate_args(parser):
    parser.add_argument(
        "-d0", "--start-date", required=False, default="25-10-2021", help="Start Date"
    )
    parser.add_argument(
        "-d1", "--end-date", required=False, default="25-11-2021", help="End Date"
    )
    parser.add_argument(
        "-i",
        "--invoice-number", required=False, help="Invoice Number",
    )
    parser.add_argument(
        "-a",
        "--clockify-api-key",
        required=False,
        help="Clockify API Key",
    )
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        help="Config File",
    )
    parser.add_argument(
        "-e",
        "--export-type",
        required=False,
        help="Export Type",
        default="pdf",
    )


def add_report_args(parser):
    parser.add_argument(
        "-d0", "--start-date", required=False, default="04-08-2023", help="Start Date"
    )
    parser.add_argument(
        "-d1", "--end-date", required=False, default="11-08-2023", help="End Date"
    )
    parser.add_argument(
        "-i",
        "--invoice-number", required=False, help="Invoice Number",
    )
    parser.add_argument(
        "-a",
        "--clockify-api-key",
        required=False,
        help="Clockify API Key",
    )
    parser.add_argument(
        "-c",
        "--config",
        required=False,
        help="Config File",
    )
    parser.add_argument(
        "-e",
        "--export-type",
        required=False,
        help="Export Type",
        default="pdf",
    )


def create_generate_parser(parent):
    parser = parent.add_parser("generate", help="generator module")
    add_generate_args(parser)


def create_report_parser(parent):
    parser = parent.add_parser("report", help="report module")
    add_generate_args(parser)


def parse_args():
    parser = argparse.ArgumentParser(prog="invoicify", description="CLI with some awesome things")
    parser.add_argument(
        "-l",
        "--log-level",
        default="INFO",
        help="Set log level, defaults to %(default)s",
    )
    add_generate_args(parser)

    subparser = parser.add_subparsers(
        title="commands", dest="commands", help="Provided source specific subparsers"
    )
    create_generate_parser(subparser)
    create_report_parser(subparser)

    return parser.parse_args()
