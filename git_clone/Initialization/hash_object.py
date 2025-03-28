# https://git-scm.com/docs/git-hash-object
import hashlib, os
import zlib
import sys


def format_hash_object_args(args):
    """
    minimal implementation currently
    -t <type>
    -w
    """
    obj_type,write = ('blob',False)
    for i in range(len(args)):
        if args[i] == '-t':
            try:
                obj_type = args[i+1]
            except IndexError:
                print("error: -t flag requires an argument")
                sys.exit(1)
        elif args[i] == '-w': write = True
    return obj_type, write, args[-1]
    
def hash_object(args):
    """
    target: str (file path)
    
    if implementing git-cat-file at some point in the future:
    - https://git-scm.com/docs/gitrevisions
    """
    obj_type,write,target = format_hash_object_args(args)
    print(obj_type,write,target)
    
    print(args)
