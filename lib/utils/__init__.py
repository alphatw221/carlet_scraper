
import re


def is_number(s):
    return bool(re.match(r'^-?\d+(?:\.\d+)?$', s))
