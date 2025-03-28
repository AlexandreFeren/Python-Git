import hashlib, os
import zlib
import sys

# TODO: Make test that use file locations and the corresponding hashes 
# files_and_hashes = {"README.md":"a522da6e8c23b4da792335364211fa2ff9efe78a"}
# folders_and_hashes = {"Source":"6f7831be3fc92736e185c20fadae9d61504dff4e"}

def hash_blob(file_name):
    # blob <file length><NUL><file contents>
    contents = ""
    with open(file_name,'rb') as f:
        contents = f.read()
    full_text = bytes('blob '+str(len(contents))+'\0','utf-8')+contents
    print(hashlib.sha1(full_text).hexdigest())
    return

def hash_tree(file_name):
    """
    tree <byte length><NUL>[<file/dir mode> <file name><NUL><SHA-1 Hash>]*
        the files are stored alphabetically, starting with folders
    """
    return

def hash_commit():
    """
    commit <byte length> tree <hash>
    parent <previous commit hash>
    author <name> <email> <timestamp> <timezone>
    committer <name> <email> <timestamp> <timezone>
    
    <commit message>\n
    
    """
    return
def __display_tree(iterator,i):
    """
    mimics git cat-file -p master^{tree}
    """
    mode_and_target = ""
    type = {ord("t"):"tree",ord("b"):"blob"}
    hash = ""
    
    while True:
        if i == 0: break
        i = next(iterator)

    while True:
        i = next(iterator,"end")
        if i == "end": break
        if i == 0: # file name terminator
            print(" ",end = "")
            hash = ""
            for i in range(20):
                i = next(iterator)
                if len(str(hex(i)[2:])) == 1: # if the hex value is under 16
                    i = "0"+str(hex(i)[2:])
                    hash += i
                else: hash += hex(i)[2:]
            
            print("0"*(6-len(mode_and_target.split()[0]))+mode_and_target.split()[0],end = " ")
            with open("../.git/objects/"+hash[:2]+"/"+ hash[2:],'rb') as f:
                print(type[zlib.decompress(f.read())[0]],end = " ")
            print(hash,end = "   ")
            print(mode_and_target.split()[-1])
            mode_and_target = ""
            hash = ""
        else:
            mode_and_target += chr(i)
    print()

def __return_readable_object(hash):
    """
    return the decompressed object, works for both blobs and trees
    """
    #print(os.listdir('../.git/objects/'+hash[:2])+hash[2:])
    #print(hash[2:])
    with open('../.git/objects/'+hash[:2]+'/'+hash[2:],'rb') as f:
        contents = f.read()
    try:
        print(zlib.decompress(contents).decode('utf-8'))
    except UnicodeDecodeError:
        # must be tree or blob, not sure where tags belong yet
        iterator = iter(zlib.decompress(contents))
        i = next(iterator)
        if i == ord("t"):
            __display_tree(iterator,i)
        elif i == ord("b"):
            __display_blob(iterator,i)
        else:
            print(zlib.decompress(contents))
        print(zlib.decompress(contents))
            
#hash_blob("../README.md")
#__return_readable_object("169bd833864cf29aac96936653141958adf5962d")
#print("-"*50)
#__return_readable_object("a522da6e8c23b4da792335364211fa2ff9efe78a")
#__display_blob("a522da6e8c23b4da792335364211fa2ff9efe78a")  #README.md
"""
General info about git objects:   

example Blob before compression:
    blob 15\x00'test content'

example Tree before compression:
    tree 155\x0040000 Initialization\x00\xae\xf8\xa7\x88\x9a$\xdf|\xce\xf7\x1fCh\x13\xa3\xdb\x96\xd5"_100644 __init__.py\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91100644 main.py\x00\xbd\x06\x16FG\xe1>\x82\x0f5\xfb\xfc\xe0]\xb9\x90\x03\xcd\xfc\x86100644 test_main.py\x00\xcf\xb9\x17\xc4\xfc\xbc\xe8\xbb1\xee\x86\x9a\xc4t\x0b\xfb\x04\xaa\xbf\xee

example Commit before compression:
    commit 243\x00tree 169bd833864cf29aac96936653141958adf5962d
    parent 883c1548dc1736535490d7bb83fec8ef0c95488c
    author Alex Feren <alexandre.feren@gmail.com> 1736197528 -0500
    committer Alex Feren <alexandre.feren@gmail.com> 1736197528 -0500

    clean up README.md\n

Blob format: blob <file length><NUL><file contents>

Tree format: tree <byte length><NUL>[<file/dir mode> <file name><NUL><SHA-1 Hash>]*
    after the <NUL> the contents can be repeated multiple times.
    byte length is the sum of lengths for everything after the <NUL>
    
Commit format: commit <byte length><NUL><current commit hash>\nparent <previous commit hash>\nauthor <name> <email> <timestamp> <timezone>\ncommitter <name> <email> <timestamp> <timezone>\n\n<commit message>\n
"""
# example Blob before compression:
# blob 15\x00'test content'
# example Tree before compression:
# tree 155\x0040000 Initialization\x00\xae\xf8\xa7\x88\x9a$\xdf|\xce\xf7\x1fCh\x13\xa3\xdb\x96\xd5"_100644 __init__.py\x00\xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91100644 main.py\x00\xbd\x06\x16FG\xe1>\x82\x0f5\xfb\xfc\xe0]\xb9\x90\x03\xcd\xfc\x86100644 test_main.py\x00\xcf\xb9\x17\xc4\xfc\xbc\xe8\xbb1\xee\x86\x9a\xc4t\x0b\xfb\x04\xaa\xbf\xee
# example Commit before compression:
# commit 243\x00tree 169bd833864cf29aac96936653141958adf5962d\nparent 883c1548dc1736535490d7bb83fec8ef0c95488c\nauthor Alex Feren <alexandre.feren@gmail.com> 1736197528 -0500\ncommitter Alex Feren <alexandre.feren@gmail.com> 1736197528 -0500\n\nclean up README.md\n
# tree <byte length><NUL>
# <file/dir mode> <file name><NUL><SHA-1 Hash>

# tree 155\x00
# 40000 Initialization\x00
# \xae\xf8\xa7\x88\x9a\x24\xdf\x7c\xce\xf7\x1f\x43\x68\x13\xa3\xdb\x96\xd5\x22\x5f
# 100644 __init__.py\x00
# \xe6\x9d\xe2\x9b\xb2\xd1\xd6CK\x8b)\xaewZ\xd8\xc2\xe4\x8cS\x91
# 100644 main.py\x00
# \xbd\x06\x16FG\xe1>\x82\x0f5\xfb\xfc\xe0]\xb9\x90\x03\xcd\xfc\x86
# 100644 test_main.py\x00
# \xcf\xb9\x17\xc4\xfc\xbc\xe8\xbb1\xee\x86\x9a\xc4\x74\x0b\xfb\x04\xaa\xbf\xee

# 40000 Initialization100644 __init__.py100644 main.py100644 test_main.py0000+(SHA-1 Hash)*4 since each count on the length is 2 bytes

# length = length(modes) + count(trees/blobs)*2 (space + NUL) + length(names)
# folders before files

# '''

# # Initialization__init__.pymain.pytest_main.py
def format_hash_object_args(args):
    # https://git-scm.com/docs/git-hash-object
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