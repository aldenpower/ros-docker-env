from sys import stderr


def eprint(*args, **kwargs):
    """
    TODO
    """
    print(*args, file=stderr, **kwargs)
