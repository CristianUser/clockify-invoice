from invoicify.arguments import parse_args
from invoicify.runners import init_runners


def main():
    init_runners(parse_args())


if __name__ == "__main__":
    main()
