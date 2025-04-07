## Setup
From the main folder, run `pip install .` to get the CLI working.

This is currently very much a work in progress, so most commands will not work until noted otherwise. So far, init and hash-object are the only mostly working commands as of March 2025.

## Goals
This is primarily an exercise for me to better understand source control, with the intention of making a basic functional source control system.

- CLI through argparse library complete with docs and help
- Majority test coverage over the full project
- Commit pipeline, run test coverage
- Ability to push to GitHub with git-clone

### Functions Implemented
#### Initialization
- init
#### Work on local version
- hash-object
#### Branching/Collaboration
#### Other
- can parse .gitignore to get the list of files that should be tracked

### Functions to Implement
#### Initialization
- clone
#### Work on local version
- commit, add, remove, ignore file
#### Branching/Collaboration
- branch, merge, status, pull, push, fetch, rebase

##  Sources
- https://git-scm.com/book/en/v2/ (mostly chapter 10: Git Internals).
