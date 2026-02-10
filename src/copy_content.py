import os
import shutil

# Recursively copy 'src' to 'dest' (creating new files or subdirs out or 'src')
def copy_content(src, dest, root=True):
    if root and os.path.exists(dest) and not os.path.isfile(dest):
        shutil.rmtree(dest)
    os.mkdir(dest)
    entryList = os.listdir(src)
    for e in entryList:
        entry = os.path.join(src, e)
        print(entry)
        if os.path.isfile(entry):
            shutil.copy(entry, dest)
        else:
            branch = os.path.join(dest, e)
            copy_content(entry, branch, False)
    return