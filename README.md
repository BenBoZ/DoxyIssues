# DoxyIssues
Python script to pull issues from Github repo and convert them to Doxygen file

## Usage
   doxy\_issues.py [-h] [-u USER] [-r REPO] [-s {open,closed,all}]
                         [-o OUTPUT_PATH]

   doxy\_issues retrieves all github issues from the given repo and outputs them
   in a format which is suitable for Doxygen.

   optional arguments:
     -h, --help            show this help message and exit
     -u USER, --user USER  The user or organization of the repo
     -r REPO, --repo REPO  The name of the repo
     -s {open,closed,all}, --state {open,closed,all}
                           Define in which state the issues are in
     -o OUTPUT_PATH, --output_path OUTPUT_PATH
                           The relative or absolute path where the file will be
                           written
