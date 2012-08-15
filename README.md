#Huboard Label Tools
This is a set of simple tools written in Python to make managing a large numbe of project with Huboard (https://github.com/rauhryan/huboard) easier. To get started download the scripts, install RestKit and run the scripts from the command line with Python.  These scripts have only been tested with Python 2.7 at this point and the prompts and feedback are still a little rough.

###Requirements

    restkit==4.2.0


##add-standard-labels.py
This script will create a set of standard labels in a repository. The labels are defined in the script in a variable.  The format is a Python tuple ('name','color') where name is the name of the label and color is a 6-digit hex color code (just the code, no '#' or any other prefix).

###Usage

The script will prompt you for a repository and your git credentials.  If you don't have access to the repository or don't have authorization to make the changes, the script will fail. The repository should be specified as ``<user|org>/<repository>`` e.g. ``azumafuji/huboard-label-tools``.

    $ python add-standard-labels.py
    This script will create the default labels 0 - Backlog, 1 - On Deck,
    2 - Analysis, 3 - Developing, 4 - Acceptance, 5 - Production Close in
    your specified repository if they do not yet exist.
    Repository: azumafuji/huboard-label-tools
    Username: azumafuji
    Password:
    Adding 0 - Backlog
    Adding 1 - On Deck
    Adding 2 - Analysis
    Adding 3 - Developing
    Adding 4 - Acceptance
    Adding 5 - Production Close


##cleanup-link-colors.py
This script will update the color of all the 'Link <=> ...' labels used by Huboard to link repositories together.  The script will cycle through a set of colors defined in the script and apply them to the link labels. The intent is to make the link lables distinguishable in the Huboard but not so obtrusive that they would be visually distracting.

###Usage
The script will prompt you for a repository and your git credentials.  If you don't have access to the repository or don't have authorization to make the changes, the script will fail. The repository should be specified as ``<user|org>/<repository>`` e.g. ``azumafuji/huboard-label-tools``.

    $ python cleanup-link-colors.py
    This script will update the Link issue colors in a repository for use with
    Huboard. Labels that start with Link <=> will be updated.
    Repository: azumafuji/huboard-label-tools
    Username: azumafuji
    Password:
    Updating Link Link <=> azumafuji/huboard-label-tools
    {'color': 'b2ffcc', 'name': u'Link <=> azumafuji/huboard-label-tools'}


