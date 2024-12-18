
'''
constantly run this, awaiting commands for version control.
'''
import sys
import os
import warnings

class Main:
    def __init__(self):
        self.commands = ['diff','Work_Tree.init']
    
    def parse_args(self,args):
        args = args.split()
        if args:
            args[0] = args[0]+".py"
        return args

    def call_command(self, argv):
        if argv == []: return
        full_path = os.path.dirname(os.path.realpath(__file__))+"\\Work_Tree\\"+argv[0]
        cwd = os.getcwd()
        sys.argv = argv
        if argv[0][:-3] in self.commands:
            with open(full_path) as f:
                exec(f.read(),{'argv':argv})
            return [full_path,cwd,argv]
        else: 
            warnings.warn("function '"+argv[0][:-3]+"' does not exist")

if __name__ == '__main__':
    main = Main()
    argv = main.parse_args(input())
    getattr(main, 'call_command')(argv)