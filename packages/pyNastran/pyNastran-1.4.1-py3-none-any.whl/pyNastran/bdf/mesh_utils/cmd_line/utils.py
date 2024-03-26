import sys

def filter_no_args(msg: str, argv: list[str], quiet: bool=False):
    if len(argv) == 1:
        if quiet:
            sys.exit()
        sys.exit(msg)
