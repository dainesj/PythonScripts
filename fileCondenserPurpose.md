# Situation

- Client has a large collection of files at a directory with many subfolders/files.  
- They want to collect them in one location for whatever reason, to print, etc.  
- Rather than navigating through many folders and printing, can just move them all to one directory and print en masse.   

# How does it work?

- Take user input of directory name/new folder name, format it so it's workable within python.  
- Try to make the new folder within this directory, handle cases where it's already created or location is invalid.  
- Iterate through the root, directories, and files to copy them into the new folder.  



