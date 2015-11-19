from __future__ import print_function

def myprint(str, *args):
    print(str % args, end='')

def dictContainsValue(dict, value):
    for k, v in dict.iteritems():
        if value == v:
            return True

    return False

def dictKeyForValue(dict, value):
    for k, v in dict.iteritems():
        if value == v:
            return k

    return None
