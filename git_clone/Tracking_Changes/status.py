"""
    Need to understand the .gitignore file to know what to ignore and what to display
"""
import git_clone.Tracking_Changes.ls_tree as ls_tree

def format_status_args():
    '''
    parse the command line arguments
    '''
    pass

def status(args):
    """
    TODO:
    - check if file has been modified
    - check if file has been staged

    """
    ls_tree.get_tracked_files()