from .random_split import random_split

SUPPORTED_SPLIT_FNS = {
        random_split.__name__: random_split
        }

def get_split_fn(name):
    return SUPPORTED_SPLIT_FNS[name]
