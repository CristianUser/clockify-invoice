from invoicify.arguments import parse_args
from invoicify.runners import init_runners

import logging
import sys


def _init_logging(args):
    level = getattr(logging, args.log_level.upper(), None)
    if not isinstance(level, int):
        raise ValueError("Unable to parse log level %s" % args.log_level)
    stream_handler = logging.StreamHandler(sys.stderr)
    logging.basicConfig(level=level, handlers=[stream_handler])


def main():
    args = parse_args()
    _init_logging(args)
    init_runners(args)


if __name__ == "__main__":
    main()
