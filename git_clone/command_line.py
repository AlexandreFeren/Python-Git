import git_clone.main as main
import sys

def cli():
    CLI = main.Main()
    if len(sys.argv) > 1:
        CLI.call_command(sys.argv[1:])