Situation:

Client has a large collection of files at a directory with many subfolders/files. 
They want to collect them in one location for whatever reason, to print, etc.

How does it work?

Take user input of directory name/new folder name, format it so it's workable within python.
Try to make the new folder within this directory, handle cases where it's already created or locatiion is invalid.
Iterate through the root, directories, and files to move them into the new folder.
This moves the files but preserves the old folder location. May be useful in knowing what you had before you moved it all.


