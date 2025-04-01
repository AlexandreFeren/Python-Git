import os, shutil, io
from platform import system
from subprocess import call
import warnings, git_clone.src.text_colors as color

def format_init_args(args):
    # https://git-scm.com/docs/git-init
    '''
    set variables to match format of command line args
    
    quiet: bool
    bare: str: .git by default, '' if flag is set
    template: str (file path)
    separate_git_dir: str (file path)
    object-format : str (sha1 or sha256)
    branch: str (main branch name/branch to make name)
    shared: str ([unmask|false|group|true|all|world|everybody|0xxx (octal))
    '''
    for i in range(len(args)):
        args[i] = args[i].split('=')
    quiet, bare, template,separate_git_dir,object_format,branch,shared = (False,'/.git','','','sha1','master','group')

    for i in args:
        if len(i) == 1 and (i[0] == '--quiet' or i[0] == '-q'): quiet = True
        elif len(i) == 1 and (i[0] == '--bare'): bare=''
        elif len(i) == 2 and (i[0] == '--template'): template = i[1].replace('\\','/')
        elif len(i) == 2 and (i[0] == '--separate-git-dir'): separate_git_dir = i[1].replace('\\','/')
        elif len(i) == 2 and (i[0] == '--object-format'): object_format = i[1]
        elif len(i) == 2 and (i[0] == '-b' or i[0] == '--initial-branch'): branch = i[1]
        elif len(i) == 2 and (i[0] == '--shared'): shared = i[1]
        else: raise ValueError('invalid command',i[0], i)

    return (quiet,bare,template,separate_git_dir,object_format,branch,shared)

def get_git_dir():
    """
    return location of the .git folder if you are in a repo, else False
    if there is a link, return the location the link points to (TODO)
    """
    path = "."
    while os.getcwd() != os.getcwd()+"\\..":
        if '.git' in next(os.walk(path))[1]: return os.path.abspath(path)
        path += "\\.."
    return False

def valid_git_dir(path):
    '''
    return repo path if there is an existing valid repo, else False
    else - return false if no existing symlink | raise error if there is an existing symlink
    '''
    expected_dirs = ['hooks','info','objects','refs']
    expected_files = ['HEAD','config','description']
    
    for _,dirs,files in os.walk(path):
        if (all([d in dirs for d in expected_dirs]) and 
            all([f in files for f in expected_files])): return True
        return False

def move_dir(src,dest):
    return

def init(args,debug=False):
    '''
    initialize git repository, just make skeleton by default.
    git init <flags>
        [-q|--quiet]
            - only print errors and warnings
        [--bare]
            - create without .git folder below newly created
        TODO: [--template = <template-directory>]
            - specify template directory
        [--separate-git-dir <git-dir>]
            - create symlink as text file pointing to repo named '.git'.
            works similarly to --bare from that location, cannot be used with --bare
            - if repo exists in context, moves current git repo to that path
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
    '''
    # symlink can just be separate_git_dir?
    quiet,bare,template,separate_git_dir,object_format,branch,shared = format_init_args(args[1:])
    curr_git_dir = get_git_dir()
    print("test")
    if curr_git_dir:    # reinitializing
        if valid_git_dir(curr_git_dir):
            """
            -b|--initial-branch should be ignored here
            """
            if not separate_git_dir:
                print("reinit")
                raise NotImplementedError("reinitialization not implemented")
            else:
                raise NotImplementedError("separate git dir not implemented")
                # reinitialize at remote location
                move_dir(curr_git_dir,separate_git_dir)
                pass
    # else:
    #     if symlink:
    #         """
    #             this may need work for clarity, but here it is already
    #             known that the target of `git_dir` is not a valid repo.
    #             thus, if there is a .git `file` in cwd, there is
    #             a symlink pointing to an invalid repo.

    #             TODO: confirm that pointing to 2 different
    #             remote repos does not work/fails correctly
    #         """
    #         if os.path.isfile(os.getcwd()+'/.git'):
    #             print('not a valid git repository')
    #         elif os.path.isdir(os.getcwd()+'/.git'):
    #             if not quiet: print("Reinitialized existing Git repository in "+git_dir)
    #             # need to move dir and make symlink
    #             move_dir(git_dir)
    #         else: # git directory does not exist, initialize and make symlink
                
    #             if not quiet: print("Initialized empty Git repository in "+git_dir)
    #             add_files(git_dir,branch)
    #             hide(git_dir) # hide git_dir folder with command line args
    #         return # we have done all the symlink work, return to ignore other code

    #     # normal init,make directory
    #     if bare == '/.git' and not(os.path.isdir(git_dir)) and not(symlink):
    #         os.makedirs(git_dir)
    #         os.system(f'attrib +h "{git_dir}"') # hide .git
    #     # add files, either to ./.git or .
    #     add_files(git_dir,branch)
    #     if not quiet: print("Initialized empty Git repository in "+git_dir)