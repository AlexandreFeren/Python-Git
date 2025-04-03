# https://git-scm.com/docs/git-add
# https://github.com/git/git/blob/867b1c1bf68363bcfd17667d6d4b9031fa6a1300/Documentation/technical/index-format.txt#L38
"""
    makes modifications to the index file in .git/index
    This is where all of the changes are staged before they are committed

git add actions:
create a blob fro the file(S) that are being added
add the file name and hash to the index file
mark the file as tracked/staged

the index is then used to create the commit
"""

import os
# from stat import *


def parse_index(fname="Dev_Notes/Git_Internal_Files/Index/index_at_f6c5889"):
    files = []
    with open(fname, "rb") as f:
        """
        From https://stackoverflow.com/questions/4084921/what-does-the-git-index-contain-exactly

        4 byte signature: DIRC (dircache)
        4 byte version number (currently 0x0002)
        32 bit number of index entries

        for each index entry, in alphabetical order:
            Extensions
            4 byte extension signature
            32 bit size of the extension
            extension data (alphabetical by file path relative to .git directory)
            160 bit SHA-1 hash of the index contents

        """
        print(os.stat("../.gitignore"))
        index = f.read()
        offset = 12

        # Header
        # input("header:")
        print("\tSignature:", index[:4].decode("utf-8"))
        print("\tVersion:", int.from_bytes(index[4:8]))
        print("\tNumber of index entries:", int.from_bytes(index[8:12]))

        # Index Entries
        # input("sorted list of index entries:")
        for _ in range(int.from_bytes(index[8:12])):
            # changed timestamp
            print("\tctime epoch (s)", int.from_bytes(
                index[offset: 4 + offset]))
            print("\tctime epoch (ns)", int.from_bytes(
                index[4 + offset: 8 + offset]))
            # modified timestamp (metadata)
            print("\tmtime epoch (s)", int.from_bytes(
                index[8 + offset: 12 + offset]))
            print(
                "\tmtime epoch (ns)", int.from_bytes(
                    index[12 + offset: 16 + offset])
            )
            # input()
            print("\n\tdev:", int.from_bytes(index[16 + offset: 20 + offset]))
            print("\tino:", int.from_bytes(index[10 + offset: 24 + offset]))

            print("\tmode:", hex(int.from_bytes(
                index[24 + offset: 28 + offset])))
            print("\tuid:", int.from_bytes(index[28 + offset: 32 + offset]))
            print("\tgid:", int.from_bytes(index[32 + offset: 36 + offset]))
            print("\tsize:", int.from_bytes(index[36 + offset: 40 + offset]))
            print(
                "\tSHA-1 hash:", hex(int.from_bytes(
                    index[40 + offset: 60 + offset]))
            )

            print("\tflags:", hex(int.from_bytes(
                index[60 + offset: 62 + offset])))
            # beyond here is only v3/v4+
            # only working with v2 for now

            # file name, variable length, NUL-terminated
            print("\tfile name: ", end="")
            filename = ""
            while index[62 + offset] != 0:
                print(chr(index[62 + offset]), end="")
                filename += chr(index[62 + offset])
                offset += 1
            files.append(filename)
            print("\n")
            # input('\nend of fname')
            offset += 62
            # variable nul bytes:
            # 1-8 nul bytes as necessary to pad the entry
            # to a multiple of eight bytes while keeping the name NUL-terminated.
            # does not include the header bytes.
            while index[offset] == 0:
                offset += 1

        # Extensions
        print("Signature:", index[offset: offset + 4].decode("utf-8"))
        # TREE          - trees that existed in the index at the time of last commit
        # REUC          - resolve undo data, saved here when resolved
        # link          - split index mode specific, no plans to implement
        # UNTR          - untracked cache, saves untracked files to verify cache
        # FSMN          - File System Monitor Cache, used by fsmonitor
        # EOIE          - End of Index Entry, used to locate beginning of extensions without parsing the entire index
        # IEOT          - Index Entry Offset Table, enables multi-threaded conversion from disk to memory
        # sdir (v5+)    - sparse directory entries
        return files


def generate_index(index_path, root="."):
    """
    take the existing index, parse it, and create a new index file
    """

    # files = parse_index(index_path)

    # get parent directory while it exists and we have not found the .git folder
    while ".git" not in os.listdir(root) and os.path.abspath(root) != os.path.abspath(
        "..\\" + root
    ):
        root = "..\\" + root
    root = os.path.abspath(root)
    # print(os.listdir(root))
    for i in os.listdir(root):
        print(root + "\\" + i)

    # ist_files(root)

    # traverse the tree and note tracked/untracked files


def add():
    """
    add a file to the index
    """
    parse_index()


# parse_index()
# generate_index('Dev_Notes/Git_Internal_Files/Index/index_at_f6c5889')
