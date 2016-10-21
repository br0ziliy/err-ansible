from os import walk, path

def myreaddir(directory):
    """
    Reads a directory, creates array of filenames and checks
    if the first line is a comment, and puts this as a description in the same array.
    """

    array = []
    # walk() and path() come from "os" module
    for (dirpath, dirnames, filenames) in walk(directory):
        for fil in filenames:
            obj = {'fname': path.join(dirpath, fil), 'comment': ""}
            array.append(obj)
    for idx, obj in enumerate(array):
        fname = obj['fname']
        with open(fname, 'r') as fhandle:
            line = fhandle.readline()
            if line.startswith('#'):
                obj['comment'] = line.rstrip()
                array[idx] = obj
            absname = array[idx]['fname']
            relname = absname[len(directory)+1:]
            array[idx]['fname'] = relname
    return array

