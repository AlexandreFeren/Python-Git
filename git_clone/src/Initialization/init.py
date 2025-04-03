import os
import io
import warnings
import git_clone.src.text_colors as color


def format_init_args(args):
    # https://git-scm.com/docs/git-init
    """
    set variables to match format of command line args

    quiet: bool
    bare: str: .git by default, '' if flag is set
    template: str (file path)
    separate_git_dir: str (file path)
    object-format : str (sha1 or sha256)
    branch: str (main branch name/branch to make name)
    shared: str ([unmask|false|group|true|all|world|everybody|0xxx (octal))
    """
    for i in range(len(args)):
        args[i] = args[i].split("=")
    quiet, bare, template, separate_git_dir, object_format, branch, shared = (
        False,
        False,
        "",
        "",
        "sha1",
        "master",
        "group",
    )

    for i in args:
        if len(i) == 1 and (i[0] == "--quiet" or i[0] == "-q"):
            quiet = True
        elif len(i) == 1 and (i[0] == "--bare"):
            bare = True
        elif len(i) == 2 and (i[0] == "--template"):
            template = i[1].replace("\\", "/")
        elif len(i) == 2 and (i[0] == "--separate-git-dir"):
            separate_git_dir = os.path.abspath(i[1].replace("\\", "/"))
        elif len(i) == 2 and (i[0] == "--object-format"):
            object_format = i[1]
        elif len(i) == 2 and (i[0] == "-b" or i[0] == "--initial-branch"):
            branch = i[1]
        elif len(i) == 2 and (i[0] == "--shared"):
            shared = i[1]
        else:
            raise ValueError("invalid command", i[0], i)

    return (quiet, bare, template, separate_git_dir, object_format, branch, shared)


def add_files(branch, path=os.getcwd()):
    # create new repo or populate incomplete existing repo
    if not os.path.isdir(path+'/hooks'):
        os.makedirs(path+'/hooks')
    if not os.path.isdir(path+'/info'):
        os.makedirs(path+'/info')
    if not os.path.isdir(path+'/objects'):
        os.makedirs(path+'/objects')
    if not os.path.isdir(path+'/objects/info'):
        os.makedirs(path+'/objects/info')
    if not os.path.isdir(path+'/objects/pack'):
        os.makedirs(path+'/objects/pack')
    if not os.path.isdir(path+'/refs'):
        os.makedirs(path+'/refs')
    if not os.path.isdir(path+'/refs/heads'):
        os.makedirs(path+'/refs/heads')
    if not os.path.isdir(path+'/refs/tags'):
        os.makedirs(path+'/refs/tags')
    io.open(path+'/info/exclude', 'a+', newline='\n')
    with io.open(path+'/HEAD', 'a+', newline='\n') as HEAD:
        HEAD.write("ref: refs/heads/"+branch+'\n')
        HEAD.close()

    with io.open(path+'/config', 'a+', newline='\n') as config:
        config.write("[core]\n\t")
        config.write("repositoryformatversion = 0\n\t")
        config.write("filemode = false\n\t")
        config.write("bare = false\n\t")
        config.write("logallrefupdates = true\n\t")
        config.write("symlinks = false\n\t")
        config.write("ignorecase = true")
        config.close()

    with io.open(path+'/description', 'a+', newline='\n') as desc:
        desc.write(
            "Unnamed repository; edit this file 'description' to name the repository.")
        desc.close()


def get_git_dir():
    """
    return location of the .git folder if you are in a repo, else False
    if there is a link, return the location the link points to (TODO)
    """
    path = os.getcwd()
    print("calling command from " + os.getcwd())
    while os.path.abspath(path) != os.path.abspath(path + "\\.."):
        if ".git" in os.listdir(path):
            return path
        path = os.path.abspath(path + "\\..")
    return False


def hide(path):
    # hide either folder or file
    if path[-1] == '/' or path[-1] == '/':
        path = path[:-1]
    if os.path.isfile(path):
        os.system(f'attrib +h "{path}"')
    elif os.path.isdir(path):
        os.system(f'attrib +h "{path}"')


def valid_git_dir(path):
    """
    return True if valid repo, else False
    """
    expected_dirs = ["hooks", "info", "objects", "refs"]
    expected_files = ["HEAD", "config", "description"]

    for _, dirs, files in os.walk(path):
        if all([d in dirs for d in expected_dirs]) and all(
            [f in files for f in expected_files]
        ):
            return True
        return False


def move_dir(src, dest):
    return


def init(args, debug=False):
    """
    initialize git repository, just make skeleton by default.
    .git, whether file or folder should always be hidden
    if initializing remote, hide folder if it starts with .

    returns
        (directory location,bare)

    git init <flags>
        [-q|--quiet]
            - only print errors and warnings
        [--bare]
            - create without .git folder below newly created
        TODO: [--template = <template-directory>]
            - specify template directory
        [--separate-git-dir <git-dir>]
            - stores .git folder (or whatever you name it) in a different location
              tracking will work the same, it is just now .git is a file
              changes are tracked relative to the directory with .git in it.

        TODO: [--object-format=<format>]
            - specify has as 'sha1' (default) or 'sha256'
        [-b <branch-name> | --initial-branch=<branch-name>]
            - create new branch with default name in HEAD (main/master)
            - create repo with main branch <branch-name>
                HEAD will contain: ref: refs/heads/<master-branch-name>
        TODO: [--shared[=<permissions>]]
            [unmask|false]          -
            [group|true]            - make group (2nd bit,2nd octal) writable, do not remove perm.
            [all|world|everybody]   - group + make readable by all
            <perm>                  - 0<3 digit octal>
                octal - 0<user><group><other>
                bit meaning - <read><write><execute>
                    - full permissions: 0111
                    - no permissions:   0000
    """
    warnings.warn(color.b_colors.WARNING +
                  "TODO: file permissions have not been configured properly yet"+color.b_colors.END_C)
    quiet, bare, template, separate_git_dir, object_format, branch, shared = (
        format_init_args(args[1:])
    )
    if bare and separate_git_dir != '':
        raise ValueError(
            "fatal: options '--separate-git-dir' and '--bare' cannot be used together")
    curr_git_dir = get_git_dir()
    print("bare:", bare, "separate", separate_git_dir, "branch:", branch)

    # bare inits behave differently than the rest
    if bare:
        if not valid_git_dir(os.getcwd()):
            add_files(branch)
        else:
            warnings.warn(color.b_colors.WARNING +
                          "reinitialize bare repo not implemented"+color.b_colors.END_C)
    elif not curr_git_dir:  # has not been initialized yet
        curr_git_dir = os.getcwd()
        if separate_git_dir == "":
            print("normal init")
            add_files(branch, os.getcwd()+"/.git")
            hide(os.getcwd()+"/.git")
        else:
            # .git file, not folder is location of src.
            print("remote init", separate_git_dir)
            with io.open(os.getcwd()+"/.git", 'a+', newline='\n') as f:
                f.write("gitdir: " +
                        os.path.abspath(separate_git_dir)
                        )
            add_files(branch, separate_git_dir)
            hide(os.getcwd()+"\\.git")
            if (separate_git_dir.split("\\")[-1][0] == "." or
                    separate_git_dir.split("/")[-1][0] == "."):
                hide(separate_git_dir)
    else:  # has been initialized
        if os.path.isfile(".git"):  # remote
            warnings.warn(color.b_colors.WARNING +
                          "reinitialize remote not implemented"+color.b_colors.END_C)
        elif separate_git_dir:  # move existing file
            warnings.warn(color.b_colors.WARNING +
                          "reinit remote not implemented"+color.b_colors.END_C)
        else:  # standard reinit
            warnings.warn(color.b_colors.WARNING +
                          "reinit not implemented"+color.b_colors.END_C)
