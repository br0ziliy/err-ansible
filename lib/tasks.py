from subprocess import check_output, STDOUT, CalledProcessError
from rq import Queue, use_connection
from redis import ConnectionError
from pickle import dumps

use_connection()
q = Queue('ansible')

def run_task(bot, cmd, _from):
    """
    Runs specified command synchronously (if Redis is running) or
    asynchronously (this is not recommended for production use since the whole
    bot will be blocked until a command returns.
    """

    bot.log.debug("Running {}".format(cmd))
    async = True
    try:
        task = q.enqueue(check_output, cmd, stderr=STDOUT)
        tasklist = bot['tasks']
        # need to get string representation of Identity here, since storing of
        # the class itself does not work for every backend, see
        # https://github.com/errbotio/errbot/issues/771 for details
        tasklist[task.get_id()] = str(_from)
        bot['tasks'] = tasklist
        return "Task enqueued: {}".format(task.get_id())
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

    task = q.fetch_job(uuid)
    res = task.result
    status = task.status
    return (res, status)

def handle_task_exception(task, exc_type, exc_value, traceback):
    """
    Custom RQ exception handler
    Most of the time we care about real Ansible output - thus we mangle with the
    "result" field here. RQ stores result as pickled object - we do the same
    here.
    """
    output = exc_value.output
    task_id = task.get_id()
    r = task.connection
    r.hset("rq:job:{}".format(task_id),'result',dumps(output))


