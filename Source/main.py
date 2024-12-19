
'''
constantly run this, awaiting commands for version control.
'''
import sys
import os

class Main:
    '''
    functions considering adding and rough groupings:
    
    initialization/info
        - init
        - clone

    info
        - diff
        - show
        - help
        - log
        - blame
        
    file moves
        - add
        - mv
        - rm
    
    interact with remote
        - reset
        - restore
        - fetch
        - commit
        - remote
        - pull
        
    branching
        - branch
        - checkout
        - merge
        - stash
        
    change cleanup
        - rebase

    under the hood
        - blob creation (on add)
    '''
    def __init__(self):
        # should be able to dynamically generate this dict
        # just exclude non-source folders
        # and create from the rest
        self.commands = {
            "\\Initialization\\":[
                "init",
                "clone"
            ]
        }

    def call_command(self, args):
        path = os.path.dirname(os.path.realpath(__file__))
        for val,key in enumerate(self.commands):
            if args[0] in self.commands[key]:
                self.exec_command(path,key,args)
    
    def exec_command(self,path,folder,args):
        full_path = path + folder + args[0] + ".py"
        with open(full_path) as f:
                exec(f.read(),{'argv':args})

if __name__ == '__main__':
    main = Main()
    if len(sys.argv) > 1:
        main.call_command(sys.argv[1:])