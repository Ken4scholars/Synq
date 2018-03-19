try:
    print('Trying import local.py settings...')
    from .local import *  # noqa
except ImportError:
    print('Trying import prod.py settings...')
    from .prod import *  # noqa