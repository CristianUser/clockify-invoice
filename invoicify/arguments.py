import argparse


def add_request_args(parser):
    parser.add_argument(
        "-d0", "--start-date", required=False, default="2021-10-25", help="Start Date"
    )
    parser.add_argument(
        "-d1", "--end-date", required=False, default="2021-11-25", help="End Date"
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


def create_request_parser(parent):
    parser = parent.add_parser("generate", help="generator module")
    add_request_args(parser)


def parse_args():
    parser = argparse.ArgumentParser(description="CLI with some awesome things")

    subparser = parser.add_subparsers(
        title="commands", dest="commands", help="Provided source specific subparsers"
    )
    create_request_parser(subparser)

    return parser.parse_args()
