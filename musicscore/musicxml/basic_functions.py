import re


def replace_dash(tag):
    if '-' in tag:
        output = re.sub(r'-', '_', tag)
    else:
        output = tag

    return output