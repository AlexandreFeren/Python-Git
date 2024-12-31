'''
TODO: hide .git folder after move, move to correct location
Attempt to create a new version control directory
Check down file system to see if in repo
'''
import os
import subprocess
import warnings
import shutil
from platform import system
from subprocess import call
import io

def hide(path):
    #hide either folder or file
    if path[-1]=='/' or path[-1]=='/':
        path = path[:-1]
    if os.path.isfile(path):
        os.system(f'attrib +h "{path}"')
    elif os.path.isdir(path):
        os.system(f'attrib +h "{path}"')
    
def re_init(git_dir):
    # TODO: pull in templates as needed
    warnings.warn('reinitialization is not yet implemented')

def move_dir(dest):
    # TODO: cleanup
    """
    Args:
        curr (str): current location of .git folder
        dest (str): destination of .git folder, including /<folder-name> at end
    """
    source = os.getcwd()+'/.git'
    #input(dest)
    for file_name in os.listdir(source):
        # print(source,dest)
        if not os.path.isdir(dest): os.makedirs(dest)
        shutil.move(os.path.join(source,file_name),dest)
    os.rmdir(source)
    #make symlink and hide both that and folder
    with io.open(source,'a',newline='\n') as symlink:
        dest = dest.replace("\\","/")
        symlink.write("gitdir: "+dest)
    hide(source)
    hide(dest)

    
def is_git_dir(path):
    '''
    return true if there is an existing valid repo
    else - return false if no existing symlink | raise error if there is an existing symlink
    '''
    expected_dirs = ['hooks','info','objects','refs']
    expected_files = ['HEAD','config','description']
    
    for _,dirs,files in os.walk(path):
        # check all expected directories/files exist
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
    quiet, bare, template,separate_git_dir,object_format,branch,shared = (False,'/.git','','','sha1','master','group')
    
    for i in args:
        if len(i) == 1 and (i[0] == '--quiet' or i[0] == '-q'): quiet = True
        elif len(i) == 1 and (i[0] == '--bare'): bare=''
        elif len(i) == 2 and (i[0] == '--template'): template = i[1].replace('/','/')
        elif len(i) == 2 and (i[0] == '--separate-git-dir'): separate_git_dir = i[1].replace('/','/')
        elif len(i) == 2 and (i[0] == '--object-format'): object_format = i[1]
        elif len(i) == 2 and (i[0] == '-b' or i[0] == '--initial-branch'): branch = i[1]
        elif len(i) == 2 and (i[0] == '--shared'): shared = i[1]
        else: raise ValueError('invalid command',i[0], i)
    
    return (quiet,bare,template,separate_git_dir,object_format,branch,shared)

def add_files(path,branch):
    # create new repo or populate incomplete existing repo
    if not os.path.isdir(path+'/hooks'): os.makedirs(path+'/hooks')
    if not os.path.isdir(path+'/info'): os.makedirs(path+'/info')
    if not os.path.isdir(path+'/objects'): os.makedirs(path+'/objects')
    if not os.path.isdir(path+'/objects/info'): os.makedirs(path+'/objects/info')
    if not os.path.isdir(path+'/objects/pack'): os.makedirs(path+'/objects/pack')
    if not os.path.isdir(path+'/refs'): os.makedirs(path+'/refs')
    if not os.path.isdir(path+'/refs/heads'): os.makedirs(path+'/refs/heads')
    if not os.path.isdir(path+'/refs/tags'): os.makedirs(path+'/refs/tags')
    
    io.open(path+'/info/exclude','a+',newline='\n')
    with io.open(path+'/HEAD','a+',newline='\n') as HEAD: 
        HEAD.write("ref: refs/heads/"+branch+'\n')
        HEAD.close()
    with io.open(path+'/config','a+',newline='\n') as config:
        config.write("[core]\n\t")
        config.write("repositoryformatversion = 0\n\t")
        config.write("filemode = false\n\t")
        config.write("bare = false\n\t")
        config.write("logallrefupdates = true\n\t")
        config.write("symlinks = false\n\t")
        config.write("ignorecase = true")

    with io.open(path+'/description','a+',newline='\n') as desc:
        desc.write("Unnamed repository; edit this file 'description' to name the repository.")

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
    quiet,bare,template,git_dir,object_format,branch,shared = format_init_args(args[1:])
    
    # basic flag error checking
    if bare == '' and git_dir != '': raise ValueError("fatal: options '--separate-git-dir' and '--bare' cannot be used together")
    symlink = None
    
    if git_dir != '':
        symlink = True
        bare = ""   # we are moving just the files in with symlink
    else: 
        symlink = False
        git_dir = os.getcwd()+bare
    
    # TODO: I think this may be incorrect code
    # works if first char is a .
    git_dir = os.path.abspath(git_dir)
    git_dir = git_dir.replace("\\","/")
    #if not os.path.isabs(git_dir): git_dir = os.getcwd()+git_dir[1:]
    
    if is_git_dir(git_dir):
        """
        -b|--initial-branch should be ignored here
        """
        # TODO
        # running init again will either just be used to move directory
        # with separate-git-dir (to empty repo)
        # or pick up new templates
        if symlink:
            # TODO: .git folder name not required, fix this.
            if os.path.isdir(os.getcwd()+'/.git'):
                move_dir(git_dir)
        
        re_init(git_dir)
        if not quiet: print('Reinitialized existing Git repository in', git_dir)
    else:
        if symlink: 
            """
                this may need work for clarity, but here it is already
                known that the target of `git_dir` is not a valid repo.
                thus, if there is a .git `file` in cwd, there is 
                a symlink pointing to an invalid repo.

                TODO: confirm that pointing to 2 different 
                remote repos does not work/fails correctly
            """
            if os.path.isfile(os.getcwd()+'/.git'):
                print('not a valid git repository')
            elif os.path.isdir(os.getcwd()+'/.git'):
                if not quiet: print("Reinitialized existing Git repository in "+git_dir)
                # need to move dir and make symlink
                move_dir(git_dir)
            else: # git directory does not exist, initialize and make symlink
                if not quiet: print("Initialized empty Git repository in "+git_dir)
                add_files(git_dir,branch)
                hide(git_dir) # hide git_dir folder with command line args
            return # we have done all the symlink work, return to ignore other code
        
        # normal init,make directory
        if bare == '/.git' and not(os.path.isdir(git_dir)) and not(symlink):
            os.makedirs(git_dir)
            os.system(f'attrib +h "{git_dir}"') # hide .git
        # add files, either to ./.git or .
        add_files(git_dir,branch)
        if not quiet: print("Initialized empty Git repository in "+git_dir)