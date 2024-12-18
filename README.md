# This is an exercise for me to better understand source control, with the intention of making a basic functional source control system.
## Goals

### Initialization
- init
- clone (?) This would be working entirely locally at least for now

### Work on local version
- commit
- add
- remove
- ignore file

### Branching/Collaboration
- branch
- merge
- status
- pull
- push
- fetch
- squash commits

## Git File structure

- index - store all file data if tracked 
    - (M)odified
    - (A)dded
    - (D)eleted
    - (C)lean
    - also info about the level in the hierarchy
- HEAD - reference to the head file(s)
- description
- config
- COMMIT_EDITMSG
> refs
    > heads - file for each branch w/hash for it
    > tags
> objects
    > <list of references to *files* (?)>
    > info
    > pack
> logs
    > refs/heads
        - <list of branches (?) and commit history (?)>
      - HEAD - unsure, TBD
> info
    - exclude - unsure, maybe .gitignore related