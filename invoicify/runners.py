from invoicify.src.generate import make_report


def init_runners(args):
    if (args.commands == 'generate'):
        make_report(args)
