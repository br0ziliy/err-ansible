from os import walk

def myreaddir(directory):
    """
    Reads a directory, creates array of filenames and checks
    if the first line is a comment, and puts this as a description in the same array.
    """

    array = []
    # walk() comes from "os" module
    for (dirpath, dirnames, filenames) in walk(directory):
        array.extend(filenames)
        break
    for idx, fname in enumerate(filenames):
        myfile = "".join([directory, fname])
        with open(myfile, 'r') as fhandle:
            line = fhandle.readline()
            if line.startswith('#'):
                filenames[idx] = "".join([fname, " - ", line.rstrip()])
        array = filenames
    return array

