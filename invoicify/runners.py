import yaml
from invoicify.src.generate import make_report


# read yaml file
def read_yaml(file_path):
    with open(file_path, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


def init_runners(args):
    config = read_yaml(args.config)

    if (args.commands == 'generate'):
        make_report(args, config)
