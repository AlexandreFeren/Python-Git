'''
Attempt to create a new version control directory
Check down file system to see if in repo
'''
import os
import sys
import subprocess
import warnings

def re_init(git_dir):
    # TODO: pull in templates as needed
    return

def move_dir(dest):
    """
    Args:
        curr (str): current location of .git folder
        dest (str): destination of .git folder, including \\.git at end

    Raises:
        Exception: target must be empty
    """
    curr = os.getcwd()+'\\.git'
    print("curr "+curr)
    # TODO: move file, make symlink
    if not os.path.isabs(dest):
        # TODO: create path if it does not exist
        dest = os.getcwd()+dest[1:]
        if not os.path.exists(dest): raise Exception("path "+dest+" does not exist")

    if os.path.isabs(dest):
        print("move"+curr,dest)
        if os.listdir(dest) == [] and os.path.exists(curr):
            os.replace(curr,dest)
            with open(curr,'a+') as symlink:
                symlink.write("gitdir: "+dest)
        else: raise Exception("unable to move",curr,"to",dest+": Directory not empty")
    else:
        if os.listdir(dest) == [] and os.path.exists(curr):
            # print(curr,dest[1:])
            os.replace(curr,dest)
            with open(curr,'a+') as symlink:
                symlink.write("gitdir: "+dest)
        else: raise Exception("unable to move",curr,"to",dest+": Directory not empty")
        # with open(curr,'a+') as symlink:
        #         symlink.write("gitdir: "+dest)
    
def is_git_dir(path):
    '''
    return true if there is an existing valid repo
    else - return false if no existing symlink | raise error if there is an existing symlink
    '''
    expected_dirs = ['hooks','info','objects','refs']
    expected_files = ['HEAD','config','description']
    
    for _,dirs,files in os.walk(path):
        # check all expected directories\\files exist
        if path != os.getcwd():
            # symlink, if there is a link, the repo should be valid
            if all([i in dirs for i in expected_dirs]) and all([i in files for i in expected_files]):
                return True
        else:
            if all([i in dirs for i in expected_dirs]) and all([i in files for i in expected_files]):
                return True
        return False
    
    
def format_init_args(args):
    '''
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
    quiet, bare, template,separate_git_dir,object_format,branch,shared = (False,'\\.git','','','sha1','main','group')
    
    for i in args:
        if len(i) == 1 and (i[0] == '--quiet' or i[0] == '-q'): quiet = True
        elif len(i) == 1 and (i[0] == '--bare'): bare=''
        elif len(i) == 2 and (i[0] == '--template'): template = i[1].replace('/','\\')
        elif len(i) == 2 and (i[0] == '--separate-git-dir'): separate_git_dir = i[1].replace('/','\\')
        elif len(i) == 2 and (i[0] == '--object-format'): object_format = i[1]
        elif len(i) == 2 and (i[0] == '-b' or i[0] == '--initial-branch'): branch = i[1]
        elif len(i) == 2 and (i[0] == '--shared'): shared = i[1]
        else: raise ValueError('invalid command',i[0], i)
    return (quiet,bare,template,separate_git_dir,object_format,branch,shared)

def add_files(path,branch):
    # create new repo or populate incomplete existing repo
    if not os.path.isdir(path+'\\hooks'): os.makedirs(path+'\\hooks')
    if not os.path.isdir(path+'\\info'): os.makedirs(path+'\\info')
    if not os.path.isdir(path+'\\objects'): os.makedirs(path+'\\objects')
    if not os.path.isdir(path+'\\objects\\info'): os.makedirs(path+'\\objects\\info')
    if not os.path.isdir(path+'\\objects\\pack'): os.makedirs(path+'\\objects\\pack')
    if not os.path.isdir(path+'\\refs'): os.makedirs(path+'\\refs')
    if not os.path.isdir(path+'\\refs\\heads'): os.makedirs(path+'\\refs\\heads')
    if not os.path.isdir(path+'\\refs\\tags'): os.makedirs(path+'\\refs\\tags')
    
    with open(path+'\\HEAD','a+') as HEAD: HEAD.write("refs\\heads\\"+branch)
    open(path+'\\config','a+')
    open(path+'\\description','a+')

def handle_symlink(repo):
    return 
    
def init(args):
    '''
    initialize git repository, just make skeleton by default.
    git init <flags>
        [-q|--quiet]
            - only print errors and warnings
        [--bare]
            - create without .git folder below newly created
        TODO: [--template = <template-directory>]
            - specify template directory
        TODO: [--separate-git-dir <git-dir>] 
            - create symlink as text file pointing to repo named '.git'. 
            works similarly to --bare from that location, cannot be used with --bare
            - if repo exists in context, moves current git repo to that path
        TODO: [--object-format=<format>]
            - specify has as 'sha1' (default) or 'sha256'
        [-b <branch-name> | --initial-branch=<branch-name>]
            - create new branch with default name in HEAD (main\\master)
            - create repo with main branch <branch-name>
                HEAD will contain: ref: refs\\heads\\<master-branch-name>
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
    quiet,bare,template,git_dir,object_format,branch,shared = format_init_args(args[1:])
    if bare == '' and git_dir != '': raise ValueError("fatal: options '--separate-git-dir' and '--bare' cannot be used together")
    
    
    symlink = None
    
    if git_dir != '': symlink = True
    else: 
        symlink = False
        git_dir = os.getcwd()+bare
    
    # basic flag error checking
    
    
    if is_git_dir(git_dir):
        # TODO
        # running init again will either just be used to move directory
        # with separate-git-dir (to empty repo)
        # or pick up new templates
        if symlink:
            if os.path.isdir(os.getcwd()+'\\.git'):
                move_dir(git_dir)
        
        re_init(git_dir)
        if not quiet: print('Reinitialized existing Git repository in '+git_dir)
    else:
        # check for symlinks
        if symlink:
            if os.path.isdir(os.getcwd()+'\\.git'):
                print("move for symlink")
                move_dir(git_dir)
                pass
            return
        
        # initialize empty
        if bare == '\\.git' and not(os.path.isdir(git_dir)) and not(symlink):
            os.makedirs(git_dir)
            subprocess.check_call(["attrib","+H",git_dir])  # hide .git folder
        add_files(git_dir,branch)
        
        # set symlink if needed
        if symlink and not '.git' in os.listdir(os.getcwd()):
            with open(os.getcwd()) as symlink:
                symlink.write("gitdir: "+git_dir)
                subprocess.check_call(["attrib","+H",os.getcwd()+'\\.git'])  # hide .git file
        if not quiet: print("Initialized empty Git repository in "+git_dir)