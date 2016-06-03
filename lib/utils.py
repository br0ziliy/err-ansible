from os import walk
from subprocess import check_output, STDOUT, CalledProcessError
from rq import Queue, use_connection
from redis import ConnectionError

use_connection()
q = Queue('ansible')

def run_cmd(bot, cmd, _from):
    """
    Runs specified command synchronously (if Redis is running) or
    asynchronously (this is not recommended for production use since the whole
    bot will be blocked until a command returns.
    """

    bot.log.info("Running {}".format(cmd))
    async = True
    try:
        job = q.enqueue(check_output, cmd, stderr=STDOUT)
        return "Task enqueued: {}".format(job)
    except ConnectionError:
        bot.log.error("Error connecting to Redis, falling back to synchronous execution")
        async = False
    if not async:
        # notify also chatrooms and/or bot admins
        bot.send(_from,"Running the task synchronously, whole bot blocked now, please wait.")
        try:
            raw_result = check_output(cmd, stderr=STDOUT)
        except CalledProcessError, e:
            raw_result = e.output
        except OSError:
            raw_result = "*ERROR*: ansible-playbook command not found"
        return raw_result

def get_task_info(uuid):
    """
    Gets task info by it's UUID
    """

    job = q.fetch_job(uuid)
    res = job.result
    if res: return res
    else: return "Job {} is still running".format(uuid)

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
    for idx, f in enumerate(filenames):
        myfile = "".join([directory,f])
        with open(myfile, 'r') as fh:
            line = fh.readline()
            if line.startswith('#'): filenames[idx] = "".join([f," - ",line.rstrip()])
        array = filenames
    return array

