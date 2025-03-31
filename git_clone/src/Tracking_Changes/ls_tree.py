import os
import fnmatch
# https:\\\\git-scm.com\\docs\\git-ls-tree
'''
plumbing command along with read-tree, used to get files in git status
ignores all unmodified files as well

There are options to change how the output is displayed (see link)
I am currently just defaulting to what will be shown with base `git status`
'''

def get_tracked_files():
    '''
    get the files that are currently tracked
    TODO:
        ! - remove from exclude
        leading / - match from root only
        ** - match any number of directories
    '''
    # preprocess .gitignore, need to keep order from .gitignore
    root = '.'
    while (not '.git' in os.listdir(root)
            and os.path.abspath(root) != os.path.abspath('..\\'+root)):
        root = '..\\'+root

    root = os.path.abspath(root)
    with open(root+'\\'+'.gitignore') as f:
        exclude = f.read().splitlines()
        exclude[:] = [i for i in exclude if i != '']
        exclude[:] = [i for i in exclude if i[0] != '#']
        exclude = [i[1:] if i[0] =='\\' else i for i in exclude]

    # Unused, will be needed to account for ! in .gitignore
    tracked = []
    untracked = []

    # needs to be separated by file and dir
    # because of */ matching only dirs
    exclude.append('.git/') # .git should never be displayed/tracked


    exclude_all = [i for i in exclude if i[-1] != '/']
    exclude_root_all = [i[1:] for i in exclude if i[0] =='/' and i[-1] != '/']

    exclude_dirs = [i[:-1] for i in exclude if i[-1] == '/']
    exclude_root_dirs = [i[1:-1] for i in exclude if i[0] =='/' and i[-1] == '/']

    exclude_root_dirs.extend(exclude_root_all)
    exclude_dirs.extend(exclude_all)

    # traverse repo where not excluded in .gitignore
    # only files get returned, so empty folders will not be tracked
    tracked_files = []
    for full_path, dirs, files in os.walk(root):
        if full_path == root:
            [dirs.remove(d)  for d in [d for d in dirs  if any(fnmatch.fnmatch(d,ex)  for ex in exclude_root_dirs)]]
            [files.remove(f) for f in [f for f in files if any(fnmatch.fnmatch(f,ex)  for ex in exclude_root_all)]]
        [dirs.remove(d)  for d in [d for d in dirs  if any(fnmatch.fnmatch(d,ex)  for ex in exclude_dirs)]]
        [files.remove(f) for f in [f for f in files if any(fnmatch.fnmatch(f,ex)  for ex in exclude_all)]]

        tracked_files.extend([full_path+'\\'+i for i in files])
    return tracked_files

def ls_tree(args):
    return get_tracked_files()
