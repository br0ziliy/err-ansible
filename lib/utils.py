from os import walk, path
import codecs
from errbot.templating import tenv

def myreaddir(directory):
    """
    Reads a directory, creates array of filenames and checks
    if the first line is a comment, and puts this as a description in the same array.
    """

    array = []
    # walk() and path() come from "os" module
    for (dirpath, dirnames, filenames) in walk(directory):
        try:
          dirnames.remove('roles')
        except ValueError:
          pass
        for fil in filenames:
            obj = {'fname': path.join(dirpath, fil), 'comment': ""}
            array.append(obj)
    for idx, obj in enumerate(array):
        fname = obj['fname']
        with codecs.open(fname, 'r', encoding='utf-8', errors='ignore') as fhandle:
            line = fhandle.readline()
            if line.startswith('#'):
                obj['comment'] = line.rstrip()
                array[idx] = obj
            absname = array[idx]['fname']
            relname = absname[len(directory):]
            array[idx]['fname'] = relname
    return array

def get_template(backend, func):
    """ Selects a template based on the current backend """
    templates = [
        "".join([backend, "_", func, ".md"]),
        "".join(["default_", func, ".md"])
    ]
    return tenv().get_or_select_template(templates).name
