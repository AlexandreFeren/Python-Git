
'''
constantly run this, awaiting commands for version control.
'''
import sys
import os
import Initialization.init as init
import Initialization.hash_object as hash_object

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
                "clone",
                "hash-object"
            ]
        }

    def call_command(self, args):
        path = os.path.dirname(os.path.realpath(__file__))
        for val,key in enumerate(self.commands):
            if args[0] in self.commands[key]:
                print(key, args)
                self.dispatch(key,args)
                return
        print("not a valid command")
    
    def dispatch(self,folder,args):
        '''
        func_dict is a list of functions to call
        based on command line args
        '''
        func_dict = {"init":init.init,"hash-object":hash_object.hash_object}
        func_dict[args[0]](args)

if __name__ == '__main__':
    main = Main()
    if len(sys.argv) > 1:
        print(sys.argv)
        main.call_command(sys.argv[1:])
        