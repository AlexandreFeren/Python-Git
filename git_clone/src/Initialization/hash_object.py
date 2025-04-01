# https:/git-scm.com/docs/git-hash-object
import hashlib
import git_clone.src.text_colors as color
import warnings


def hash_object(args):
    """
    TODO:
        - Write to objects folder
        - Accept flags
        - Support all file formats

    if implementing git-cat-file at some point in the future:
    - https:/git-scm.com/docs/gitrevisions
    """
    warnings.warn(
        color.b_colors.WARNING
        + "hash-object currently defaults to utf-8 with no check"
        + color.b_colors.END_C
    )
    warnings.warn(
        color.b_colors.WARNING
        + "hash-object currently cannot write to a file"
        + color.b_colors.END_C
    )
    print()
    contents = ""
    with open(args[1]) as f:
        contents = bytes(f.read(), "utf-8")
        full_text = bytes("blob " + str(len(contents)) +
                          "\x00", "utf-8") + contents
        print(hashlib.sha1(full_text).hexdigest())
        # this will be what goes into the file when fully implemented
        # c = zlib.compress(full_text)
    f.close()
